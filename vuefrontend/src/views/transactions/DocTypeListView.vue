<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Type Documents</h3>
      <router-link to="/document-types/form" class="btn btn-success">+ New Document Type</router-link>
    </div>

    <div class="mb-3 row">
      <div class="col-md-4">
        <input v-model="search" type="text" class="form-control" placeholder="Search by code or description..." />
      </div>
      <div class="col-md-3">
        <select v-model="perPage" class="form-select">
          <option v-for="n in [5, 10, 25, 50]" :key="n" :value="n">{{ n }} entries per page</option>
        </select>
      </div>
    </div>

    <b-table
      :items="filteredItems"
      :fields="fields"
      :per-page="perPage"
      :current-page="currentPage"
      bordered
      hover
      responsive
      striped>
      <!-- Affects Physical -->
      <template #cell(affects_physical)="data">
        <td class="sorting_1 text-center">
          <span :class="data.item.affects_physical ? 'badge bg-success' : 'badge bg-secondary'">
            {{ data.item.affects_physical ? 'Yes' : 'No' }}
          </span>
        </td>
      </template>

      <!-- Affects Logical -->
      <template #cell(affects_logical)="data">
        <td class="sorting_1 text-center">
          <span :class="data.item.affects_logical ? 'badge bg-success' : 'badge bg-secondary'">
            {{ data.item.affects_logical ? 'Yes' : 'No' }}
          </span>
        </td>
      </template>

      <!-- Is Purchase -->
      <template #cell(is_purchase)="data">
        <td class="sorting_1 text-center">
          <span :class="data.item.is_purchase ? 'badge bg-success' : 'badge bg-secondary'">
            {{ data.item.is_purchase ? 'Yes' : 'No' }}
          </span>
        </td>
      </template>

      <!-- Is Sales -->
      <template #cell(is_sales)="data">
        <td class="sorting_1 text-center">
          <span :class="data.item.is_sales ? 'badge bg-success' : 'badge bg-secondary'">
            {{ data.item.is_sales ? 'Yes' : 'No' }}
          </span>
        </td>
      </template>

      <template #cell(is_active)="data">
        <td class="text-center">
          <span v-if="data.item.is_active" class="badge bg-success">Active</span>
          <span v-else class="badge bg-secondary">Inactive</span>
        </td>
      </template>

      <template #cell(actions)="data">
        <td class="text-center">
          <router-link :to="`/document-types/form?id=${data.item.id}`" class="btn btn-sm btn-outline-primary me-1">
            Edit
          </router-link>
          <button @click="deleteDocType(data.item.id)" class="btn btn-sm btn-outline-danger">Delete</button>
        </td>
      </template>
    </b-table>

    <b-pagination
      v-model="currentPage"
      :total-rows="filteredItems.length"
      :per-page="perPage"
      align="center"
      class="mt-3" />
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';

  const docTypes = ref([]);
  const search = ref('');
  const perPage = ref(10);
  const currentPage = ref(1);

  const fields = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'type_code', label: 'Code', sortable: true },
    { key: 'description', label: 'Description', sortable: true },
    { key: 'affects_physical', label: 'INVFIS', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'affects_logical', label: 'INVLOG', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'is_purchase', label: 'Purchase', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'is_sales', label: 'Sales', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'is_active', label: 'Status', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'actions', label: 'Actions', thClass: 'text-center', tdClass: 'text-center' },
  ];

  const fetchDocTypes = async () => {
    try {
      const res = await axios.get('/api/document-types/');
      docTypes.value = res.data;
    } catch (err) {
      console.error('Error fetching document types', err);
    }
  };

  onMounted(fetchDocTypes);

  const filteredItems = computed(() => {
    if (!search.value) return docTypes.value;
    return docTypes.value.filter(item =>
      `${item.type_code} ${item.description}`.toLowerCase().includes(search.value.toLowerCase())
    );
  });

  const deleteDocType = async id => {
    if (!confirm('Are you sure you want to delete this document type?')) return;
    try {
      await axios.delete(`/api/document-types/${id}/`);
      docTypes.value = docTypes.value.filter(doc => doc.id !== id);
    } catch (err) {
      console.error('Error deleting document type', err);
    }
  };
</script>

<style scoped>
  table td {
    vertical-align: middle;
  }
</style>
