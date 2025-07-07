<template>
    <div class="modal fade" ref="modalElement" id="houseModelModal" tabindex="-1" aria-labelledby="houseModelModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="houseModelModalLabel">
                        {{ action === 'edit' ? 'Edit House Model ' + houseModelId : 'Add House Model' }}
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="handleSubmit">
                        <!-- Campo para nombre del modelo -->
                        <div class="mb-3">
                            <label for="houseModelName" class="form-label">House Model Name</label>
                            <input type="text" class="form-control" id="houseModelName" v-model="houseModel.name"
                                :class="{ 'is-invalid': error.houseModelName }" @input="clearError('houseModelName')" />
                            <div v-if="error.houseModelName" class="text-danger mt-1">
                                Please provide a house model name.
                            </div>
                        </div>

                        <!-- Campo para comunidades (Jobs) -->
                        <div class="mb-3">
                            <label for="jobs" class="form-label">Select Communities (Jobs)</label>
                            <multiselect v-model="houseModel.jobs" :options="groupedJobs" :group-values="'options'"
                                :group-label="'label'" :track-by="'id'" :multiple="true" label="name"
                                placeholder="Select Communities" @input="clearError('jobs')"
                                :class="{ 'is-invalid': error.jobs }" />
                            <div v-if="error.jobs" class="text-danger mt-1">
                                Please select at least one community.
                            </div>
                        </div>

                        <!-- Botones de acción -->
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
                            <button type="button" class="btn btn-primary" @click="handleSubmit">
                                {{ action === 'edit' ? 'Update' : 'Save' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';

export default {
    components: { Multiselect },
    props: {
        action: String,
        houseModelId: {
            type: Number,
            default: null,
        },
    },
    data() {
        return {
            houseModel: {
                name: '',
                jobs: [],
            },
            builders: [],
            groupedJobs: [],
            error: {
                jobs: false,
                houseModelName: false,
            },
        };
    },
    watch: {
        houseModelId: {
            handler(newVal) {
                if (this.action === 'edit' && newVal) {
                    this.fetchHouseModelJobs();
                } else {
                    this.houseModel = {
                        name: '',
                        jobs: [],
                    };
                }
            },
            immediate: true,
        },
    },
    methods: {
        validateFields() {
            let isValid = true;

            // Validar que al menos un Job esté seleccionado
            if (!this.houseModel.jobs || this.houseModel.jobs.length === 0) {
                this.error.jobs = true;
                isValid = false;
            } else {
                this.error.jobs = false;
            }

            // Validar que el nombre del modelo no esté vacío
            if (!this.houseModel.name || this.houseModel.name.trim() === '') {
                this.error.houseModelName = true;
                isValid = false;
            } else {
                this.error.houseModelName = false;
            }

            return isValid;
        },
        clearError(field) {
            this.error[field] = false; // Elimina el error correspondiente
        },
        async handleSubmit() {
            if (!this.validateFields()) {
                return;
            }

            try {
                const houseModelToSend = {
                    name: this.houseModel.name,
                    jobs: this.houseModel.jobs.map(job => job.id), // Transformar los Jobs a IDs
                };

                if (this.action === 'edit') {
                    await axios.put(`/api/house_model/${this.houseModelId}/`, houseModelToSend);
                } else {
                    await axios.post('/api/house_model/', houseModelToSend);
                }

                this.$emit('refresh'); // Notificar al componente padre
                this.closeModal();
            } catch (error) {
                console.error('Error saving House Model:', error);
            }
        },

        showModal() {
            if (this.modalInstance) {
                this.modalInstance.show();
            }
        },
        closeModal() {
            if (this.modalInstance) {
                this.modalInstance.hide();
            }
            this.$emit('close');
        },
        async fetchBuildersAndJobs() {
            try {
                const builderResponse = await axios.get('/api/builder/');
                const jobResponse = await axios.get('/api/job/');
                this.builders = builderResponse.data || [];
                const jobs = jobResponse.data || [];
                this.groupedJobs = this.builders.map(builder => ({
                    label: 'Builder: ' + builder.name || 'Unnamed Builder',
                    options: jobs.filter(job => job && job.builder === builder.id && job.name),
                })).filter(group => group.options.length > 0);
            } catch (error) {
                console.error('Error fetching Builders or Jobs:', error);
            }
        },
        async fetchHouseModelJobs() {
            try {
                if (this.houseModelId) {
                    const response = await axios.get(`/api/house_models/${this.houseModelId}/jobs/`);
                    const { houseModel, jobs } = response.data;
                    this.houseModel.name = houseModel.name;
                    this.houseModel.jobs = jobs.map(job => ({
                        id: job.id,
                        name: job.name,
                    }));
                }
            } catch (error) {
                console.error('Error fetching House Model Jobs:', error);
            }
        },
    },
    mounted() {
        this.fetchBuildersAndJobs();
        if (this.houseModelId) {
            this.fetchHouseModelJobs();
        }
        // Vue-style Bootstrap modal instance
        if (this.$refs.modalElement) {
            const { Modal } = require('bootstrap');
            this.modalInstance = Modal.getOrCreateInstance(this.$refs.modalElement);
        }
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
