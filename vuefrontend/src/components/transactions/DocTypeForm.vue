<template>
  <div class="container mt-4">
    <!-- Main Title -->
    <div class="text-center">
      <h3 class="text-warning">Transaction Types</h3>
    </div>

    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-center align-items-center">
        <h5 class="mb-0 text-center">
          <i class="fas fa-file-alt me-2"></i>
          {{ isViewMode ? 'View Document Type' : (isEditMode ? 'Edit Document Type' : 'New Document Type') }}
        </h5>
      </div>

      <div class="card-body p-4">
        <form @submit.prevent="handleSubmit">
          <!-- Basic Information -->
          <div class="row mb-4">
            <div class="col-12">
              <h6 class="text-warning border-bottom pb-2 mb-3">
                <i class="fas fa-info-circle me-2"></i>
                Basic Information
              </h6>
            </div>
            <div class="col-md-6 mb-3">
              <div class="row">
                <div class="col-md-4">
                  <label for="type_code" class="form-label">
                    Type Code
                    <span class="text-danger">*</span>
                  </label>
                </div>
                <div class="col-md-8">
                  <input
                    id="type_code"
                    v-model="form.type_code"
                    type="text"
                    class="form-control"
                    placeholder="Ex: INCOME, SUPRET"
                    required
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Unique code to identify the document type" />
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="row">
                <div class="col-md-4">
                  <label for="description" class="form-label fw-bold">
                    Description
                    <span class="text-danger">*</span>
                  </label>
                </div>
                <div class="col-md-8">
                  <input
                    id="description"
                    v-model="form.description"
                    type="text"
                    class="form-control"
                    placeholder="Document type description"
                    required
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Descriptive name for the document type" />
                </div>
              </div>
            </div>
          </div>

          <!-- Inventory Configuration -->
          <div class="row mb-4">
            <div class="col-12">
              <h6 class="text-warning border-bottom pb-2 mb-3">
                <i class="fas fa-boxes me-2"></i>
                Inventory Configuration
              </h6>
            </div>
            <div class="col-md-4 mb-3">
              <label for="stock_movement" class="form-label">Stock Movement</label>
              <select 
                id="stock_movement" 
                v-model="form.stock_movement" 
                class="form-select"
                :disabled="isViewMode || submitting"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Defines how it affects inventory">
                <option :value="1">+1 Entry</option>
                <option :value="-1">-1 Exit</option>
                <option :value="0">0 Neutral</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label fw-bold">Affects Inventory</label>
              <div class="d-flex flex-column gap-3">
                <div class="form-check form-switch">
                  <input
                    id="affects_physical"
                    v-model="form.affects_physical"
                    class="form-check-input"
                    type="checkbox"
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Affects physical inventory count" />
                  <label class="form-check-label" for="affects_physical">Physical Inventory</label>
                </div>
                <div class="form-check form-switch">
                  <input 
                    id="affects_logical" 
                    v-model="form.affects_logical" 
                    class="form-check-input" 
                    type="checkbox"
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Affects logical inventory tracking" />
                  <label class="form-check-label" for="affects_logical">Logical Inventory</label>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label fw-bold">Additional Configuration</label>
              <div class="d-flex flex-column gap-3">
                <div class="form-check form-switch">
                  <input
                    id="affects_accounting"
                    v-model="form.affects_accounting"
                    class="form-check-input"
                    type="checkbox"
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Affects accounting records and financial reports" />
                  <label class="form-check-label" for="affects_accounting">Affects Accounting</label>
                </div>
                <div class="form-check form-switch">
                  <input
                    id="warehouse_required"
                    v-model="form.warehouse_required"
                    class="form-check-input"
                    type="checkbox"
                    :disabled="isViewMode || submitting"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Requires warehouse selection for this document type" />
                  <label class="form-check-label" for="warehouse_required">Warehouse Required</label>
                </div>
              </div>
            </div>
          </div>

          <!-- Business Configuration -->
          <div class="row mb-4">
            <div class="col-12">
              <h6 class="text-warning border-bottom pb-2 mb-3">
                <i class="fas fa-briefcase me-2"></i>
                Business Configuration
              </h6>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-check form-switch">
                <input
                  id="is_purchase"
                  v-model="form.is_purchase"
                  class="form-check-input"
                  type="checkbox"
                  :disabled="isViewMode || submitting"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="For transactions with suppliers" />
                <label
                  class="form-check-label"
                  for="is_purchase">
                  Purchase Document
                </label>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-check form-switch">
                <input 
                  id="is_sales" 
                  v-model="form.is_sales" 
                  class="form-check-input" 
                  type="checkbox"
                  :disabled="isViewMode || submitting"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="For transactions with customers" />
                <label class="form-check-label" for="is_sales">Sales Document</label>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-check form-switch">
                <input 
                  id="is_taxable" 
                  v-model="form.is_taxable" 
                  class="form-check-input" 
                  type="checkbox"
                  :disabled="isViewMode || submitting"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Applies taxes to the document" />
                <label class="form-check-label" for="is_taxable">Subject to Taxes</label>
              </div>
            </div>
          </div>

          <!-- Status -->
          <div class="row mb-4">
            <div class="col-12">
              <h6 class="text-warning border-bottom pb-2 mb-3">
                <i class="fas fa-toggle-on me-2"></i>
                Status
              </h6>
            </div>
            <div class="col-md-4">
              <div class="form-check form-switch">
                <input 
                  id="is_active" 
                  v-model="form.is_active" 
                  class="form-check-input" 
                  type="checkbox"
                  :disabled="isViewMode || submitting"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Allows using this type in transactions" />
                <label class="form-check-label" for="is_active">Active Document Type</label>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="row">
            <div class="col-12">
              <div class="d-flex gap-2 justify-content-center">
                <router-link to="/document-types" class="btn btn-secondary">
                  <i class="fas fa-times me-1"></i>
                  Cancel
                </router-link>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="isViewMode || submitting"
                >
                  <span
                    v-if="submitting"
                    class="spinner-border spinner-border-sm me-1"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <i v-else class="fas fa-save me-1"></i>
                  {{ isEditMode ? (submitting ? 'Updating...' : 'Update') : (submitting ? 'Creating...' : 'Create') }}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'
import '@assets/css/base.css'
import { Tooltip } from 'bootstrap'

const route = useRoute()
const router = useRouter()

const submitting = ref(false)
const id = route.query.id
const isViewMode = computed(() => route.query.mode === 'view')
const isEditMode = computed(() => !!id && !isViewMode.value)

const form = ref({
  type_code: '',
  description: '',
  affects_physical: true,
  affects_logical: true,
  affects_accounting: false,
  is_taxable: false,
  is_purchase: false,
  is_sales: false,
  warehouse_required: true,
  stock_movement: 0,
  is_active: true
})

onMounted(async () => {
  // initialize bootstrap tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(el => new Tooltip(el))

  if (id) {
    try {
      const { data } = await axios.get(`/api/document-types/${id}/`)
      form.value = data
    } catch (error) {
      console.error('Error loading data:', error)
      Swal.fire('Oops!', 'Error loading the document type.', 'error')
    }
  }
})

const handleSubmit = async () => {
  if (isViewMode.value) return
  submitting.value = true
  try {
    if (isEditMode.value) {
      await axios.put(`/api/document-types/${id}/`, form.value)
    } else {
      await axios.post('/api/document-types/', form.value)
    }
    router.push('/document-types') // éxito silencioso + redirect
  } catch (error) {
    console.error('Error saving:', error)
    const { status, data } = error?.response || {}
    if (status === 400 && data) {
      const messages = Object.entries(data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join('\n')
      await Swal.fire('Oops!', messages || 'There were validation errors.', 'error')
    } else if (status === 403) {
      await Swal.fire('Forbidden', 'You do not have permission for this action.', 'error')
    } else {
      await Swal.fire('Oops!', 'Error saving the document type.', 'error')
    }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped></style>
