<template>
  <div>
    <div class="card shadow mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h6 class="text-primary">Contract List</h6>
        <button v-if="this.hasPermission('ctrctsapp.add_contract')" class="btn btn-success ml-auto"
          @click="createContract()"> <strong>+</strong> New Contract</button>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <div v-if="loadingContracts" class="spinner-container">
            Loading contracts ...&nbsp;
            <div class="spinner-border" style="width: 4rem; height: 4rem;" role="status"></div>
            <div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status"></div>
            <div class="spinner-grow" style="width: 2rem; height: 2rem;" role="status"></div>
            <div class="spinner-grow" style="width: 1rem; height: 1rem;" role="status"></div>
          </div>
          <table class="table table-striped table-hover table-bordered" id="contractsTable" ref="contractsTable">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Doc Type</th>
                <th scope="col">Type</th>
                <th scope="col">Date</th>
                <th scope="col">Builder</th>
                <th scope="col">Job</th>
                <th scope="col">Model</th>
                <th scope="col">Lot</th>
                <th scope="col">Address</th>
                <th scope="col">SqFt</th>
                <th scope="col">Job Price</th>
                <th scope="col">Options</th>
                <th scope="col">Total</th>
                <th scope="col">Need Print</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { openPdf } from "@/helpers";
import Swal from 'sweetalert2'

export default {
  name: 'ContractsView',
  data() {
    return {
      contracts: [],
      loading_text: 'Loading contracts',
      loadingContracts: true, // Mantener en true hasta que los datos estén listos
    };
  },
  async mounted() {
    try {
      const res = await axios.get('/api/user_detail/');
      this.userId = res.data.id;
      // console.log("🚩this.userId: ",this.userId)
      if (!this.userId) throw new Error('User ID not found');
      this.initDataTable();
    } catch (err) {
      console.error('🧨 Error getting user:', err);
      Swal.fire('Error', 'Unable to fetch user information.', 'error');
    }
  },
  methods: {
    updateContracts(contracts) {
        this.contracts = contracts;
    },
    downloadContract(id) {
      this.loadingContracts = true; // Activa el spinner
      this.loading_text = `Downloading contract ${id} as PDF`;
      axios.get('/web/contract-pdf/' + id)
        .then((response) => {
          openPdf(response.data);
          this.loadingContracts = false;
        })
        .catch(error => {
          console.error('Error fetching contracts:', error);
          this.loadingContracts = false; // Asegúrate de que el spinner se desactive si hay un error
        });
    },

    initDataTable() {
      if (this.$refs.contractsTable) {
        if ($.fn.DataTable.isDataTable(this.$refs.contractsTable)) {
          $(this.$refs.contractsTable).DataTable().destroy();
        }
        const BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/';

        $(this.$refs.contractsTable).DataTable({
          processing: true,
          serverSide: true,
          ajax: {
            url: `${BASE_URL}api/contract/datatable-contracts/?user_id=${this.userId}`,
            dataSrc: function (json) {
              // console.log("✅ DataTables received:", json);
              return json.data;
            },
            beforeSend: function (xhr) {
              const token = sessionStorage.getItem('authToken');
              if (token) {
                xhr.setRequestHeader('Authorization', 'Token ' + token);
              }
            },
          },
          columns: [
            { data: 'id' },
            { data: 'doc_type' },
            { data: 'type' },
            {
              data: 'date_created',
              render: function (data) {
                const date = new Date(data);
                return date.toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                });
              }
            },
            {
              data: 'builder',
              render: (data) => data?.name || ''
            },
            {
              data: 'job',
              render: (data) => data?.name || ''
            },
            {
              data: 'house_model',
              render: (data) => data?.name || ''
            },
            { data: 'lot' },
            { data: 'address' },
            { data: 'sqft' },
            { data: 'job_price' },
            { data: 'total_options' },
            { data: 'total' },
            {
              data: 'needs_reprint',
              render: function (data) {
                return data ? '<span class="badge bg-danger">Yes</span>' : '<span class="badge bg-success">No</span>';
              }
            },
            {
              data: null,
              orderable: true,
              render: (data) => {
                const buttons = [];

                if (this.hasPermission('ctrctsapp.view_contract')) {
                  buttons.push(`<button class="btn btn-outline-success me-1 view-btn" data-id="${data.id}">View</button>`);
                }

                if (this.hasPermission('ctrctsapp.view_workprice')) {
                  buttons.push(`<button class="btn btn-outline-dark me-1 print-btn" data-id="${data.id}">Print</button>`);
                }

                if (this.hasPermission('ctrctsapp.change_contract')) {
                  buttons.push(`<button class="btn btn-outline-primary me-1 edit-btn" data-id="${data.id}">Edit</button>`);
                }

                if (this.hasPermission('ctrctsapp.delete_contract')) {
                  buttons.push(`<button class="btn btn-outline-danger me-1 delete-btn" data-id="${data.id}">Delete</button>`);
                }

                return `<div class="btn-group btn-group-sm">${buttons.join('')}</div>`;
              }
            }
          ],
          pageLength: 25,
          order: [[13, 'desc'], [0, 'desc']],
          responsive: true
        });

        // Eventos después de inicializar
        $(this.$refs.contractsTable).off('click').on('click', '.view-btn', (event) => {
          const id = event.currentTarget.dataset.id;
          this.viewContract(id);
        });

        $(this.$refs.contractsTable).on('click', '.print-btn', (event) => {
          const id = event.currentTarget.dataset.id;
          this.printContract(id);
        });

        $(this.$refs.contractsTable).on('click', '.edit-btn', (event) => {
          const id = event.currentTarget.dataset.id;
          this.editContract(id);
        });

        $(this.$refs.contractsTable).on('click', '.delete-btn', (event) => {
          const id = event.currentTarget.dataset.id;
          this.deleteContract(id);
        });

        this.loadingContracts = false;
      }
    },

    createContract() {
      this.$router.push({ name: 'contract-form' });
    },

    editContract(id) {
      this.$router.push({ name: 'contract-edit', params: { id: id } });
    },
    viewContract(id) {
        // console.log('Chack contract-view ID:', id);
        this.$router.push({ name: 'contract-view', params: { id: id } });
      },

    printContract(id) {
      // Realizamos un PUT a la acción personalizada para marcar el contrato como impreso
      axios.put(`/api/contract/${id}/mark-printed/`)
        .then(() => {
          // Después de marcar como impreso, actualizamos la lista local de contratos
          const contractIndex = this.contracts.findIndex(contract => contract.id === id);
          if (contractIndex !== -1) {
            // Actualizar el contrato en la lista local
            this.contracts[contractIndex].needs_reprint = false;
            // Actualizar el estilo de la fila si es necesario
           this.contracts[contractIndex].rowStyle = 'table-light';  // Cambiar el color de la fila a normal
          }

          // Ahora que el contrato ha sido actualizado, descargamos el PDF
          this.downloadContract(id);

          // Volver a inicializar DataTable con los nuevos datos (si es necesario)
          this.$nextTick(() => {
            this.initDataTable();
          });
        })
        .catch(error => {
          console.error('Error updating needs_reprint:', error);
        });
    },

    deleteContract(id) {
      Swal.fire({
        title: "Are you sure?",
        text: `This contract ${id} will be permanently deleted.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
      }).then((result) => {
        if (result.isConfirmed) {
          axios.delete(`/api/contract/${id}/`)
            .then(() => {
              console.log('Contract deleted successfully');

              // Destruir DataTable antes de actualizar los contratos
              if ($.fn.DataTable.isDataTable(this.$refs.contractsTable)) {
                $(this.$refs.contractsTable).DataTable().destroy();
              }

              // Filtrar la lista de contratos para remover el eliminado
              this.contracts = this.contracts.filter(contract => contract.id !== id);

              // Volver a inicializar DataTable con los nuevos datos
              this.$nextTick(() => {
                this.initDataTable();
              });

              // Mostrar confirmación de eliminación exitosa
              this.notifyToastSuccess('The contract has been deleted.');
            })
            .catch(error => {
              console.error('Error deleting contract:', error);
              Swal.fire({
                title: "Error",
                text: "There was a problem deleting the contract.",
                icon: "error"
              });
            });
        }
      });
    },

    truncateText(text, length) {
      if (text.length <= length) {
        return text;
      }
      return text.substring(0, length) + '...';
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return date.toLocaleDateString('en-EN', options);
    }
  }
};
</script>

<style scoped>
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
