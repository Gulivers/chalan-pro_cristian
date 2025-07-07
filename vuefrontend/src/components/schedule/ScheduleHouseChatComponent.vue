<template>
  <div class="h-100">
    <div class="d-flex flex-column h-100 p-lg-3 p-1">
      <!-- Debug: Show received eventId prop -->
      <div class="alert alert-info" v-if="debugMode">
        <strong>Debug:</strong> eventId = {{ eventId }}
      </div>

      <!-- Chat window with full height -->
      <div class="chat-window border rounded p-3 d-flex flex-column flex-grow-1">
        <h5 class="border-bottom pb-2">Chat for Job ID: {{ eventId }}</h5>

        <div class="chat-messages d-flex flex-column overflow-auto">
          <div v-for="message in messages" :key="message.id" class="my-2 p-2 rounded d-inline-block" style="max-width: 95%"
               :class="message.user?.id === user?.id ? 'bg-light text-black ms-auto ' : 'bg-secondary text-white me-auto'">
            <div class="w-100" style="font-size: .7rem">{{message.user?.username}} : {{parseDate(message.timestamp)}}</div>
            {{ message.message }}
          </div>
        </div>
      </div>

      <div class="mt-3 d-flex">
        <input v-model="newMessage" @keyup.enter="sendMessage" class="form-control me-2"
               placeholder="Type a message..." :disabled="!canSendMessage">
        <button @click="sendMessage" class="btn btn-outline-success" :disabled="!canSendMessage">
          <img src="@assets/img/ico-send.svg" alt="Add" width="25" height="25">
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import '@assets/css/base.css';
import axios from "axios";
import {useAuthStore} from '@stores/auth'
import dayjs from 'dayjs'

export default {
  props: {
    eventId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      user: null,
      newMessage: '',
      messages: [],
      websocket: null,
      wsUrl: null,
      canSendMessage: null,
      debugMode: false
    };
  },
  mounted() {
    const authStore = useAuthStore()
    this.user = authStore.user.value
    this.canSendMessage = this.hasPermission('appschedule.add_eventchatmessage')
    this.wsUrl = `${process.env.VUE_APP_WS_BASE_URL}ws/schedule/event/${this.$props.eventId}/chat/`
    console.log(`connect to WS event ${this.wsUrl}`)
    this.connectWebSocket()
    this.getMessages()

  },
  beforeUnmount() {
    this.disconnectWebSocket();
  },
  methods: {
    parseDate(date){
      const timestamp = dayjs(date)
      return timestamp.format('MMM DD, HH:mm')
    },
    async sendMessage() {
      if (this.newMessage.trim() === '') {
        return
      }
      try {
        const response = await axios.post(`/api/events/${this.$props.eventId}/chat/messages/`, {
          message: this.newMessage.trim(),
          event: this.$props.eventId,
        });
        if ([201, 200].includes(response.status)) {
          // this.messages.push(response.data)
          this.newMessage = ''
          console.log('mensaje guardado')
        } else {
          console.log('response error:', response)
        }
      } catch (e) {
        console.error(e)
      }
    },
    connectWebSocket() {
      this.websocket = new WebSocket(this.wsUrl);
      this.websocket.onopen = () => {
        console.log('Conexión WebSocket establecida.');
      };

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'chat.updated') {
          this.messages.push(data.data)
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
    async getMessages() {
      try {
        const response = await axios.get(`/api/events/${this.$props.eventId}/chat/messages/`);
        if (response.status === 200) {
          console.log(this.user)
          console.log('getMessages:', response.data)
          this.messages = response.data
        }
      } catch (error) {
        console.error('Error fetching event chats data:', error);
      }
    },
  }
};
</script>

<style>
.chat-messages {
  max-height: 60vh;
  overflow-y: auto;
  padding-bottom: 10px;
}

.container-fluid {
  height: 100%;
}

.chat-window {
  height: 100%;
  min-height: 200px;
}
</style>
