
import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';

const LoginView = () => import('@views/LoginView.vue');
const HomeView = () => import('@views/HomeView.vue');
const JobMap = () => import('@components/houses/JobMap.vue');
const PasswordReset = () => import('@components/PasswordReset.vue');
const PasswordResetConfirm = () => import('@components/PasswordResetConfirm.vue');
const AboutView = () => import('@views/AboutView.vue');
const ContractFormComponent = () => import('@components/contracts/ContractFormComponent.vue');
const WorkPriceFormComponent = () => import('@components/contracts/WorkPriceFormComponent.vue');
const WorkPricesBuilderComponent = () => import('@components/contracts/WorkPricesBuilderComponent.vue');
const WeeklySummaryListComponent = () => import('@components/contracts/WeeklySummaryListComponent.vue');
const ScheduleComponent = () => import('@components/schedule/ScheduleComponent.vue');
const ScheduleHouseChatsGeneralComponent = () => import('@components/schedule/ScheduleHouseChatsGeneralComponent.vue');
const ContractView = () => import('@views/contract/ContractView.vue');
const WorkPricesView = () => import('@views/contract/WorkPricesView.vue');
const SupervisorCommunitiesList = () => import('@components/houses/SupervisorCommunitiesList.vue');
const IdentitySettings = () => import('@components/appidentity/IdentitySettings.vue');
const IdentitySettingsAdministrador = () => import('@components/appidentity/IdentitySettingsAdministrador.vue');

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { hideNavbar: true },
  },
  {
    path: '/logout',
    name: 'logout',
    beforeEnter: (to, from, next) => {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userPermissions');
      next({ name: 'login' });
    }
  },
  {
    path: "/map",
    name: "JobMap",
    component: JobMap,
    meta: { requiresAuth: true, requiredPermissions: [] }
  },
  {
    path: "/supervisor-communities",
    name: "SupervisorCommunitiesList",
    component: SupervisorCommunitiesList,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.add_contract'] }
  },
  {
    path: '/reset_password',
    name: 'reset_password',
    component: PasswordReset,
  },
  {
    path: '/reset-password-confirm',
    component: PasswordResetConfirm,
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true, requiredPermissions: [] }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { requiresAuth: false, requiredPermissions: [], }
  },
  {
    path: '/contracts',
    name: 'contracts',
    component: ContractView,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_contract'] }
  },
  {
    path: '/contract-form',
    name: 'contract-form',
    component: ContractFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.add_contract'] }
  },
  {
    path: '/contract-edit/edit/:id',
    name: 'contract-edit',
    component: ContractFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.change_contract'] }
  },
  {
    path: '/contract-view/view/:id',
    name: 'contract-view',
    component: ContractFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_contract'] }
  },
  {
    path: '/work-prices',
    name: 'work-prices',
    component: WorkPricesView,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_workprice'] }
  },
  {
    path: '/work-prices-form',
    name: 'work-prices-form',
    component: WorkPriceFormComponent,
    props: true,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.add_workprice'] }
  },
  {
    path: '/work-prices/edit/:id',
    name: 'work-prices-edit',
    component: WorkPriceFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.change_workprice'] }
  },
  {
    path: '/work-prices/view/:id',
    name: 'work-prices-view',
    component: WorkPriceFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_workprice'] }
  },
  {
    path: '/work-prices-builders',
    name: 'work-prices-builders',
    component: WorkPricesBuilderComponent,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_workprice'] }
  },
  {
    path: '/weekly-summary-list/',
    name: 'weekly-summary-list',
    component: WeeklySummaryListComponent,
    props: true,
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.view_contract'] }
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: ScheduleComponent,
    meta: { requiresAuth: true, requiredPermissions: ['appschedule.view_event'] }
  },
  {
    path: '/chat-general',
    name: 'chat-general',
    component: ScheduleHouseChatsGeneralComponent,
    meta: { requiresAuth: true, requiredPermissions: ['appschedule.view_event'] }
  },
  {
    path: '/settings',
    name: 'identity-settings',
    component: IdentitySettings,
    meta: { requiresAuth: true }  
  },
  {
    path: '/settings-administrador',
    name: 'settings-administrador',
    component: IdentitySettingsAdministrador,
    meta: { requiresAuth: true }
  },
]



const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach(async (to, from, next) => {
  const authToken = localStorage.getItem('authToken');
  console.log(`Auth Token in Router>>: ${authToken ? 'true' : 'false'}`);
  const userPermissions = JSON.parse(localStorage.getItem('userPermissions') || '[]');
  //console.log(`User Permissions in Router>>: ${JSON.stringify(userPermissions)}`);

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authToken) {
      next({ name: 'login' });
    } else {
      try {
        const response = await axios.get('/api/validate-token/', {
          headers: { 'Authorization': `Token ${authToken}` }
        });

        if (response.data.valid) {
          const requiredPermissions = to.meta.requiredPermissions || [];
          const userPermissionsArray = userPermissions.permissions || [];
          const userPermissionsSet = new Set(userPermissionsArray);

          const hasPermission = requiredPermissions.length === 0 ||
            requiredPermissions.every(permission => userPermissionsSet.has(permission));
          console.log('Has permission:', hasPermission);

          if (hasPermission) {
            next();
          } else {
            alert('You do not have permission to access this page');
            next(false);
          }
        } else {
          localStorage.removeItem('authToken');
          localStorage.removeItem('userPermissions');
          next({ name: 'login' });
        }
      } catch (error) {
        console.error('Error validating token:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('userPermissions');
        next({ name: 'login' });
      }
    }
  } else {
    next();
  }
});

export default router;