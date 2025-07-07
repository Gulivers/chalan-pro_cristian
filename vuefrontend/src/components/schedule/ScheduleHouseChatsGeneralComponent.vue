<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar de eventos -->
      <div class="col-md-5 col-lg-4 col-xl-3 border-end p-3 bg-light">
        <div class="row pb-2" ref="leftHeader">
          <div class="col-4 text-start"><h3 class="mb-0">Jobs</h3></div>
          <div class="col-8 text-end">
            <div class="input-group">
              <input
                type="text"
                class="form-control rounded-0"
                v-model="search"
                placeholder="Search event"
                @keydown.enter="getEvents" />
              <button class="btn btn-primary rounded-0" type="button" @click="getEvents">
                <search-icon></search-icon>
              </button>
            </div>
          </div>
        </div>

        <ul class="list-group events-list" ref="events" :style="eventsMaxHeightStyle">
          <li
            v-for="event in events"
            :key="event.id"
            @click="selectEvent(event)"
            class="list-group-item list-group-item-action"
            :class="{ active: selectedEvent && selectedEvent.id === event.id }">
            <div class="row">
              <div class="col-4 text-start d-flex align-items-center">
                {{ event.crew_title }}
              </div>
              <div class="col-8 d-flex justify-content-between align-items-center">
                <span class="text-truncate">{{ event.title }}</span>
                <span class="badge text-bg-warning" v-if="unreadMessages[event.id]">
                  {{ unreadMessages[event.id] }}
                </span>
              </div>
              <small class="text-muted text-end mt-1">
                <span class="badge text-bg-danger me-2" v-if="event.extended_service">Ext. Service</span>
                {{ event.date }}
              </small>
            </div>
          </li>
        </ul>
        <div class="row">
          <div class="col-12 mt-2">
            <button
              type="button"
              class="btn btn-primary btn-sm me-2"
              :disabled="!previous || loading"
              @click="handlePrevious">
              Previous
            </button>
            <button type="button" class="btn btn-primary btn-sm" :disabled="!next || loading" @click="handleNext">
              Next
            </button>
          </div>
        </div>
      </div>

      <!-- Chat window -->
      <div class="col-md-7 col-lg-8 col-xl-9 d-flex flex-column p-2" :style="contentMaxHeightStyle">
        <div v-if="selectedEvent" class="chat-window border rounded p-2 d-flex flex-column flex-grow-1">
          <ScheduleHouseDiscussion v-if="selectedEvent" :event="selectedEvent" />
        </div>
        <div class="d-flex align-items-center h-100" v-if="loading">
          <h2 class="text-center w-100">Preparing event...</h2>
        </div>
        <div class="d-flex align-items-center h-100" v-if="!loading && !selectedEvent">
          <h2 class="text-center w-100">Please select an event first.</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import '@assets/css/base.css';
  import axios from 'axios';
  import dayjs from 'dayjs';
  import ScheduleHouseDiscussion from '@schedule/ScheduleHouseDiscussion.vue';
  import { useAuthStore } from '@stores/auth';
  import SearchIcon from '@components/icons/searchIcon.vue';

  export default {
    components: { SearchIcon, ScheduleHouseDiscussion },
    data() {
      return {
        events: [],
        next: null,
        previous: null,
        page: 1,
        selectedEvent: null,
        search: '',
        duration: null,
        loading: false,
        leftHeaderHeight: 0,
        mainNavHeight: 0,
        mainFooterHeight: 0,
        unreadMessages: {},
        wsNotify: null,
        userId: null,
      };
    },
    methods: {
      async getEvents(event, page = 1) {
        this.page = page;
        this.selectedEvent = null;

        try {
          const url_get = `/api/my-events/?page=${this.page}${this.search.trim() ? '&search=' + this.search : ''}`;
          const response = await axios.get(url_get);

          if (response.status === 200) {
            this.events = response.data.results;
            this.next = response.data.next;
            this.previous = response.data.previous;

            // Carga los mensajes no leídos
            const unreadRes = await axios.get('/api/unread-chat-counts/');
            this.unreadMessages = unreadRes.data;

            // Ordenar eventos por mensajes no leídos
            this.events.sort((a, b) => {
              const aUnread = this.unreadMessages[a.id] || 0;
              const bUnread = this.unreadMessages[b.id] || 0;
              return bUnread - aUnread;
            });
          }
        } catch (error) {
          console.error('Error fetching event data:', error);
        }
      },
      async selectEvent(event) {
        this.selectedEvent = null;
        this.loading = true;

        // Marcar como leído
        try {
          await axios.post(`/api/mark-chat-read/${event.id}/`);
          this.unreadMessages[event.id] = 0;
        } catch (error) {
          console.warn('Failed to mark chat as read:', error);
        }

        setTimeout(() => {
          this.loading = false;
          this.selectedEvent = event;
        }, 500);
      },
      updateHeights() {
        if (this.$refs.leftHeader) {
          this.leftHeaderHeight = this.$refs.leftHeader.offsetHeight;
        }
        const nav = document.querySelector('nav');
        if (nav) {
          this.mainNavHeight = nav.offsetHeight;
        }
        const footer = document.querySelector('footer');
        if (footer) {
          this.mainFooterHeight = footer.offsetHeight;
        }
      },
      handleNext() {
        this.getEvents(null, this.page + 1);
      },
      handlePrevious() {
        this.getEvents(null, this.page - 1);
      },
      connectUnreadWebSocket() {
        if (!this.userId) return;

        this.wsNotify = new WebSocket(`${process.env.VUE_APP_WS_BASE_URL}ws/schedule/unread/user/${this.userId}/`);

        this.wsNotify.onopen = () => {
          console.log('[WS] Connected to unread counter for user', this.userId);
        };

        this.wsNotify.onmessage = event => {
          const data = JSON.parse(event.data);

          if (data.type === 'unread.updated') {
            const { event_id, count, user_id } = data;

            // Filtro defensivo: si el mensaje viene del mismo usuario, ignorarlo
            if (user_id && user_id === this.userId) {
              return;
            }

            // Solo actualizar el contador si es para otro usuario
            this.$set(this.unreadMessages, event_id, count);
          }
        };

        this.wsNotify.onclose = () => {
          console.warn('[WS] Unread socket closed');
        };
      },
      disconnectUnreadWebSocket() {
        if (this.wsNotify) {
          this.wsNotify.close();
          this.wsNotify = null;
        }
      },
      async getAuthenticatedUser() {
        try {
          const response = await axios.get('/api/user_detail/');
          return response.data;
        } catch (error) {
          console.error('Error fetching authenticated user:', error);
          return {};
        }
      },
    },
    computed: {
      eventsMaxHeightStyle() {
        const calculatedHeight = `calc(100vh - ${this.leftHeaderHeight}px - ${this.mainNavHeight}px - ${this.mainFooterHeight}px)`;
        return {
          height: calculatedHeight,
          minHeight: '400px',
          overflowY: 'auto',
        };
      },
      contentMaxHeightStyle() {
        const calculatedHeight = `calc(100vh - ${this.mainNavHeight}px - ${this.mainFooterHeight}px)`;
        return {
          minHeight: calculatedHeight,
          overflowY: 'auto',
        };
      },
    },
    async mounted() {
      const data = await this.getAuthenticatedUser();
      const authStore = useAuthStore();
      authStore.setUser(data);
      this.userId = data.id;
      this.connectUnreadWebSocket();

      this.updateHeights();
      this.getEvents();
    },
    beforeUnmount() {
      this.disconnectUnreadWebSocket();
    },
  };
</script>
