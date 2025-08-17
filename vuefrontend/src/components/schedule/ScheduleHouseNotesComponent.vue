<template>
  <div class="card vh-80 mt-3">
    <div class="card-header">
      <nav>
        <div class="nav nav-tabs card-header-tabs" id="nav-tab" role="tablist">
          <button class="nav-link active" id="nav-notes-tab" data-bs-toggle="tab" data-bs-target="#nav-notes" type="button" role="tab" aria-controls="nav-notes" aria-selected="true">
            📝 Notes
          </button>
          <button class="nav-link" id="nav-folder-tab" data-bs-toggle="tab" data-bs-target="#nav-folder" type="button" role="tab" aria-controls="nav-folder" aria-selected="false">
            📁 Folder
          </button>
        </div>
      </nav>
    </div>

    <div class="card-body tab-content" id="nav-tabContent">
      <!-- Tab Notas -->
      <div class="tab-pane fade show active" id="nav-notes" role="tabpanel" aria-labelledby="nav-notes-tab" tabindex="0">
        <h4 class="text-center mb-3">House Notes</h4>
        <div ref="quillEditor" class="quill-editor"></div>

        <div class="d-flex justify-content-between align-items-center flex-wrap mt-3">
          <div class="status-buttons" v-if="showEditor">
            <button class="btn btn-outline-success btn-sm me-1 mb-1" @click="insertEmoji('✅')">Mark as Done ✅</button>
            <button class="btn btn-outline-info btn-sm me-1 mb-1" @click="insertEmoji('😃')">Completed 😃</button>
            <button class="btn btn-outline-warning btn-sm me-1 mb-1" @click="insertEmoji('⚠️')">Alert ⚠️</button>
            <button class="btn btn-outline-danger btn-sm me-1 mb-1" @click="insertEmoji('⏳')">Delayed ⏳</button>
            <button class="btn btn-outline-dark btn-sm me-1 mb-1" @click="insertEmoji('🔥')">Critical 🔥</button>
          </div>
          <button class="btn btn-primary mt-2" @click="saveNote" :disabled="!showEditor">💾 Save Note</button>
        </div>
      </div>

      <!-- Tab Folder -->
      <div class="tab-pane fade" id="nav-folder" role="tabpanel" aria-labelledby="nav-folder-tab" tabindex="0">
        <EventImageAdmin :eventId="eventId" />
      </div>
    </div>
  </div>
</template>

<script>
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import axios from "axios";
import EventImageAdmin from './EventImageAdmin.vue';

export default {
  components: {
    EventImageAdmin, 
  },
  props: {
    eventId: Number, // Event object received from ScheduleEventModal
    required: true
  },
  data() {
    return {
      websocket: null,
      wsUrl: null,
      showEditor: null,
    }
  },
  mounted() {
    this.showEditor = this.hasPermission('appschedule.add_eventnote')
    this.quill = new Quill(this.$refs.quillEditor, {
      theme: 'snow',
      placeholder: 'Write notes about the construction...',
    });

    this.wsUrl = `${process.env.VUE_APP_WS_BASE_URL}ws/schedule/event/${this.$props.eventId}/`
    console.log(`connect to WS event ${this.wsUrl}`)
    this.connectWebSocket()
    this.getNote()
    if (!this.showEditor){
      this.quill.root.dataset.placeholder = ''
      this.quill.enable(false)
    }
  },
  beforeUnmount() {
    console.log('unmounted quilljs')
    this.disconnectWebSocket();
  },

  methods: {
    // Método para insertar emojis de estado en el cursor actual
    insertEmoji(emoji) {
      const cursorPosition = this.quill.getSelection()?.index || 0;
      this.quill.insertText(cursorPosition, ` ${emoji} `, "user");
    },
    async saveNote() {
      const notesContent = this.quill.root.innerHTML;
      const resp = await this.postNote({
        event: this.$props.eventId,
        notes: notesContent
      })
      if (!resp) {
        this.notifyError('Could not save message')
      }
    },

    connectWebSocket() {
      this.websocket = new WebSocket(this.wsUrl);
      this.websocket.onopen = () => {
        console.log('Conexión WebSocket establecida.');
      };

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'note.updated') {
          this.quill.root.innerHTML = data.event.notes
          if(this.showEditor){
            this.notifyToastSuccess('Message has been updated successfully')
          }
        }
      };

      this.websocket.onclose = () => {
        console.log('Conexión WebSocket cerrada.');
        // Opcional: Intenta reconectar después de un tiempo
        // setTimeout(this.connectWebSocket, 3000);
      };

      this.websocket.onerror = (error) => {
        console.error('Error de WebSocket:', error);
      };
    },

    disconnectWebSocket() {
      if (this.websocket) {
        this.websocket.close();
        this.websocket = null;
      }
    },

    async getNote() {
      try {
        const response = await axios.get(`/api/events/${this.$props.eventId}/note/`);
        if (response.status === 200) {
          const data = response.data
          this.quill.root.innerHTML = data.notes
        }
      } catch (error) {
        console.error('Error fetching notes data:', error);
      }
    },
    async postNote(payload) {
      try {
        const response = await axios.post(`/api/events/${this.$props.eventId}/note/`, payload);
        if ([200, 201].includes(response.status)) {
          console.log(response.data)
          return true
        }
      } catch (error) {
        console.error('Error saving note:', error);
        return false
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
  text-align: center;
}

.quill-editor {
  min-height: max(200px, 30vh);
  border: 1px solid #ccc;
  padding: 10px;
}

.status-buttons {
  margin-bottom: 10px;
}

.status-buttons button {
  margin: 5px;
}

.quill-editor {
  min-height: max(200px, 30vh);
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
.status-buttons button {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}
</style>