<template>
  <div v-if="!isAbsence">
    <!-- Builder Field -->
    <div class="row align-items-center mb-2">
      <label class="col-auto col-form-label">Builder</label>
      <div class="col d-flex align-items-start gap-1">
        <v-select
          :options="builders"
          v-model="builderValue"
          :reduce="b => b.id"
          label="name"
          :disabled="!isEditing"
          placeholder="Select Builder"
          class="flex-grow-1"
          @change="resetJob"
          ref="builder"
          @keydown.enter="focusNext($event, 'job')"
          @focus="selectText"
        />
        <AddBuilderButton v-if="isEditing" @builder-added="reloadBuilders" />
        <EditBuilderButton
          v-if="isEditing && builderValue"
          :builder="selectedBuilder"
          @builder-updated="onBuilderUpdated"
        />
      </div>
    </div>

    <!-- Job Field -->
    <div class="row align-items-center mb-2">
      <label class="col-auto col-form-label">Job</label>
      <div class="col d-flex align-items-start gap-1">
        <v-select
          :options="filteredJobs"
          v-model="jobValue"
          :reduce="j => j.id"
          label="name"
          :disabled="!isEditing"
          placeholder="Select Job"
          class="flex-grow-1"
          @change="resetHouse"
          ref="job"
          @keydown.enter="focusNext($event, 'houseModel')"
          @focus="selectText"
        />
        <AddJobButton
          v-if="isEditing"
          :builder-id="builderValue"
          :builders="builders"
          @job-added="reloadJobs"
        />
        <EditJobButton
          v-if="isEditing && jobValue"
          :job="selectedJob"
          :builders="builders"
          @job-updated="reloadJobs"
        />
      </div>
    </div>

    <!-- House Model Field -->
    <div class="row align-items-center mb-3">
      <label class="col-auto col-form-label">House Model (Optional)</label>
      <div class="col d-flex align-items-start gap-1">
        <v-select
          :options="filteredHouses"
          v-model="houseModelValue"
          :reduce="h => h.id"
          label="name"
          :disabled="!isEditing"
          placeholder="Select House Model"
          class="flex-grow-1"
          ref="houseModel"
          @keydown.enter="focusNext($event, 'lot')"
          @focus="selectText"
        />
        <AddHouseModelButton
          :job-id="jobValue"
          @housemodel-added="reloadHouseModels"
        />
        <EditHouseModelButton
          v-if="houseModelValue"
          :house-model="selectedHouseModel"
          @housemodel-updated="reloadHouseModels"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from 'vue'
import VSelect from 'vue-select'
import AddBuilderButton from '@/components/buttons/AddBuilderButton.vue'
import EditBuilderButton from '@/components/buttons/EditBuilderButton.vue'
import AddJobButton from '@/components/buttons/AddJobButton.vue'
import EditJobButton from '@/components/buttons/EditJobButton.vue'
import AddHouseModelButton from '@/components/buttons/AddHouseModelButton.vue'
import EditHouseModelButton from '@/components/buttons/EditHouseModelButton.vue'
import axios from '@/axios'

const props = defineProps({
  modelValue: Object,
  isEditing: Boolean,
  isAbsence: Boolean
})

const emit = defineEmits([
  'update:modelValue',
  'update:builder',
  'update:job',
  'update:houseModel'
])

// Form values as props
const builderValue = ref(props.modelValue?.builder || '')
const jobValue = ref(props.modelValue?.job || '')
houseModelValue = ref(props.modelValue?.house_model || '')

// Local data
const builders = ref([])
const jobs = ref([])
const houses = ref([])

// Load initial data
fetchData()

async function fetchData() {
  await getBuilders()
  await getJobs()
  await getHouses()
}

async function getBuilders() {
  try {
    const response = await axios.get('/api/builders/')
    builders.value = response.data
  } catch (error) {
    console.error('Error fetching builders:', error)
  }
}

async function getJobs() {
  try {
    const response = await axios.get('/api/jobs/')
    jobs.value = response.data
  } catch (error) {
    console.error('Error fetching jobs:', error)
  }
}

async function getHouses() {
  try {
    const response = await axios.get('/api/houses/')
    houses.value = response.data
  } catch (error) {
    console.error('Error fetching houses:', error)
  }
}

function resetJob() {
  jobValue.value = ''
  houseModelValue.value = ''
}

function resetHouse() {
  houseModelValue.value = ''
}

function reloadBuilders({ builder, list }) {
  builders.value = list
  if (builder?.id) builderValue.value = builder.id
}

function onBuilderUpdated({ builder, list }) {
  builders.value = list
  if (builder?.id) builderValue.value = builder.id
}

function reloadJobs({ job, list }) {
  jobs.value = list
  if (job?.id) jobValue.value = job.id
}

function reloadHouseModels({ houseModel, list }) {
  houses.value = list
  if (houseModel?.id) houseModelValue.value = houseModel.id
}

const filteredJobs = computed(() => builderValue.value ? jobs.value.filter(j => j.builder === builderValue.value) : [])
const filteredHouses = computed(() => jobValue.value ? houses.value.filter(h => h.jobs.includes(jobValue.value)) : [])

const selectedBuilder = computed(() => builders.value.find(b => b.id === builderValue.value))
const selectedJob = computed(() => jobs.value.find(j => j.id === jobValue.value))
const selectedHouseModel = computed(() => houses.value.find(h => h.id === houseModelValue.value))

function focusNext(event, nextField) {
  event.preventDefault()
  const el = document.querySelector(`[ref='${nextField}'] input, select`)
  if (el) el.focus()
}

function selectText(event) {
  const input = event.target
  input.select()
}
</script>
