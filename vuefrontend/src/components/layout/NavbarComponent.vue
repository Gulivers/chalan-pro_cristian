<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-body">
    <div class="container">
      <a class="navbar-brand" href="/">CHALAN-PRO</a>
      <button class="navbar-toggler" type="button" @click="toggleNavbar" aria-controls="navbarNav" aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div :class="['collapse', 'navbar-collapse', { 'show': isNavbarOpen }]" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <!-- Loop through menuItems -->
          <li v-for="(item, index) in menuItems" :key="index" class="{ 'dropdown': item.children, 'active': isDropdownActive(item) }" :class="{ 'dropdown': item.children }">
            <!-- Dropdown -->
            <template v-if="item.children">
              <a class="nav-link dropdown-toggle" href="#" role="button" :class="{ 'text-orange': isDropdownActive(item) }"
                @click.prevent="toggleDropdown(index)">
                {{ item.text }}
              </a>
              <ul class="dropdown-menu" :class="{ 'show': item.isOpen }">
                <li v-for="(subItem, subIndex) in item.children" :key="subIndex">
                  <router-link :to="subItem.route" class="dropdown-item" @click="closeNavbar">
                    {{ subItem.text }}
                  </router-link>
                </li>
              </ul>
            </template>
            <!-- Regular Menu Item -->
            <template v-else>
              <router-link :to="item.route" class="nav-link" @click="closeNavbar">{{ item.text }}</router-link>
            </template>
          </li>

          <!-- Authentication Links -->
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link" @click="closeNavbar">Log In</router-link>
          </li>
          <li class="nav-item" v-else>
            <router-link to="/logout" class="nav-link" @click="logout">Log Out</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <span class="nav-link">Welcome, {{ userName }}</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,
      isNavbarOpen: false,
      menuItems: [
        { text: 'Dashboard', route: '/' },
        {
          text: 'Schedule',
          isOpen: false, // Controls dropdown state
          children: [
            {text: 'Schedule', route: '/schedule'},
            {text: 'Job Communications', route: '/chat-general'}
          ]
        },
        { text: 'Contracts', route: '/contracts' },
        {
          text: 'Piece Work Prices',
          isOpen: false, // Controls dropdown state
          children: [
            { text: 'Piece Work Prices', route: '/work-prices' },
            { text: 'Work Prices per Builder', route: '/work-prices-builders' }
          ]
        },
        {
          text: 'Communities',
          isOpen: false, 
          children: [
            { text: 'Communities Map', route: '/map' },
            { text: 'Supervisor Communities', route: '/supervisor-communities' }
          ]
        },
        { 
          text: 'Settings',
          isOpen: false, 
          children: [
            { text: 'Me', route: '/settings' }, // This should match the route for IdentitySettings
            { text: 'Administrador', route: '/settings-administrador' },
          ]
          },
        { text: 'About', route: '/about' },
      ],
      userName: ''
    };
  },
  computed: {
    isDropdownActive() {
      return (item) => {
        return item.children && item.children.some(subItem => this.$route.path === subItem.route);
      };
    }
  },
  mounted() {
    this.checkUserIdentity();
  },
  methods: {
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
    toggleDropdown(index) {
      this.menuItems.forEach((item, i) => {
        if (i === index) {
          item.isOpen = !item.isOpen;
        } else {
          item.isOpen = false;
        }
      });
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userPermissions');
      this.isLoggedIn = false;
      this.$router.push('/login');
      this.closeNavbar();
    },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    closeNavbar() {
      this.isNavbarOpen = false;
      this.menuItems.forEach(item => {
        if (item.children) {
          item.isOpen = false;
        }
      });
    }
  },
  watch: {
    $route() {
      this.checkUserIdentity();
      this.closeNavbar();
    }
  }
};
</script>

<style scoped>
/*
// Ahora se ejeculan los colores del navbar en el src\assets\scss\custom-bootstrap.scss 
.navbar {
  background-color: #4e73df;
  background-image: linear-gradient(180deg, #395ecb 35%, #0c35b1 100%);
}

nav {
  padding: 12px;
}

nav a {
  font-weight: bold;
  color: #e5e8eb;
}

nav .nav-link.router-link-exact-active {
  color: #ff931e;
}

/* Dropdown Styling */
/*
.dropdown-menu {
  background-color: #4e73df;
  background-image: linear-gradient(180deg, #395ecb 35%, #0c35b1 100%);
  display: none;
  position: absolute;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  color: rgb(255, 255, 255);
}

.dropdown-item:hover {
  background-color: #4e73df;
}

/* Dropdown items turn orange */
.text-orange {
  color: #ff931e !important;
  font-weight: bold;
}
.dropdown-item.router-link-exact-active {
  color: #ff931e !important;
  font-weight: bold;
}

/* Ensure dropdown works on mobile */
/*
@media (max-width: 991.98px) {
  .navbar-nav {
    padding-top: 1rem;
  }

  .nav-item {
    padding: 0.5rem 0;
  }

  .dropdown-menu {
    position: relative;
    width: 100%;
  }
}
*/
</style>
