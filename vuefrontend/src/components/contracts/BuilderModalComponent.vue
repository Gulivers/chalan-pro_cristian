<template>
  <div class="modal fade" ref="modalElement" :id="id" tabindex="-1" role="dialog" aria-labelledby="builderModalLabel"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ action === 'edit' ? 'Edit Builder' : 'Add Builder' }}
          </h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveBuilder">
            <!-- Builder Name -->
            <div class="form-group mb-3">
              <label for="builderName" class="form-label">Builder Name</label>
              <input type="text" class="form-control" id="builderName" v-model="modalBuilder.name"
                :class="{ 'is-invalid': error.name }" placeholder="Enter builder name" @input="clearError('name')"
                required />
              <div v-if="error.name" class="text-danger mt-1">Please provide a builder name.</div>
            </div>

            <!-- Trim Amount -->
            <div class="form-group mb-3">
              <label for="trimAmount" class="form-label">Trim Price SqFt</label>
              <input type="number" class="form-control" id="trimAmount" v-model="modalBuilder.trim_amount"
                placeholder="Enter trim price per SqFt" required />
            </div>

            <!-- Rough Amount -->
            <div class="form-group mb-3">
              <label for="roughAmount" class="form-label">Rough Price SqFt</label>
              <input type="number" class="form-control" id="roughAmount" v-model="modalBuilder.rough_amount"
                placeholder="Enter rough price per SqFt" required />
            </div>

            <!-- Travel Price Amount -->
            <div class="form-group mb-3">
              <label for="travelPriceAmount" class="form-label">Travel Amount</label>
              <input type="number" class="form-control" id="travelPriceAmount"
                v-model="modalBuilder.travel_price_amount" placeholder="Enter travel amount" required />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="saveBuilder">
            {{ action === 'edit' ? 'Update Builder' : 'Add Builder' }}
          </button>
          <!-- Save & Assign Prices -->
          <button v-if="action !== 'edit'" type="button" class="btn btn-success" @click="saveAndAssignPrices">
            Save & Assign Prices
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";

export default {
  props: ["id", "action", "builder"],
  data() {
    return {
      modalBuilder: { ...this.builder }, // Local reactive copy of the builder data
      modalInstance: null, // Store the Bootstrap modal instance
      error: {
        name: false,
      },
    };
  },
  watch: {
    // Watch the `builder` prop to update `modalBuilder` when prop changes
    builder: {
      handler(newBuilder) {
        this.modalBuilder = { ...newBuilder };
      },
      immediate: true,
      deep: true,
    },
  },
  mounted() {
    if (this.$refs.modalElement) {
      this.modalInstance = Modal.getOrCreateInstance(this.$refs.modalElement);
    }
  },
  methods: {
    validateFields() {
      let isValid = true;

      // Validate Name
      if (!this.modalBuilder.name || this.modalBuilder.name.trim() === "") {
        this.error.name = true;
        isValid = false;
      } else {
        this.error.name = false;
      }

      return isValid;
    },
    clearError(field) {
      this.error[field] = false;
    },

    async saveBuilder() {
      if (!this.validateFields()) {
        return;
      }

      try {
        // Use `modalBuilder` instead of `builder` for the API call
        if (this.action === "edit") {
          await axios.put(`/api/builder/${this.modalBuilder.id}/`, this.modalBuilder);
        } else {
          await axios.post("/api/builder/", this.modalBuilder);
        }
        this.$emit("refresh"); // Emit event to refresh list in parent
        this.$emit("saved", this.modalBuilder);
        if (this.action !== "edit") {
          this.$emit("clearBuilderSelect");
        }
        this.closeModal();
      } catch (error) {
        console.error(error);
      }
    },

    async saveAndAssignPrices() {
      if (!this.validateFields()) {
        return;
      }
      try {
        const response = await axios.post("/api/builder/", this.modalBuilder);
        const newBuilderId = response.data.id;

        this.$emit("refresh");
        this.$emit("saved", this.modalBuilder);
        this.$emit("clearBuilderSelect");

        // Open the "Work Prices per Builder" page in a new tab with the new builder's ID
        window.open(`/work-prices-builders?builder=${newBuilderId}`, "_blank");

        this.closeModal();
      } catch (error) {
        console.error(error);
      }
    },

    showModal() {
      if (this.modalInstance) {
        this.modalInstance.show();
      }
    },
    hideModal() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
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
