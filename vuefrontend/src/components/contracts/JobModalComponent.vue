<template>
  <div class="modal fade" ref="modalElement" :id="id" tabindex="-1" role="dialog" aria-labelledby="jobModalLabel"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="jobModalLabel">
            {{ action === 'edit' ? 'Edit Community (Job)' : 'Add Community (Job)' }}
          </h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="saveJob">
            <!-- Name Field -->
            <div class="mb-3">
              <label for="jobName" class="form-label">Name</label>
              <input type="text" id="jobName" v-model="modalJob.name" class="form-control"
                :class="{ 'is-invalid': error.name }" placeholder="Enter community name" @input="clearError('name')"
                required />
              <div v-if="error.name" class="text-danger mt-1">Please provide a community name.</div>
            </div>

            <!-- Builder Field -->
            <div class="mb-3">
              <label for="builder" class="form-label">Builder</label>
              <v-select :options="builders" v-model="modalJob.builder" :reduce="builder => builder.id" label="name"
                placeholder="Select Builder" :class="{ 'is-invalid': error.builder }" @input="clearError('builder')"
                required />
              <div v-if="error.builder" class="text-danger mt-1">Please select a builder.</div>
            </div>

            <!-- Address Field -->
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <input type="text" id="address" v-model="modalJob.address" class="form-control"
                placeholder="Enter address" @input="fetchCoordinates" />
            </div>

            <!-- Latitude Field -->
            <div class="mb-3">
              <label for="latitude" class="form-label">Latitude</label>
              <input type="number" step="0.000001" id="latitude" v-model="modalJob.latitude" class="form-control"
                placeholder="Latitude (Optional)" />
            </div>

            <!-- Longitude Field -->
            <div class="mb-3">
              <label for="longitude" class="form-label">Longitude</label>
              <input type="number" step="0.000001" id="longitude" v-model="modalJob.longitude" class="form-control"
                placeholder="Longitude (Optional)" />
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="saveJob">
            {{ action === 'edit' ? 'Update' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

export default {
  components: {
    vSelect,
  },
  props: {
    id: String,
    action: String,
    job: {
      type: Object,
      default: () => ({
        name: "",
        builder: null,
        address: "",
        latitude: null,
        longitude: null,
      }),
    },
    builders: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      modalJob: {
        name: "",
        builder: null,
        address: "",
        latitude: null,
        longitude: null,
      },
      modalInstance: null,
      error: {
        name: false,
        builder: false,
      },
    };
  },
  watch: {
    job: {
      handler(newJob) {
        if (newJob) {
          this.modalJob.name = newJob.name || "";
          this.modalJob.builder = newJob.builder || null;
          this.modalJob.address = newJob.address || "";
          this.modalJob.latitude = newJob.latitude !== null ? newJob.latitude : null;
          this.modalJob.longitude = newJob.longitude !== null ? newJob.longitude : null;
        }
      },
      immediate: true,
      deep: true,
    },
  },
  mounted() {
    if (this.$refs.modalElement) {
      this.modalInstance = Modal.getOrCreateInstance(this.$refs.modalElement);
    } else {
      console.error("Modal element not found in JobModalComponent");
    }
  },
  methods: {
    validateFields() {
      let isValid = true;

      if (!this.modalJob.name || this.modalJob.name.trim() === "") {
        this.error.name = true;
        isValid = false;
      } else {
        this.error.name = false;
      }

      if (!this.modalJob.builder) {
        this.error.builder = true;
        isValid = false;
      } else {
        this.error.builder = false;
      }

      return isValid;
    },

    clearError(field) {
      this.error[field] = false;
    },
    async saveJob() {
      if (!this.validateFields()) {
        return;
      }

      try {
        const jobData = {
          name: this.modalJob.name,
          builder: this.modalJob.builder,
          address: this.modalJob.address,
          latitude: this.modalJob.latitude || null,
          longitude: this.modalJob.longitude || null,
        };

        if (this.action === "edit") {
          await axios.put(`/api/job/${this.modalJob.id}/`, jobData);
        } else {
          await axios.post("/api/job/", jobData);
        }

        this.$emit("refresh");
        this.$emit("saved", jobData);
        if (this.action !== "edit") {
          this.$emit("clearJobSelect");
        }
        this.closeModal();
      } catch (error) {
        console.error("Error saving job:", error.response?.data || error.message);
      }
    },

    async fetchCoordinates() {
      if (!this.modalJob.address || this.modalJob.address.length < 5) return;

      try {
        const response = await axios.get("https://nominatim.openstreetmap.org/search", {
          params: {
            q: this.modalJob.address,
            format: "json",
            addressdetails: 1,
          },
          headers: { "User-Agent": "chalan-pro-app" },
        });

        if (response.data.length > 0) {
          const location = response.data[0];
          this.modalJob.latitude = parseFloat(location.lat) || null;
          this.modalJob.longitude = parseFloat(location.lon) || null;
        }
      } catch (error) {
        console.error("Error fetching coordinates:", error);
      }
    },


    showModal() {
      if (this.modalInstance) this.modalInstance.show();
    },
    hideModal() {
      if (this.modalInstance) this.modalInstance.hide();
    },
    closeModal() {
      this.hideModal();
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.text-danger {
  color: red;
  font-size: 0.875rem;
}

.is-invalid {
  border-color: red !important;
  box-shadow: 0 0 5px red !important;
}
</style>
