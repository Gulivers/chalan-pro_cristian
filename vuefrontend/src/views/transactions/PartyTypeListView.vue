<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Party Types</h3>
      <router-link to="/party-types/form" class="btn btn-success">+ New Party Type</router-link>
    </div>

    <div class="mb-3 row">
      <div class="col-md-2">
        <select v-model="perPage" class="form-select">
          <option v-for="n in [5, 10, 25, 50]" :key="n" :value="n">{{ n }} </option>entries per page
        </select>
      </div>
      <div class="col-md-4">
        <input v-model="search" type="text" class="form-control" placeholder="Search by name or description..." />
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
      
      <template #cell(is_active)="data">
        <td class="text-center">
          <span v-if="data.item.is_active" class="badge bg-success">Active</span>
          <span v-else class="badge bg-secondary">Inactive</span>
        </td>
      </template>

      <template #cell(actions)="data">
        <td class="text-center">
          <div class="btn-group btn-group-sm" role="group">
            <router-link :to="`/party-types/form?id=${data.item.id}&mode=view`" class="btn btn-outline-success">
              View
            </router-link>
            <router-link :to="`/party-types/form?id=${data.item.id}&mode=edit`" class="btn btn-outline-primary">
              Edit
            </router-link>
            <button @click="deletePartyType(data.item.id)" class="btn btn-outline-danger">Delete</button>
          </div>
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
  import { ref, computed, onMounted, getCurrentInstance } from 'vue';
  import axios from 'axios';
  
  const { proxy } = getCurrentInstance();

  const partyTypes = ref([]);
  const search = ref('');
  const perPage = ref(10);
  const currentPage = ref(1);

  const fields = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'description', label: 'Description', sortable: true },
    { key: 'is_active', label: 'Status', thClass: 'text-center', tdClass: 'text-center' },
    { key: 'actions', label: 'Actions', thClass: 'text-center', tdClass: 'text-center' },
  ];

  const fetchPartyTypes = async () => {
    try {
      const res = await axios.get('/api/party-types/');
      partyTypes.value = res.data;
    } catch (err) {
      console.error('Error fetching party types', err);
      if (proxy.notifyError) {
        proxy.notifyError('Error loading party types.');
      }
    }
  };

  onMounted(fetchPartyTypes);

  const filteredItems = computed(() => {
    if (!search.value) return partyTypes.value;
    return partyTypes.value.filter(item =>
      `${item.name} ${item.description || ''}`.toLowerCase().includes(search.value.toLowerCase())
    );
  });

  const deletePartyType = id => {
    proxy.confirmDelete(
      'Are you sure?',
      'This action cannot be undone.',
      async () => {
        try {
          await axios.delete(`/api/party-types/${id}/`);
          partyTypes.value = partyTypes.value.filter(party => party.id !== id);
          if (proxy.notifyToastSuccess) {
            proxy.notifyToastSuccess('The party type has been deleted.');
          }
        } catch (err) {
          console.error('Error deleting party type', err);
          if (proxy.notifyError) {
            proxy.notifyError('Error deleting the party type.');
          }
        }
      }
    );
  };
</script>

<style scoped>
  table td {
    vertical-align: middle;
  }
  
  .btn-group {
    justify-content: center;
  }
  
  .btn-group .btn {
    border-radius: 0.25rem;
  }
  
  .btn-group .btn:not(:last-child) {
    margin-right: 2px;
  }
</style>