<template>
  <div class="container">
    <h3 class="card-title-orange pt-3">
      <p>Warehouse Manager</p>
    </h3>

    <div class="card shadow mb-4">
      <div class="card-header py-2">
        <h6 class="ms-1 font-weight-bold text-primary">
          {{ isReadOnly ? 'View Warehouse' : isEdit ? 'Edit Warehouse' : 'Create Warehouse' }}
        </h6>
      </div>

      <div class="card-body">
        <div class="row">
          <!-- Name & Active switch -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Name</label>
            <input
              v-model="warehouse.name"
              type="text"
              class="form-control"
              placeholder="Warehouse Name"
              :readonly="isReadOnly" />

            <div class="form-check form-switch mt-3 d-flex align-items-center gap-2">
              <input
                class="form-check-input"
                type="checkbox"
                role="switch"
                id="isActiveCheck"
                v-model="warehouse.is_active"
                :disabled="isReadOnly" />
              <label class="form-check-label mb-0" for="isActiveCheck">Active</label>
            </div>
          </div>

          <!-- Location -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Location</label>
            <input
              v-model="warehouse.location"
              type="text"
              class="form-control"
              placeholder="Warehouse Location"
              :readonly="isReadOnly" />
          </div>
        </div>

        <div class="row mt-4">
          <div class="col" v-if="!isReadOnly">
            <button class="btn btn-primary" @click="saveWarehouse">
              {{ isEdit ? 'Update' : 'Create' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        warehouse: {
          name: '',
          location: '',
          is_active: true,
        },
        isEdit: false,
      };
    },
    computed: {
      isReadOnly() {
        return this.$route.name === 'warehouse-view';
      },
    },
    mounted() {
      const id = this.$route.params.id;
      if (id) {
        this.isEdit = true;
        axios
          .get(`/api/warehouses/${id}/`)
          .then(res => (this.warehouse = res.data))
          .catch(err => console.error('Error fetching warehouse:', err));
      }
    },
    methods: {
      saveWarehouse() {
        const id = this.$route.params.id;
        const url = id ? `/api/warehouses/${id}/` : '/api/warehouses/';
        const method = id ? 'put' : 'post';

        axios[method](url, this.warehouse)
          .then(() => this.$router.push('/warehouses'))
          .catch(err => console.error('Error saving warehouse:', err));
      },
    },
  };
</script>
