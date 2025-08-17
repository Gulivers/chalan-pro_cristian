<template>
  <div class="container">
    <h3 class="card-title-orange pt-3">
      <p>{{ cleanFormTitle }}</p>
    </h3>
    <div class="card shadow mb-4">
      <div class="card-header">
        <h6 class="ms-1 font-weight-bold text-primary">{{ formTitle }}</h6>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleSubmit" v-if="Object.keys(internalSchema).length">
          <div class="row px-2 text-start">
            <div class="col-md-6 col-lg-6 mb-3" v-for="(config, key) in internalSchema" :key="key">
              <!-- Evita duplicar label en booleanos -->
              <label v-if="config.type !== 'boolean'" class="form-label">
                {{ config.label }}
              </label>

              <input
                v-if="config.type === 'string' || config.type === 'text'"
                v-model="form[key]"
                type="text"
                class="form-control"
                :placeholder="`Enter ${config.label}...`"
                :readonly="readOnly" />

              <textarea
                v-else-if="config.type === 'textarea' || config.widget === 'textarea'"
                v-model="form[key]"
                class="form-control"
                :placeholder="`Enter ${config.label}...`"
                :readonly="readOnly" />

              <select v-else-if="config.type === 'select'" v-model="form[key]" class="form-select" :disabled="readOnly">
                <option value="" disabled selected hidden class="text-muted">Select {{ config.label }}...</option>
                <option v-for="opt in optionsMap[key] || []" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>

              <div v-else-if="config.type === 'boolean'" class="form-check form-switch d-flex align-items-center mt-4">
                <input
                  v-model="form[key]"
                  class="form-check-input"
                  type="checkbox"
                  role="switch"
                  :id="key"
                  :disabled="readOnly" />
                <label class="form-check-label ms-2" :for="key">
                  {{ config.label }}
                </label>
              </div>
            </div>
          </div>

          <!-- Botones -->
          <div class="mt-4" v-if="!readOnly">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary ms-2" @click="cancelForm">Cancel</button>
          </div>

          <div v-else>
            <button type="button" class="btn btn-secondary mt-3" @click="cancelForm">Back</button>
          </div>
        </form>

        <div v-else>
          <p class="text-muted">Schema not loaded or has no fields.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import selectMixin from '@/helpers/useSelectOptions';
  import appMixin from '@/mixins/appMixin';

  export default {
    name: 'DynamicForm',
    mixins: [selectMixin],
    props: {
      schema: Object,
      schemaEndpoint: String,
      apiEndpoint: String,
      objectId: {
        type: [String, Number],
        default: null,
      },
      formTitle: {
        type: String,
        default: 'Form',
      },
      readOnly: {
        type: Boolean,
        default: false,
      },
      redirectAfterSave: {
        type: String,
        default: null,
      },
      isModal: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        internalSchema: {},
        form: {},
        fields: [],
      };
    },
    computed: {
      cleanFormTitle() {
        return this.formTitle
          .replace(/^Create\s+/i, '')
          .replace(/^Edit\s+/i, '')
          .replace(/^View\s+/i, '')
          .trim();
      },
    },
    watch: {
      objectId: {
        immediate: true,
        handler(newVal) {
          if (this.internalSchema && Object.keys(this.internalSchema).length) {
            this.loadRecord();
          }
        },
      },
    },
    async created() {
      try {
        // Cargar esquema desde props o endpoint
        if (this.schema && Object.keys(this.schema).length) {
          this.internalSchema = this.schema;
        } else if (this.schemaEndpoint) {
          const response = await axios.get(this.schemaEndpoint);
          this.internalSchema = response.data || {};
        }

        this.fields = Object.keys(this.internalSchema);
        await this.loadOptionsForSchema(this.internalSchema);
        this.loadRecord(); // Primera carga
      } catch (err) {
        console.error('❌ Error initializing schema:', err);
      }
    },
    methods: {
      async loadRecord() {
        if (!this.internalSchema || !Object.keys(this.internalSchema).length) return;

        try {
          if (this.objectId) {
            const res = await axios.get(`${this.apiEndpoint}${this.objectId}/`);
            this.form = res.data;
          } else {
            this.form = Object.fromEntries(
              this.fields.map(f => {
                const type = this.internalSchema[f]?.type;
                return [f, type === 'boolean' ? false : ''];
              })
            );
          }
        } catch (err) {
          console.error('❌ Error loading record:', err);
        }
      },
      handleSubmit() {
        const cleanedForm = { ...this.form };

        for (const key of this.fields) {
          const config = this.internalSchema[key];
          if (config.type === 'select' && config.optionsEndpoint) {
            const value = cleanedForm[key];
            cleanedForm[key] = typeof value === 'object' && value !== null ? value.id || value.value : value;
          }
        }

        const url = this.objectId ? `${this.apiEndpoint}${this.objectId}/` : this.apiEndpoint;
        const method = this.objectId ? 'put' : 'post';

        axios[method](url, cleanedForm)
          .then(() => {
            if (this.redirectAfterSave) {
              this.$router.push(this.redirectAfterSave);
            } else {
              this.$emit('saved');
            }
          })
          .catch(err => {
            if (err.response?.data) {
              this.handleFieldErrors(err.response.data);
            } else {
              this.notifyError('An error occurred while saving.');
            }
          });
      },
      handleFieldErrors(errors) {
        let errorMessages = [];

        for (const [field, messages] of Object.entries(errors)) {
          const fieldLabel = this.internalSchema[field]?.label || field;
          const messageList = Array.isArray(messages) ? messages.join(', ') : messages;
          errorMessages.push(`${fieldLabel}: ${messageList}`);
        }

        if (errorMessages.length) {
          this.notifyError(errorMessages.join('\n'));
        } else {
          this.notifyError('Validation error occurred.');
        }
      },
      cancelForm() {
        if (this.isModal) {
          this.$emit('cancel');
        } else {
          if (this.$router && this.$route.name) {
            this.$router.back();
          } else {
            this.$emit('cancel');
          }
        }
      },
    },
  };
</script>

<style scoped>
  .form-check-label {
    margin-left: 0.5rem;
  }
</style>
