<template>
  <div class="d-inline-block">
    <button
      class="btn btn-outline-secondary btn-sm ms-1"
      type="button"
      @click="openBuilderModal"
      :disabled="isDisabled"
    >
      <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15">
    </button>

    <BuilderModal
      ref="builderModal"
      :action="'edit'"
      :builder="builderData"
      @saved="handleSaved"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import BuilderModal from '@/components/contracts/BuilderModalComponent.vue'
import axios from 'axios'

const props = defineProps({
  isDisabled: {
    type: Boolean,
    default: false
  },
  builder: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['builder-updated'])

const builderData = ref({ ...props.builder })
const builderModal = ref(null)

watch(() => props.builder, (newVal) => {
  builderData.value = { ...newVal }
})

function openBuilderModal() {
  builderData.value = { ...props.builder }
  builderModal.value?.showModal()
}

function closeModal() {
  builderModal.value?.hideModal()
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove())
}

function handleSaved() {
  // Volvemos a consultar la lista completa para estar seguros
  axios.get('/api/builder/')
    .then(response => {
      const updated = response.data.find(b => b.id === props.builder.id)
      emit('builder-updated', {
        builder: updated,
        list: response.data
      })
    })
    .catch(error => {
      console.error('Error fetching builders after edit:', error)
    })
}
</script>
