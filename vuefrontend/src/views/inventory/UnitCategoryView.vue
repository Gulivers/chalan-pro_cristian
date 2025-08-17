<template>
    <div class="card shadow mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h6 class="text-primary mb-0">Unit Categories</h6>
        <button class="btn btn-success" @click="goToCreateForm">
          <strong>+</strong> New Category
        </button>
      </div>
  
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          Loading Unit Categories...
          <div class="spinner-border" role="status"></div>
        </div>
  
        <div v-else-if="items.length" class="table-responsive">
          <table class="table table-striped table-hover table-bordered" id="unitCategoryTable" ref="unitCategoryTable">
            <thead>
              <tr>
                <th>ID</th>
                <th v-for="field in headers" :key="field">
                  {{ schema[field]?.label || field }}
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.id">
                <td>{{ item.id }}</td>
                <td v-for="field in headers" :key="field">
                  <template v-if="typeof item[field] === 'boolean'">
                    <span :class="['badge', item[field] ? 'bg-success' : 'bg-secondary']">
                      {{ item[field] ? 'Active' : 'Inactive' }}
                    </span>
                  </template>
                  <template v-else>
                    {{ item[field] || '—' }}
                  </template>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-success" @click="viewItem(item.id)">View</button>
                    <button class="btn btn-outline-primary" @click="editItem(item.id)">Edit</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div v-else class="text-muted text-center">No categories available.</div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "UnitCategoryView",
    data() {
      return {
        schema: {},
        items: [],
        headers: [],
        loading: false,
        dataTable: null,
      };
    },
    mounted() {
      this.fetchSchema();
      this.fetchItems();
    },
    beforeUnmount() {
      // Limpiar DataTable antes de desmontar el componente
      this.destroyDataTable();
    },
    methods: {
      fetchSchema() {
        axios.get("/api/schema/unitcategory/")
          .then(res => {
            this.schema = res.data || {};
            this.headers = Object.keys(this.schema);
          })
          .catch(err => {
            console.error("❌ Error fetching schema:", err);
          });
      },
      fetchItems() {
        this.loading = true;
        axios.get("/api/unitcategory/")
          .then(res => {
            this.items = res.data;
            this.loading = false;
            // Usar setTimeout para asegurar que el DOM esté completamente renderizado
            setTimeout(() => {
              if (this.items.length && this.$refs.unitCategoryTable) {
                this.initDataTable();
              }
            }, 100);
          })
          .catch(() => {
            this.loading = false;
            console.error("❌ Error fetching categories");
          });
      },
      destroyDataTable() {
        if (this.dataTable && $.fn.dataTable && $.fn.dataTable.isDataTable(this.$refs.unitCategoryTable)) {
          try {
            this.dataTable.destroy();
            this.dataTable = null;
          } catch (error) {
            console.warn('Error destroying DataTable:', error);
          }
        }
      },
      initDataTable() {
        const table = this.$refs.unitCategoryTable;
        if (!table || !$.fn.dataTable) {
          return;
        }

        try {
          // Destruir DataTable existente si existe
          this.destroyDataTable();

          // Inicializar nuevo DataTable
          this.dataTable = $(table).DataTable({
            destroy: true,
            responsive: true,
            pageLength: 50,
            order: [[0, "desc"]],
            language: {
              search: "Search:",
            },
          });
        } catch (error) {
          console.error('Error initializing DataTable:', error);
        }
      },
      goToCreateForm() {
        this.$router.push({ name: "unit-category-form" });
      },
      viewItem(id) {
        this.$router.push({ name: "unit-category-view", params: { id } });
      },
      editItem(id) {
        this.$router.push({ name: "unit-category-edit", params: { id } });
      },
    },
  };
  </script>
  