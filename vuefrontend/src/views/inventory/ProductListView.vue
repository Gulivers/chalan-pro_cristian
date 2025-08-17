<template>
  <div class="card shadow mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h6 class="text-primary mb-0">Products</h6>
      <button class="btn btn-success" @click="goToCreateForm">
        <strong>+</strong>
        New Product
      </button>
    </div>

    <div class="card-body">
      <div v-if="loading" class="text-center py-3">
        Loading Products...
        <div class="spinner-border" role="status"></div>
      </div>

      <div v-else-if="items.length" class="table-responsive">
        <table class="table table-bordered table-striped table-hover" id="productTable" ref="productTable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>SKU</th>
              <th>Category</th>
              <th>Brand</th>
              <th>Reorder Level</th>
              <th>Default Unit</th>
              <th class="text-center">Active</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.sku }}</td>
              <td>{{ item.category_name || '—' }}</td>
              <td>{{ item.brand_name || '—' }}</td>
              <td>{{ item.reorder_level }}</td>
              <td>{{ item.unit_name || '—' }}</td>
              <td class="text-center">
                <span class="badge" :class="item.is_active ? 'bg-success' : 'bg-secondary'">
                  {{ item.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="text-center">
                <div class="btn-group btn-group-sm">
                  <button
                    v-if="this.hasPermission('appinventory.view_product')"
                    class="btn btn-outline-success"
                    @click="viewItem(item.id)">
                    View
                  </button>
                  <button
                    v-if="this.hasPermission('appinventory.change_product')"
                    class="btn btn-outline-primary"
                    @click="editItem(item.id)">
                    Edit
                  </button>
                  <button
                    v-if="this.hasPermission('appinventory.delete_product')"
                    class="btn btn-outline-danger"
                    @click="deleteItem(item.id)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-muted text-center">No products found.</div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Swal from 'sweetalert2';

  export default {
    name: 'ProductListView',
    data() {
      return {
        items: [],
        loading: false,
      };
    },
    mounted() {
      this.fetchProducts();
    },
    beforeUnmount() {
      const table = this.$refs.productTable;
      if (table && $.fn.dataTable && $.fn.dataTable.isDataTable(table)) {
        $(table).DataTable().destroy();
      }
    },
    methods: {
      fetchProducts() {
        this.loading = true;
        axios
          .get('/api/products/')
          .then(res => {
            this.items = res.data;
            this.loading = false;
            this.$nextTick(() => {
              if (this.items.length && this.$refs.productTable) {
                this.initDataTable();
              }
            });
          })
          .catch(err => {
            this.loading = false;
            this.notifyError('Failed to load products.');
            console.error('Fetch error:', err);
          });
      },
      initDataTable() {
        const table = this.$refs.productTable;
        if (table && $.fn.dataTable) {
          const $table = $(table);
          if ($.fn.dataTable.isDataTable(table)) {
            $table.DataTable().destroy();
          }
          setTimeout(() => {
            $table.DataTable({
              responsive: true,
              pageLength: 50,
              order: [[0, 'desc']],
              language: {
                search: 'Search:',
              },
            });
          }, 50);
        }
      },
      goToCreateForm() {
        this.$router.push({ name: 'product-form' });
      },
      viewItem(id) {
        this.$router.push({ name: 'product-view', params: { id } });
      },
      editItem(id) {
        this.$router.push({ name: 'product-edit', params: { id } });
      },
      confirmDelete(id) {
        this.deleteItem(id);
      },

      async deleteItem(id) {
        const result = await Swal.fire({
          title: 'Are you sure?',
          text: `This product ${id} will be permanently deleted.`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Yes, delete it!',
        });

        if (!result.isConfirmed) return;

        try {
          await axios.delete(`/api/products/${id}/`);

          // Destruir DataTable si está activo
          const table = this.$refs.productTable;
          if (table && $.fn.dataTable.isDataTable(table)) {
            $(table).DataTable().destroy();
          }

          // Filtrar el producto eliminado
          this.items = this.items.filter(item => item.id !== id);

          // Reiniciar DataTable
          this.$nextTick(() => {
            if (this.items.length && this.$refs.productTable) {
              $(this.$refs.productTable).DataTable({
                responsive: true,
                pageLength: 50,
                order: [[0, 'desc']],
                language: {
                  search: 'Search:',
                },
              });
            }
          });

          // Mostrar notificación
          this.notifyToastSuccess('The product has been deleted.');
        } catch (err) {
          console.error('Delete failed:', err);
          Swal.fire({
            title: 'Error',
            text: 'There was a problem deleting the product.',
            icon: 'error',
          });
        }
      },
    },
  };
</script>
