<template>
  <div class="vh-80 pt-3">
    <h4 class="text-center mb-3">House Notes</h4>
    <div ref="quillEditor" class="quill-editor"></div>

    <button class="btn btn-primary mt-3 ms-2" @click="saveNote"
            :disabled="!showEditor">Save Note
    </button>

    <div class="status-buttons pt-3" v-if="showEditor">
      <button class="btn btn-outline-success" @click="insertEmoji('✅')"
              style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
        Mark as Done ✅
      </button>
      <button class="btn btn-outline-info" @click="insertEmoji('😃')"
              style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
        Completed 😃
      </button>
      <button class="btn btn-outline-warning" @click="insertEmoji('⚠️')"
              style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
        Alert ⚠️
      </button>
      <button class="btn btn-outline-danger" @click="insertEmoji('⏳')"
              style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
        Delayed ⏳
      </button>
      <button class="btn btn-outline-dark" @click="insertEmoji('🔥')"
              style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
        Critical 🔥
      </button>
    </div>
  </div>
</template>

<script>
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import axios from "axios";

export default {
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
</style>