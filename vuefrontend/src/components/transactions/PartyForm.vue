<template>
  <div class="container my-3">
    <div class="card shadow-sm">
      <div class="card-header d-flex align-items-center justify-content-between">
        <h5 class="mb-0">{{ title }}</h5>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary btn-sm" @click="() => router.back()">
            <i class="fas fa-arrow-left me-1"></i>
            Back
          </button>
          <button class="btn btn-outline-dark btn-sm" @click="redirectToList">
            <i class="fas fa-list me-1"></i>
            List
          </button>
        </div>
      </div>

      <div class="card-body">
        <div v-if="loading" class="text-muted">Loading...</div>

        <form v-else @submit.prevent="handleSubmit" novalidate>
          <!-- non_field_errors -->
          <div v-if="serverErrors.non_field_errors" class="alert alert-warning py-2">
            <ul class="mb-0">
              <li v-for="(msg, i) in serverErrors.non_field_errors" :key="'warn-' + i">{{ msg }}</li>
            </ul>
          </div>

          <div class="row g-3">
            <!-- Name -->
            <div class="col-md-6">
              <label class="form-label">
                Name
                <span class="text-danger">*</span>
              </label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.name }"
                v-model="form.name"
                :readonly="isViewMode"
                maxlength="255"
                autocomplete="off"
                required />
              <div v-if="serverErrors.name" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.name" :key="'name-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- RFC -->
            <div class="col-md-6">
              <label class="form-label">RFC</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.rfc }"
                v-model="form.rfc"
                :readonly="isViewMode"
                maxlength="50"
                autocomplete="off" />
              <div v-if="serverErrors.rfc" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.rfc" :key="'rfc-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Street -->
            <div class="col-md-6">
              <label class="form-label">Street</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.street }"
                v-model="form.street"
                :readonly="isViewMode"
                maxlength="100"
                autocomplete="off" />
              <div v-if="serverErrors.street" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.street" :key="'street-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Floor/Office -->
            <div class="col-md-6">
              <label class="form-label">Floor/Office</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.floor_office }"
                v-model="form.floor_office"
                :readonly="isViewMode"
                maxlength="100"
                autocomplete="off" />
              <div v-if="serverErrors.floor_office" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.floor_office" :key="'fo-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- City -->
            <div class="col-md-4">
              <label class="form-label">City</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.city }"
                v-model="form.city"
                :readonly="isViewMode"
                maxlength="100"
                autocomplete="off" />
              <div v-if="serverErrors.city" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.city" :key="'city-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- State -->
            <div class="col-md-4">
              <label class="form-label">State</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.state }"
                v-model="form.state"
                :readonly="isViewMode"
                maxlength="100"
                autocomplete="off" />
              <div v-if="serverErrors.state" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.state" :key="'state-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Zip Code -->
            <div class="col-md-4">
              <label class="form-label">Zip Code</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.zipcode }"
                v-model="form.zipcode"
                :readonly="isViewMode"
                maxlength="20"
                autocomplete="off" />
              <div v-if="serverErrors.zipcode" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.zipcode" :key="'zip-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Country -->
            <div class="col-md-6">
              <label class="form-label">Country</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.country }"
                v-model="form.country"
                :readonly="isViewMode"
                maxlength="100"
                autocomplete="off" />
              <div v-if="serverErrors.country" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.country" :key="'country-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Phone -->
            <div class="col-md-6">
              <label class="form-label">Phone</label>
              <input
                type="text"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.phone }"
                v-model="form.phone"
                :readonly="isViewMode"
                maxlength="20"
                autocomplete="off" />
              <div v-if="serverErrors.phone" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.phone" :key="'phone-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Email -->
            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.email }"
                v-model="form.email"
                :readonly="isViewMode"
                maxlength="255"
                autocomplete="off" />
              <div v-if="serverErrors.email" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.email" :key="'email-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Types (M2M) -->
            <div class="col-md-6">
              <label class="form-label">Types</label>
              <v-select
                :options="options.types"
                label="name"
                :reduce="o => o.id"
                v-model="form.types"
                :disabled="isViewMode"
                multiple
                :class="{ 'is-invalid': serverErrors.types }"
                placeholder="Select one or more types"
                :close-on-select="false"
                :clearable="true" />
              <div v-if="serverErrors.types" class="invalid-feedback d-block">
                <div v-for="(msg, idx) in serverErrors.types" :key="'types-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Category (FK) -->
            <div class="col-md-6">
              <label class="form-label">Category</label>
              <v-select
                :options="options.categories"
                label="name"
                :reduce="o => o.id"
                v-model="form.category"
                :disabled="isViewMode"
                :class="{ 'is-invalid': serverErrors.category }"
                placeholder="Select a category"
                :clearable="true" />
              <div v-if="serverErrors.category" class="invalid-feedback d-block">
                <div v-for="(msg, idx) in serverErrors.category" :key="'cat-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Default Price Type (FK) -->
            <div class="col-md-6">
              <label class="form-label">Default Price Type</label>
              <v-select
                :options="options.priceTypes"
                label="name"
                :reduce="o => o.id"
                v-model="form.default_price_type"
                :disabled="isViewMode"
                :class="{ 'is-invalid': serverErrors.default_price_type }"
                placeholder="Select a price type"
                :clearable="true" />
              <div v-if="serverErrors.default_price_type" class="invalid-feedback d-block">
                <div v-for="(msg, idx) in serverErrors.default_price_type" :key="'pt-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Ranks -->
            <div class="col-md-3">
              <label class="form-label">Customer Rank</label>
              <input
                type="number"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.customer_rank }"
                v-model.number="form.customer_rank"
                :readonly="isViewMode"
                min="0" />
              <div v-if="serverErrors.customer_rank" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.customer_rank" :key="'cr-' + idx">{{ msg }}</div>
              </div>
            </div>

            <div class="col-md-3">
              <label class="form-label">Supplier Rank</label>
              <input
                type="number"
                class="form-control"
                :class="{ 'is-invalid': serverErrors.supplier_rank }"
                v-model.number="form.supplier_rank"
                :readonly="isViewMode"
                min="0" />
              <div v-if="serverErrors.supplier_rank" class="invalid-feedback">
                <div v-for="(msg, idx) in serverErrors.supplier_rank" :key="'sr-' + idx">{{ msg }}</div>
              </div>
            </div>

            <!-- Active -->
            <div class="col-md-3 d-flex align-items-end">
              <div class="form-check form-switch">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="isActiveSwitch"
                  v-model="form.is_active"
                  :disabled="isViewMode" />
                <label class="form-check-label" for="isActiveSwitch">Active</label>
              </div>
            </div>
          </div>

          <div class="mt-4 d-flex gap-2">
            <button v-if="!isViewMode" type="submit" class="btn btn-primary" :disabled="submitting">
              <i class="fas fa-save me-1" v-if="!submitting"></i>
              {{ submitting ? 'Saving...' : 'Save' }}
            </button>

            <button type="button" class="btn btn-outline-secondary" @click="redirectToList">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, computed, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios';
  import vSelect from 'vue-select'; // Import para usar <v-select> en el template

  // Ajusta al nombre/path real de tu ruta de lista
  const LIST_ROUTE_NAME = 'parties';
  const LIST_ROUTE_PATH = '/parties';

  const route = useRoute();
  const router = useRouter();

  const id = route.query.id ?? null;
  const isViewMode = route.query.mode === 'view';
  const isEditMode = !!id && !isViewMode;
  const isCreateMode = !id;

  const title = computed(() => (isCreateMode ? 'Create Party' : isViewMode ? 'View Party' : 'Edit Party'));

  const loading = ref(false);
  const submitting = ref(false);
  const serverErrors = reactive({});

  // Form alineado con tu serializer
  const form = reactive({
    name: '',
    rfc: '',
    street: '',
    floor_office: '',
    city: '',
    state: '',
    zipcode: '',
    country: '',
    phone: '',
    email: '',
    types: [], // M2M: array de IDs
    category: null, // FK: ID o null
    default_price_type: null, // FK: ID o null
    customer_rank: 0,
    supplier_rank: 0,
    is_active: true,
  });

  // Catálogos para vue-select
  const options = reactive({
    types: [],
    categories: [],
    priceTypes: [],
  });

  function normalizePaginator(data) {
    // DRF paginado -> .results; sin paginado -> array directo
    return Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : [];
  }

  function trimForm() {
    for (const k of Object.keys(form)) {
      if (typeof form[k] === 'string') form[k] = form[k].trim();
    }
    if (form.email) form.email = form.email.toLowerCase();
  }

  function resetServerErrors() {
    for (const k of Object.keys(serverErrors)) delete serverErrors[k];
  }

  function redirectToList() {
    if (LIST_ROUTE_NAME) {
      try {
        router.push({ name: LIST_ROUTE_NAME });
      } catch {
        router.push(LIST_ROUTE_PATH);
      }
    } else {
      router.push(LIST_ROUTE_PATH);
    }
  }

  /** -------- Validación cliente (mínima) -------- */
  function validateClient() {
    const errs = {};

    // name
    if (!form.name) errs.name = ['This field is required.'];
    else if (form.name.length < 2) errs.name = ['Must be at least 2 characters.'];
    else if (form.name.length > 255) errs.name = ['Must be 255 characters or fewer.'];

    // longitudes de texto
    if (form.rfc && form.rfc.length > 50) errs.rfc = ['Must be 50 characters or fewer.'];
    [
      ['street', 100],
      ['floor_office', 100],
      ['city', 100],
      ['state', 100],
      ['country', 100],
    ].forEach(([k, max]) => {
      if (form[k] && form[k].length > max) errs[k] = [`Must be ${max} characters or fewer.`];
    });
    [
      ['zipcode', 20],
      ['phone', 20],
    ].forEach(([k, max]) => {
      if (form[k] && form[k].length > max) errs[k] = [`Must be ${max} characters or fewer.`];
    });

    // email opcional pero con formato si existe
    if (form.email) {
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRe.test(form.email)) errs.email = ['Enter a valid email address.'];
    }

    // ranks enteros no negativos
    ['customer_rank', 'supplier_rank'].forEach(k => {
      if (!Number.isInteger(form[k]) || form[k] < 0) errs[k] = ['Must be a non-negative integer.'];
    });

    resetServerErrors();
    Object.assign(serverErrors, errs);
    return Object.keys(errs).length === 0;
  }

  /** -------- Carga de catálogos y detalle -------- */
  async function fetchCatalogs() {
    const [t, c, p] = await Promise.all([
      axios.get('/api/party-types/?ordering=name'),
      axios.get('/api/party-categories/?ordering=name'),
      axios.get('/api/price-types/?ordering=name'),
    ]);
    options.types = normalizePaginator(t.data);
    options.categories = normalizePaginator(c.data);
    options.priceTypes = normalizePaginator(p.data);
  }

  async function fetchPartyIfNeeded() {
    if (!id) return;
    const { data } = await axios.get(`/api/parties/${id}/`);
    // Esperado: types como array de IDs; category/default_price_type como ID o null
    Object.assign(form, data);
  }

  onMounted(async () => {
    loading.value = true;
    try {
      await fetchCatalogs();
      await fetchPartyIfNeeded();
    } catch (e) {
      // Mostrar error y permitir reintentar sin redirigir (evita loops)
      serverErrors.non_field_errors = ['Failed to load catalogs. Check your session or network and try again.'];
      console.error('PartyForm init error:', e);
    } finally {
      loading.value = false;
    }
  });

  /** -------- Guardar (create/edit) -------- */
  async function handleSubmit() {
    if (isViewMode) return;
    trimForm();
    if (!validateClient()) return;

    submitting.value = true;
    try {
      if (isEditMode) {
        await axios.put(`/api/parties/${id}/`, form);
      } else {
        await axios.post('/api/parties/', form);
      }
      // Éxito silencioso + redirect
      redirectToList();
    } catch (error) {
      const data = error?.response?.data;
      resetServerErrors();
      if (data && typeof data === 'object') {
        Object.assign(serverErrors, data);
      } else {
        serverErrors.non_field_errors = ['Unexpected error. Please try again.'];
      }
    } finally {
      submitting.value = false;
    }
  }
</script>

<style scoped>
  /* Asegura que vue-select se vea como un control full-width */
  .v-select {
    --vs-controls-color: var(--bs-secondary);
  }
  .v-select,
  .v-select .vs__dropdown-toggle {
    width: 100%;
  }
</style>
