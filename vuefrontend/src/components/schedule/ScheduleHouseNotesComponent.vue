<template>
  <div class="card vh-80 mt-3">
    <div class="card-header">
      <nav>
        <div class="nav nav-tabs card-header-tabs" id="nav-tab" role="tablist">
          <button
            class="nav-link active"
            id="nav-notes-tab"
            data-bs-toggle="tab"
            data-bs-target="#nav-notes"
            type="button"
            role="tab"
            aria-controls="nav-notes"
            aria-selected="true">
            📝 Notes
          </button>
          <button
            class="nav-link"
            id="nav-folder-tab"
            data-bs-toggle="tab"
            data-bs-target="#nav-folder"
            type="button"
            role="tab"
            aria-controls="nav-folder"
            aria-selected="false">
            📁 Folder
          </button>
        </div>
      </nav>
    </div>

    <div class="card-body tab-content" id="nav-tabContent">
      <!-- Tab Notas -->
      <div
        class="tab-pane fade show active"
        id="nav-notes"
        role="tabpanel"
        aria-labelledby="nav-notes-tab"
        tabindex="0">
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
  import axios from 'axios';
  import EventImageAdmin from './EventImageAdmin.vue';

  export default {
    components: { EventImageAdmin },
    props: {
      eventId: Number, // Event object received from ScheduleEventModal
      required: true,
    },
    data() {
      return {
        websocket: null,
        wsUrl: null,
        showEditor: null,
        lastSavedHTML: '',
      };
    },
    mounted() {
      this.showEditor = this.hasPermission('appschedule.add_eventnote');
      this.checkUserIdentity();
      // Quill
      this.quill = new Quill(this.$refs.quillEditor, {
        theme: 'snow',
        placeholder: 'Write notes about the construction...',
      });

      // WebSocket + carga inicial
      this.wsUrl = `${process.env.VUE_APP_WS_BASE_URL}ws/schedule/event/${this.$props.eventId}/`;
      this.connectWebSocket();
      this.getNote();

      if (!this.showEditor) {
        this.quill.root.dataset.placeholder = '';
        this.quill.enable(false);
      }
    },
    beforeUnmount() {
      this.disconnectWebSocket();
    },

    methods: {
      // Insertar emojis en el cursor actual
      insertEmoji(emoji) {
        const sel = this.quill.getSelection();
        const pos = (sel && sel.index) ?? this.quill.getLength();
        this.quill.insertText(pos, ` ${emoji} `, 'user');
      },

      // Firma (usuario + timestamp) al final del documento
      insertSignature() {
        const now = new Date();
        const ts = now.toLocaleString(undefined, {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
        });

        const signatureHTML = `
        <p class="note-stamp" contenteditable="false">
          📝&nbsp; 
          <small>${this.userName}: ${ts}</small>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
      `.trim();

        const root = this.quill.root;
        const currentHTML = root.innerHTML.trim();

        // Evitar firma duplicada inmediata
        if (!currentHTML.endsWith(signatureHTML)) {
          // Si no termina en bloque, agrega salto
          if (!currentHTML.endsWith('</p>') && !currentHTML.endsWith('</div>')) {
            this.quill.insertText(this.quill.getLength() - 1, '\n', 'user');
          }
          const range = this.quill.getSelection();
          this.quill.setSelection(this.quill.getLength(), 0);
          this.quill.clipboard.dangerouslyPasteHTML(this.quill.getLength(), signatureHTML);
          if (range) this.quill.setSelection(range.index, range.length);
        }
      },

      async saveNote() {
        if (!this.showEditor) return;

        const currentHTMLBefore = this.quill.root.innerHTML.trim();
        if (currentHTMLBefore === this.lastSavedHTML) {
          this.notifyToastSuccess?.('Nothing changed.');
          return;
        }

        // Inserta firma y guarda
        this.insertSignature();
        const notesContent = this.quill.root.innerHTML.trim();

        const ok = await this.postNote({
          event: this.$props.eventId,
          notes: notesContent,
        });
        if (!ok) {
          this.notifyError?.('Could not save message');
          return;
        }

        this.lastSavedHTML = notesContent;
        this.notifyToastSuccess?.('Note saved with signature.');
      },

      connectWebSocket() {
        this.websocket = new WebSocket(this.wsUrl);
        this.websocket.onmessage = event => {
          const data = JSON.parse(event.data);
          if (data.type === 'note.updated') {
            this.quill.root.innerHTML = data.event.notes;
            this.lastSavedHTML = data.event.notes?.trim() || '';
            if (this.showEditor) this.notifyToastSuccess?.('Message has been updated successfully');
          }
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
          const { data, status } = await axios.get(`/api/events/${this.$props.eventId}/note/`);
          if (status === 200) {
            this.quill.root.innerHTML = data.notes;
            this.lastSavedHTML = (data.notes || '').trim();
          }
        } catch (e) {
          console.error('Error fetching notes data:', e);
        }
      },

      async postNote(payload) {
        try {
          const resp = await axios.post(`/api/events/${this.$props.eventId}/note/`, payload);
          return [200, 201].includes(resp.status);
        } catch (e) {
          console.error('Error saving note:', e);
          return false;
        }
      },
      checkUserIdentity() {
        const token = localStorage.getItem('authToken');
        this.isLoggedIn = !!token;
        if (this.isLoggedIn) {
          this.getAuthenticatedUser().then(user => {
            if (user) {
              this.userName = user.username;
            }
          });
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
