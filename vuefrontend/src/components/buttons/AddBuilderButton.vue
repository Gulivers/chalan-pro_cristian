<template>
  <div class="d-inline-block">
    <button
      class="btn btn-outline-secondary btn-sm ms-1"
      type="button"
      @click="openBuilderModal"
      :disabled="isDisabled"
    >
      <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15">
    </button>

    <BuilderModal
      ref="builderModal"
      :action="action"
      :builder="builderData"
      @saved="handleSaved"
      @close="closeModal"
      @clearBuilderSelect="clearBuilderSelection"
    />
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import BuilderModal from '@/components/contracts/BuilderModalComponent.vue'
import axios from 'axios'

const props = defineProps({
  isDisabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['builder-added'])

const action = ref('add')
const builderData = ref({
  name: '',
  trim_amount: 0,
  rough_amount: 0,
  travel_price_amount: 0
})

const builderModal = ref(null)

function openBuilderModal() {
  action.value = 'add'
  builderData.value = {
    name: '',
    trim_amount: 0,
    rough_amount: 0,
    travel_price_amount: 0
  }
  builderModal.value?.showModal()
}

function closeModal() {
  builderModal.value?.hideModal()
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove())
}

function clearBuilderSelection() {
  // Este evento puede ser escuchado externamente si se requiere.
  emit('clear-builder-select')
}

function handleSaved() {
  axios.get('/api/builder/')
    .then(response => {
      const builderList = response.data;

      // Encuentra el último builder añadido comparando IDs
      const newestBuilder = builderList.reduce((latest, b) =>
        !latest || b.id > latest.id ? b : latest, null
      );

      emit('builder-added', {
        builder: newestBuilder,
        list: builderList
      });
    })
    .catch(error => {
      console.error('Error reloading builders:', error);
    });
}
</script>
