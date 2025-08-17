<template>
    <div
      class="modal fade"
      ref="modalElement"
      id="houseModelModal"
      tabindex="-1"
      aria-labelledby="houseModelModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="houseModelModalLabel">
              {{ isEditMode ? `Edit House Model #${houseModelId}` : 'Add House Model' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
  
          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <!-- Name -->
              <div class="mb-3">
                <label for="houseModelName" class="form-label">House Model Name X</label>
                <input
                  id="houseModelName"
                  type="text"
                  class="form-control"
                  v-model.trim="houseModel.name"
                  :class="{ 'is-invalid': error.houseModelName }"
                  @input="clearError('houseModelName')"
                />
                <div v-if="error.houseModelName" class="text-danger mt-1">
                  Please provide a house model name.
                </div>
              </div>
  
              <!-- Jobs (grouped by Builder) -->
              <div class="mb-3">
                <label class="form-label">Select Communities (Jobs)</label>
                <multiselect
                  v-model="houseModel.jobs"
                  :options="groupedJobs"
                  :group-values="'options'"
                  :group-label="'label'"
                  :multiple="true"
                  :track-by="'id'"
                  label="name"
                  :close-on-select="false"
                  placeholder="Select Communities"
                  @input="clearError('jobs')"
                  :class="{ 'is-invalid': error.jobs }"/>
                <div v-if="error.jobs" class="text-danger mt-1">
                  Please select at least one community.
                </div>
              </div>
  
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                <button type="submit" class="btn btn-primary">
                  {{ isEditMode ? 'Update' : 'Save' }}
                </button>
              </div>
            </form>
          </div>
  
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import Multiselect from 'vue-multiselect'
  import 'vue-multiselect/dist/vue-multiselect.min.css'
  import modalFocusMixin from '@/mixins/modalFocusMixin.js'
  
  export default {
    name: 'HouseModelModal',
    components: { Multiselect },
    mixins: [modalFocusMixin],
    props: {
      action: { type: String, default: 'add' },          // 'add' | 'edit'
      houseModelId: { type: Number, default: null },     // id a editar
      builderId: { type: [Number, String], default: null },
    },
    data() {
      return {
        modalInstance: null,
        houseModel: {
          name: '',
          // En el multiselect guardamos objetos {id, name}
          jobs: [],
        },
        builders: [],
        jobs: [],
        groupedJobs: [],
        error: {
          jobs: false,
          houseModelName: false,
        },
        loading: false,
      }
    },
    computed: {
      isEditMode() {
        return this.action === 'edit' && !!this.houseModelId
      },
      effectiveBuilderId() {
        const propId = Number(this.builderId)
        if (Number.isFinite(propId) && propId > 0) return propId
        const derived = Number(this.derivedBuilderId)
        return (Number.isFinite(derived) && derived > 0) ? derived : null
      },
    },
    watch: {
      builderId: {
        immediate: true,
        handler() {
            this.fetchBuildersAndJobs()
        }
      },
      houseModelId: {
        immediate: true,
        async handler(newVal) {
          this.houseModel = { name: '', jobs: [] }
          if (this.action === 'edit' && newVal) {
            if (!this.builders.length || !this.jobs.length) {
              await this.fetchBuildersAndJobs()
            }
            await this.loadForEdit()
          }
        }
      }
    },
    methods: {
      async showModal() {
        // Refrescar datos cada vez que se abre el modal
        await this.fetchBuildersAndJobs()
        if (this.modalInstance) {
          this.modalInstance.show()
          this.handleModalShow(this.$refs.modalElement)
        }
      },
      hideModal() {
        this.handleModalHide(this.$refs.modalElement)
        if (this.modalInstance) this.modalInstance.hide()
      },
      closeModal() {
        this.handleModalHide(this.$refs.modalElement)
        this.hideModal()
        this.$emit('close')
      },
  
      validateFields() {
        let ok = true
  
        if (!this.houseModel.name || this.houseModel.name.trim() === '') {
          this.error.houseModelName = true
          ok = false
        } else {
          this.error.houseModelName = false
        }
  
        if (!this.houseModel.jobs || this.houseModel.jobs.length === 0) {
          this.error.jobs = true
          ok = false
        } else {
          this.error.jobs = false
        }
  
        return ok
      },
      clearError(field) {
        this.error[field] = false
      },
  

      async fetchBuildersAndJobs() {
        try {
          // console.log('🔄 Refrescando datos de Builders y Jobs...')
          
          const [builderRes, jobRes] = await Promise.all([
            axios.get('/api/builder/'),
            axios.get('/api/job/')
          ])
          
          this.builders = Array.isArray(builderRes.data) ? builderRes.data : []
          this.jobs = Array.isArray(jobRes.data) ? jobRes.data : []
          
          // console.log(`✅ Datos actualizados: ${this.builders.length} builders, ${this.jobs.length} jobs`)
          
          this.buildGroupedJobs()
        } catch (err) {
          console.error('❌ Error fetching Builders/Jobs:', err)
        }
      },
  
      buildGroupedJobs() {
        const bId = Number(this.builderId)
        const filterByBuilder = Number.isFinite(bId) && bId > 0
        // 1) Si hay builderId, limitamos los builders al seleccionado; si no, usamos todos
        const buildersSource = filterByBuilder
          ? this.builders.filter(b => b.id === bId)
          : this.builders

        // 2) Agrupamos jobs por cada builder “permitido”
        const groups = buildersSource.map(b => {
          const options = (this.jobs || [])
            .filter(j => j && j.builder === b.id && j.name)
            .map(j => ({ id: j.id, name: j.name }))

          return options.length
            ? { label: `Builder: ${b.name}`, options }
            : null
        }).filter(Boolean)

        this.groupedJobs = groups
        
        // console.log(`Jobs agrupados: ${this.groupedJobs.length} grupos disponibles`)
        // this.groupedJobs.forEach(group => {
        //   console.log(`  - ${group.label}: ${group.options.length} jobs`)
        // })
      },
  

      async loadForEdit() {
        if (!this.houseModelId) return
        try {
          // ENDPOINT DETALLE CONSISTENTE
          // viewset/urls para que exista: GET /api/house_model/<id>/
          const res = await axios.get(`/api/house_model/${this.houseModelId}/`)
          const data = res.data || {}
  
          // name directo
          this.houseModel.name = data.name || ''
  
          // jobs puede venir como lista de IDs o de objetos; soportamos ambos
          const jobIds = Array.isArray(data.jobs)
            ? data.jobs.map(j => (typeof j === 'object' ? j.id : j)).filter(Boolean)
            : []
  
          // Mapear IDs a objetos {id, name} para el multiselect
          const jobMap = new Map(this.jobs.map(j => [j.id, j.name]))
          this.houseModel.jobs = jobIds
            .filter(id => jobMap.has(id))
            .map(id => ({ id, name: jobMap.get(id) }))
        } catch (err) {
          console.error('Error loading house model detail:', err)
        }
      },
  
      async handleSubmit() {
        if (!this.validateFields()) return
  
        // Transformar a payload de API: jobs -> ids
        const payload = {
          name: this.houseModel.name,
          jobs: this.houseModel.jobs.map(j => j.id),
        }
  
        try {
          if (this.isEditMode) {
            const { data: updated } = await axios.put(`/api/house_model/${this.houseModelId}/`, payload)
            // también emitimos en edición para refrescar lista y mantener selección
            this.$emit('saved', updated)
          } else {
            const { data: created } = await axios.post('/api/house_model/', payload)
            // emitimos el creado (debe traer al menos id y name)
            this.$emit('saved', created)
          }
          // Notificar al padre y cerrar
          this.$emit('refresh')   // tu padre escucha y refetch
          this.closeModal()
        } catch (err) {
          console.error('Error saving House Model:', err)
        }
      },
    },
  
    mounted() {
      // Instancia modal Bootstrap 5
      if (this.$refs.modalElement) {
        const { Modal } = require('bootstrap')
        this.modalInstance = Modal.getOrCreateInstance(this.$refs.modalElement)
        this.setupModalFocusHandling(this.$refs.modalElement)
      }
    },
  }
  </script>
  
  <style scoped>
  .text-danger { color: red; font-size: 0.875rem; }
  .is-invalid { border-color: red !important; box-shadow: 0 0 5px red !important; }
  </style>
  