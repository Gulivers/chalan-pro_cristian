<!-- vuefrontend/src/views/inventory/WarehouseListView.vue -->
<template>
    <div class="card shadow mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h6 class="text-primary mb-0">Warehouse List</h6>
        <button class="btn btn-success ml-auto" @click="createWarehouse">
          <strong>+</strong> New Warehouse
        </button>
      </div>
  
      <div class="card-body">
        <div v-if="loading" class="spinner-container text-center">
          <p>Loading Warehouses...</p>
          <div class="spinner-border text-primary" role="status"></div>
        </div>
  
        <div class="table-responsive">
          <table class="table table-striped table-hover table-bordered" ref="warehouseTable">
            <thead>
              <tr>
                <th>ID</th>
                <th scope="col">Name</th>
                <th scope="col">Location</th>
                <th scope="col">Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody v-show="!loading">
              <tr v-for="warehouse in warehouses" :key="warehouse.id">
                <td>{{ warehouse.id }}</td>
                <td class="text-start">{{ warehouse.name }}</td>
                <td class="text-start">{{ warehouse.location }}</td>
                <td>
                  <span class="badge bg-success" v-if="warehouse.is_active">Active</span>
                  <span class="badge bg-secondary" v-else>Inactive</span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-success" @click="viewWarehouse(warehouse.id)">View</button>
                    <button class="btn btn-outline-primary" @click="editWarehouse(warehouse.id)">Edit</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'WarehouseListView',
    data() {
      return {
        loading: false,
        warehouses: []
      };
    },
    mounted() {
      this.fetchWarehouses();
    },
    methods: {
      fetchWarehouses() {
        this.loading = true;
        axios.get('/api/warehouses/')
          .then(res => {
            this.warehouses = res.data;
            this.$nextTick(this.initDataTable);
          })
          .finally(() => {
            this.loading = false;
          });
      },
      initDataTable() {
        if (this.$refs.warehouseTable && $.fn.DataTable) {
          if ($.fn.DataTable.isDataTable(this.$refs.warehouseTable)) {
            $(this.$refs.warehouseTable).DataTable().destroy();
          }
  
          $(this.$refs.warehouseTable).DataTable({
            destroy: true,
            responsive: true,
            pageLength: 50,
            order: [[0, 'desc']],
            language: {
              search: "Search:",
            },
          });
        }
      },
      createWarehouse() {
        this.$router.push({ name: 'warehouse-form' });
      },
      editWarehouse(id) {
        this.$router.push({ name: 'warehouse-edit', params: { id } });
      },
      viewWarehouse(id) {
        this.$router.push({ name: 'warehouse-view', params: { id } });
      }
    }
  };
  </script>
  
  <style scoped>
  .spinner-container {
    padding: 2rem;
  }
  </style>
  