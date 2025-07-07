<template>
  <div class="container my-4">
    <div v-if="Message" :class="['alert', typeMessage]" role="alert">
      {{ Message }}
    </div>
    <div class="card shadow-lg">
      <div class="card-header d-flex justify-content-between align-items-center">
        
        <button type="button" class="btn btn-success text-white" @click="openCreateModal">
          + Agregar Identidad 
        </button>
        <h5 class="mb-5 text-primary">Identity Company</h5>
        
        <div class="d-flex align-items-center">
          <label class="me-2 mb-0">Items for page:</label>
          <select class="form-select form-select-sm w-auto" v-model="pageSize" @change="fetchIdentities(1)">
            <option v-for="size in pageSizeOptions" :key="size" :value="size">{{ size }}</option>
          </select>
        </div>
        
      </div>
      
        <div class="input-group">
          <span class="input-group-text">
            <i class="bi bi-search">Search:</i>
          </span>
          <input
            v-model="searchTerm"
            type="text"
            class="form-control"
            placeholder="Buscar por nombre o usuario..."
            @input="debouncedFetch"
          />
        </div>

      <div class="card-body p-0">

        <div v-if="loading" class="text-center p-4">Loading identities...</div>

        <div v-else class="table-responsive">
          <table class="table table-striped table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>User</th>
                <th>Name Company</th>
                <th>Logo</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="identity in identities" :key="identity.id">
                <td>{{ identity.username }}</td>
                <td>{{ identity.name }}</td>
                <td>
                  <img
                    v-if="identity.logo"
                    :src="identity.logo"
                    alt="logo"
                    class="img-thumbnail"
                    style="max-width: 100px; height: auto; aspect-ratio: 3/2; object-fit: contain;"
                  />
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-secondary me-2" @click="view(identity)">
                    View
                  </button>
                  <button class="btn btn-sm btn-outline-primary me-2" @click="edit(identity)">
                    Edit
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="deleteIdentity(identity.id)">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <nav v-if="totalPages > 1" class="card-footer">
        <ul class="pagination justify-content-center my-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="fetchIdentities(currentPage - 1)">«</button>
          </li>

          <li
            v-for="page in totalPages"
            :key="page"
            class="page-item"
            :class="{ active: currentPage === page }"
          >
            <button class="page-link" @click="fetchIdentities(page)">{{ page }}</button>
          </li>

          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link" @click="fetchIdentities(currentPage + 1)">»</button>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Modal -->
    <div
      class="modal fade"
      :class="{ show: mostrarModal }"
      :style="{ display: mostrarModal ? 'block' : 'none' }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" v-if="!isViewMode">

          <div class="modal-header" v-if="!isCreateMode">
            <h5 class="modal-title" >Edit Identity</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>

          <div class="modal-header" v-else>
            <h5 class="modal-title">Create Identity</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="saveIdentity">
              <div class="mb-3" v-if="isCreateMode">
                <label class="form-label">User</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="userQuery"
                  @input="onUserSearch"
                  @focus="userDropdownVisible = true"
                  @blur="hideDropdownWithDelay"
                  placeholder="Buscar usuario..."
                  required
                />
                <ul
                  class="list-group position-absolute w-100 shadow"
                  v-show="userDropdownVisible && userOptions.length"
                  style="z-index: 1000; max-height: 200px; overflow-y: auto;"
                >
                  <li
                    class="list-group-item list-group-item-action"
                    v-for="user in userOptions"
                    :key="user.id"
                    @mousedown.prevent="selectUser(user)"
                  >
                    <strong>{{ user.username }}</strong>
                  </li>
                </ul>
              </div>
              <div class="mb-3">
                <label class="form-label">Name Company</label>
                <input v-model="form.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Logo</label>
                <input type="file" class="form-control" @change="onFileChange" />
              </div>
              <button type="submit" class="btn btn-primary w-100">Save</button>
            </form>
          </div>

        </div>

        <div class="modal-content" v-else>

          <div class="modal-header">
            <h5 class="modal-title">Identity</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>

          <div class="modal-body">
            <div>
              <div class="mb-3">
                <label class="form-label">Logo</label><br />
                <img
                  v-if="form.logo"
                  :src="form.logo"
                  alt="logo"
                  class="img-thumbnail"
                  style="max-width: 100%; height: auto; aspect-ratio: 3/2; object-fit: contain;"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Name Company</label>
                <input :value="form.name" type="text" class="form-control" disabled />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div class="modal-backdrop fade show" v-show="mostrarModal"></div>
  </div>
</template>

<script>
import axios from 'axios';
import debounce from 'lodash/debounce';

export default {
  name: 'AdminIdentities',
  data() {
    return {
      mostrarModal: false,
      isViewMode: false,
      isCreateMode: false,
      identities: [],
      loading: false,
      form: {
        id: null,
        user_id: null,
        username: '',
        name: '',
        logo: null,
      },
      user_id: null,
      currentPage: 1,
      totalPages: 1,
      pageSizeOptions: [5, 10, 20],
      pageSize: 10,
      userQuery: '',
      userOptions: [],
      searchTerm: '',
      Message: '',
      typeMessage : '',
    };
  },
  watch: {
    searchTerm() {
      this.debouncedFetchIdentities();
    }
  },
  mounted() {
    this.debouncedFetchIdentities = debounce(this.fetchIdentities, 500);
    this.fetchIdentities();
  },
  methods: {
    putMessage(type, message) {
      this.typeMessage = type;
      this.Message = message;
    },
    cerrarModal() {
      this.mostrarModal = false;
      this.isViewMode = false;
      this.isCreateMode = false;
      this.resetForm();
    },
    fetchIdentities(page = 1) {
      this.loading = true;
      axios
        .get(`/api/identity/?search=${this.searchTerm}&page=${page}&page_size=${this.pageSize}`)
        .then((res) => {
          console.log('Identities fetched:', res.data);
          this.identities = res.data.results;
          this.totalPages = Math.ceil(res.data.count / this.pageSize);
          this.currentPage = page;
        })
        .catch((error) => {
          console.error('Error fetching identities:', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onUserSearch() {
      if (this.userQuery.length < 1) {
        this.userOptions = [];
        return;
      }
      axios.get(`/api/users/?search=${this.userQuery}`).then((res) => {
        this.userOptions = res.data.results;
      });
    },
    selectUser(user) {
      this.userQuery = `${user.username}`;
      this.user_id = user.id;
      this.userDropdownVisible = false;
    },
    hideDropdownWithDelay() {
      setTimeout(() => {
        this.userDropdownVisible = false;
      }, 200); 
    },
    onFileChange(e) {
      this.form.logo = e.target.files[0];
    },
    saveIdentity() {
      const formData = new FormData();
      formData.append('name', this.form.name);
      if (this.form.logo) formData.append('logo', this.form.logo);

      if (this.isCreateMode) {
        
        formData.append('user_id', this.user_id);
        axios
        .post('/api/identity/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then(() => {
          alert('Identidad creada con éxito');
          this.fetchIdentities();
          this.cerrarModal();
          this.putMessage('alert-success', 'Identity created successfully');
        })
        .catch(error => {
            if (error.response && error.response.status === 400) {
              const errores = error.response.data;

              this.cerrarModal();
              if (errores.user) {
                this.errorMessage = errores.user[0];
              } else if (errores.detail) {
                this.errorMessage = errores.detail;
              } else {
                this.errorMessage = "Error al crear identidad.";
              }
            } else {
              this.errorMessage = "Error del servidor. Intenta nuevamente.";
            }

            console.error('Error al crear:', error);
        });
      } else {
        formData.append('id', this.form.id);
        axios
          .put(`/api/identity/${this.form.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          .then(() => {
            alert('Datos actualizados con éxito');
            this.fetchIdentities();
            this.cerrarModal();
            this.putMessage('alert-primary', 'Update your identity.');
          })
          .catch(error => {
            if (error.response && error.response.status === 400) {
              const errores = error.response.data;

              this.cerrarModal();
              if (errores.user) {
                this.errorMessage = errores.user[0];
              } else if (errores.detail) {
                this.errorMessage = errores.detail;
              } else {
                this.errorMessage = "Error al crear identidad.";
              }
            } else {
              this.errorMessage = "Error del servidor. Intenta nuevamente.";
            }

            console.error('Error al editar:', error);
          });
      }
    },
    view(identity) {
      this.isViewMode = true;
      this.mostrarModal = true;
      this.form = {
        id: identity.id,
        name: identity.name,
        logo: identity.logo, 
        username: identity.username, 
      };
    },
    edit(identity) {
      this.mostrarModal = true;
      this.form = {
        id: identity.id,
        name: identity.name,
        logo: null,
        username: identity.username,
      };
    },
    deleteIdentity(id) {
      if (confirm('¿Eliminar esta identidad?')) {
        axios.delete(`/api/identity/${id}/`).then(() => {
          this.fetchIdentities();
          this.putMessage('alert-danger', 'Identity deleted successfully.');
        });
      }
    },
    resetForm() {
      this.form = {
        id: null,
        name: '',
        logo: null,
        username: '', 
      };
      this.userQuery = '';
      this.userOptions = [];
      this.user_id = null;
    },
    openCreateModal() {
      this.isCreateMode = true;
      this.mostrarModal = true;
      this.isViewMode = false;
      this.resetForm();

    },
  },
};
</script>