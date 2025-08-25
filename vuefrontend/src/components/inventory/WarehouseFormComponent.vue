<template>
  <div class="container">
    <h3 class="card-title-orange pt-3">
      <p>Warehouse Manager</p>
    </h3>

    <div class="card shadow mb-4">
      <div class="card-header py-2">
        <h6 class="ms-1 font-weight-bold text-primary">
          {{ isViewMode ? 'View Warehouse' : isEditMode ? 'Edit Warehouse' : 'Create Warehouse' }}
        </h6>
      </div>

      <div class="card-body">
        <div class="row">
          <!-- Name & Active switch -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Name</label>
            <input
              v-model.trim="warehouse.name"
              type="text"
              class="form-control"
              placeholder="Warehouse Name"
              :readonly="isDisabled" />

            <div class="form-check form-switch mt-3 d-flex align-items-center gap-2">
              <input
                class="form-check-input"
                type="checkbox"
                role="switch"
                id="isActiveCheck"
                v-model="warehouse.is_active"
                :disabled="isDisabled" />
              <label class="form-check-label mb-0" for="isActiveCheck">Active</label>
            </div>
          </div>

          <!-- Location -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Location</label>
            <input
              v-model.trim="warehouse.location"
              type="text"
              class="form-control"
              placeholder="Warehouse Location"
              :readonly="isDisabled" />
          </div>
        </div>

        <div class="row mt-4">
          <div class="col-12 d-flex flex-column flex-sm-row justify-content-center align-items-center gap-2">
            <button v-if="!isViewMode" class="btn btn-primary" @click="saveWarehouse" :disabled="isDisabled">
              <span
                v-if="submitting"
                class="spinner-border spinner-border-sm me-1"
                role="status"
                aria-hidden="true"></span>
              <i v-else class="fas fa-save me-1"></i>
              {{ isEditMode ? (submitting ? 'Updating...' : 'Update') : submitting ? 'Creating...' : 'Create' }}
            </button>

            <button type="button" class="btn btn-secondary" @click="goBack" :disabled="submitting">Back</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Swal from 'sweetalert2';

  export default {
    name: 'WarehouseForm',
    data() {
      return {
        warehouse: {
          name: '',
          location: '',
          is_active: true,
        },
        submitting: false,
      };
    },
    computed: {
      id() {
        return this.$route.params.id;
      },
      isViewMode() {
        // soporta ruta dedicada y (por si acaso) query ?mode=view
        return this.$route.name === 'warehouse-view' || this.$route.query.mode === 'view';
      },
      isEditMode() {
        return !!this.id && !this.isViewMode;
      },
      isDisabled() {
        return this.isViewMode || this.submitting;
      },
    },
    mounted() {
      if (this.id) this.loadWarehouse();
    },
    methods: {
      async loadWarehouse() {
        try {
          const { data } = await axios.get(`/api/warehouses/${this.id}/`);
          this.warehouse = {
            name: data.name ?? '',
            location: data.location ?? '',
            is_active: !!data.is_active,
          };
        } catch (error) {
          console.error('Error fetching warehouse:', error);
          await Swal.fire('Oops!', 'Error loading the warehouse.', 'error');
        }
      },

      async saveWarehouse() {
        if (this.isViewMode) return;
        // Validación mínima local
        if (!this.warehouse.name?.trim()) {
          await Swal.fire('Validation', 'Name is required.', 'warning');
          return;
        }

        this.submitting = true;
        const url = this.id ? `/api/warehouses/${this.id}/` : '/api/warehouses/';
        const method = this.id ? 'put' : 'post';

        try {
          await axios[method](url, this.warehouse);
          this.$router.push('/warehouses'); // éxito silencioso + redirect
        } catch (error) {
          console.error('Error saving warehouse:', error);
          const { status, data } = error?.response || {};
          if (status === 400 && data) {
            const messages = Object.entries(data)
              .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
              .join('\n');
            await Swal.fire('Oops!', messages || 'There were validation errors.', 'error');
          } else if (status === 403) {
            await Swal.fire('Forbidden', 'You do not have permission for this action.', 'error');
          } else {
            await Swal.fire('Oops!', 'Error saving the warehouse.', 'error');
          }
        } finally {
          this.submitting = false;
        }
      },

      goBack() {
        if (this.$router && this.$route.name) {
          this.$router.back();
        } else {
          this.$router.push('/warehouses');
        }
      },
    },
  };
</script>
