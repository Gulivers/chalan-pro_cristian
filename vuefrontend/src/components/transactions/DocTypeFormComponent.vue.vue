<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">{{ isEditMode ? 'Edit Document Type' : 'New Document Type' }}</h5>
        <router-link to="/document-types" class="btn btn-secondary btn-sm">Back to list</router-link>
      </div>

      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Code *</label>
              <input v-model="form.type_code" type="text" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Description *</label>
              <input v-model="form.description" type="text" class="form-control" required />
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-4">
              <label class="form-label">Stock Movement</label>
              <select v-model="form.stock_movement" class="form-select">
                <option :value="1">+1 Entrada</option>
                <option :value="-1">-1 Salida</option>
                <option :value="0">0 Neutro</option>
              </select>
            </div>
            <div class="col-md-4 d-flex align-items-center">
              <div class="form-check form-switch me-3">
                <input v-model="form.affects_physical" class="form-check-input" type="checkbox" />
                <label class="form-check-label">Affects Physical</label>
              </div>
              <div class="form-check form-switch">
                <input v-model="form.affects_logical" class="form-check-input" type="checkbox" />
                <label class="form-check-label">Affects Logical</label>
              </div>
            </div>
            <div class="col-md-4 d-flex align-items-center">
              <div class="form-check form-switch me-3">
                <input v-model="form.affects_accounting" class="form-check-input" type="checkbox" />
                <label class="form-check-label">Accounting</label>
              </div>
              <div class="form-check form-switch">
                <input v-model="form.warehouse_required" class="form-check-input" type="checkbox" />
                <label class="form-check-label">Warehouse Req.</label>
              </div>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-4 form-check form-switch">
              <input v-model="form.is_purchase" class="form-check-input" type="checkbox" />
              <label class="form-check-label">Purchase</label>
            </div>
            <div class="col-md-4 form-check form-switch">
              <input v-model="form.is_sales" class="form-check-input" type="checkbox" />
              <label class="form-check-label">Sales</label>
            </div>
            <div class="col-md-4 form-check form-switch">
              <input v-model="form.is_taxable" class="form-check-input" type="checkbox" />
              <label class="form-check-label">Taxable</label>
            </div>
          </div>

          <div class="form-check form-switch mb-4">
            <input v-model="form.is_active" class="form-check-input" type="checkbox" />
            <label class="form-check-label">Active</label>
          </div>

          <button type="submit" class="btn btn-primary">
            {{ isEditMode ? 'Update' : 'Create' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const isEditMode = ref(false)
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

const id = route.query.id

onMounted(async () => {
  if (id) {
    isEditMode.value = true
    try {
      const { data } = await axios.get(`/api/document-types/${id}/`)
      form.value = data
    } catch (error) {
      console.error('Error loading data:', error)
      alert('Error loading the document type.')
    }
  }
})

const handleSubmit = async () => {
  try {
    if (isEditMode.value) {
      await axios.put(`/api/document-types/${id}/`, form.value)
    } else {
      await axios.post('/api/document-types/', form.value)
    }
    router.push('/document-types')
  } catch (error) {
    console.error('Error saving:', error)
    alert('Error saving the document type.')
  }
}
</script>

<style scoped>
label {
  font-weight: 500;
}
</style>
