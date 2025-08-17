<template>
    <div class="card shadow mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h6 class="text-primary mb-0">Unit of Measure</h6>
        <button class="btn btn-success" @click="goToCreateForm">
          <strong>+</strong> New Unit
        </button>
      </div>
  
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          Loading Units...
          <div class="spinner-border" role="status"></div>
        </div>
  
        <div v-else-if="items.length" class="table-responsive">
          <table class="table table-striped table-hover table-bordered" id="unitTable" ref="unitTable">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Code</th>
                <th>Category</th>
                <th class="text-center">Ref. Unit</th>
                <th class="text-center">Sign</th>
                <th>Factor</th>
                <th class="text-center">Active</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.id">
                <td>{{ item.id }}</td>
                <td class="text-start">{{ item.name }}</td>
                <td class="text-start">{{ item.code }}</td>
                <td class="text-start">{{ item.category_name || "N/A" }}</td>
                <td class="text-center">{{ item.reference_unit ? "✔" : "✖" }}</td>
                <td class="text-center">{{ item.conversion_sign }}</td>
                <td>{{ item.conversion_factor }}</td>
                <td class="text-center">
                  <span class="badge" :class="item.is_active ? 'bg-success' : 'bg-secondary'">
                    {{ item.is_active ? "Active" : "Inactive" }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-success" @click="viewItem(item.id)">View</button>
                    <button class="btn btn-outline-primary" @click="editItem(item.id)">Edit</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div v-else class="text-muted text-center">No units available.</div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "UnitOfMeasureView",
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
      this.destroyDataTable();
    },
    methods: {
      fetchSchema() {
        axios
          .get("/api/schema/unitofmeasure/")
          .then((res) => {
            this.schema = res.data || {};
            this.headers = Object.keys(this.schema);
          })
          .catch((err) => {
            console.error("Error fetching schema:", err);
          });
      },
      fetchItems() {
        this.loading = true;
        axios
          .get("/api/unitsofmeasure/")
          .then((res) => {
            this.items = res.data;
            this.loading = false;
            setTimeout(() => {
              if (this.items.length && this.$refs.unitTable) {
                this.initDataTable();
              }
            }, 100);
          })
          .catch((err) => {
            this.loading = false;
            console.error("Error fetching items:", err);
          });
      },
      destroyDataTable() {
        if (this.dataTable && $.fn.dataTable && $.fn.dataTable.isDataTable(this.$refs.unitTable)) {
          try {
            this.dataTable.destroy();
            this.dataTable = null;
          } catch (error) {
            console.warn('Error destroying DataTable:', error);
          }
        }
      },
      initDataTable() {
        const table = this.$refs.unitTable;
        if (!table || !$.fn.dataTable) {
          return;
        }

        try {
          this.destroyDataTable();

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
        this.$router.push({ name: "unit-measure-form" });
      },
      viewItem(id) {
        this.$router.push({ name: "unit-measure-view", params: { id } });
      },
      editItem(id) {
        this.$router.push({ name: "unit-measure-edit", params: { id } });
      },
    },
  };
  </script>
  