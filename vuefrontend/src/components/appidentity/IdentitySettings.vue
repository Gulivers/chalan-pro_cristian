<template>
  <div class="container mt-5">
    <div v-if="Message" class="alert alert-info" role="alert">
      {{ Message }}
    </div>
    <div class="card shadow mx-auto" style="max-width: 400px;">
      <div class="card-body text-center">

        <div class="mb-3 w-100" style="max-width: 400px;">
          <img
            v-if="identity.logo"
            :src="identity.logo"
            alt="Company logo"
            class="img-fluid border rounded w-100"
            style="aspect-ratio: 3 / 2; object-fit: contain;"
          />
          <div
            v-else
            class="bg-secondary text-white d-flex align-items-center justify-content-center rounded"
            style="aspect-ratio: 3 / 2; width: 100%;"
          >
            Sin logo
          </div>
        </div>
        <div class="text-start mt-3">
          <label class="form-label fw-bold">Name Company</label>
          <div class="form-control-plaintext">{{ identity.name || 'No registrado' }}</div>
        </div>

        <!-- Botón para abrir el modal -->
        <button class="btn btn-outline-primary mt-3" @click="mostrarModal = true">
          Edit Profile
        </button>
      </div>
    </div>
  </div>

    <!-- Modal Bootstrap (SIEMPRE EN EL DOM) -->
  <div
    class="modal fade"
    :class="{ show: mostrarModal }"
    :style="{ display: mostrarModal ? 'block' : 'none' }"
    tabindex="-1"
    role="dialog"
    id="editModal"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">Edit Profile</h5>
          <button type="button" class="btn-close" @click="cerrarModal"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="saveChanges">
            <div class="mb-3">
              <label class="form-label">Name Company</label>
              <input v-model="identity.name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Logo</label>
              <input type="file" class="form-control" @change="onFileChange" />
            </div>
            <button type="submit" class="btn btn-primary w-100">Save</button>
          </form>
        </div>

      </div>
    </div>
  </div>
    <!-- Backdrop manual (opcional si no usas Bootstrap JS directamente) -->
    <div class="modal-backdrop fade show" v-show="mostrarModal"></div>
</template>



<script>
import { identity } from '@fullcalendar/core/internal';
import axios from 'axios';

export default {
  name: 'IdentitySettings',
  data() {
    return {
      mostrarModal: false,
      identity: {
        id: null,
        username: '',
        name: '',
        logo: ''
      },
      archivo: null,
      Message: '',
    };
  },
  mounted() {
    this.getOrCreateIdentity();
  },
  methods: {
    cerrarModal() {
      this.mostrarModal = false;
    },
    getOrCreateIdentity() {
      axios.get('/api/identity/me/')
        .then(res => {
          this.identity = {
            id: res.data.id,
            username: res.data.username,
            name: res.data.name,
            logo: res.data.logo || ''
          };
        })
        .catch(error => {
          console.error('Error al obtener o crear la identidad:', error);
        });
    },
    onFileChange(e) {
      this.archivo = e.target.files[0];
    },
    saveChanges() {
      const formData = new FormData();
      formData.append('name', this.identity.name);
      if (this.archivo) {
        formData.append('logo', this.archivo);
      }

      axios.put(`/api/identity/${this.identity.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
        .then(() => {
          alert('Datos actualizados con éxito');
          this.getOrCreateIdentity(); // Recarga la vista con nuevos datos
          this.cerrarModal();
          this.Message = 'Profile updated successfully.';
        })
        .catch(error => {
          console.error('Error al guardar cambios:', error);
          console.error('Error details:', error.response ? error.response.data : error.message);

        });
    }
  }
};
</script>
