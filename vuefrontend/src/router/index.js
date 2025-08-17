
import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';

// ───────────────────────────────────────────────────────────
// LAZY IMPORTS (ordenado por módulos)
// ───────────────────────────────────────────────────────────

const LoginView = () => import('@views/LoginView.vue');
const HomeView = () => import('@views/HomeView.vue');
const AboutView = () => import('@views/AboutView.vue');
const JobMap = () => import('@components/houses/JobMap.vue');
const SupervisorCommunitiesList = () => import('@components/houses/SupervisorCommunitiesList.vue');
const PasswordReset = () => import('@components/PasswordReset.vue');
const PasswordResetConfirm = () => import('@components/PasswordResetConfirm.vue');

// Contracts
const ContractView = () => import('@views/contract/ContractView.vue');
const ContractFormComponent = () => import('@components/contracts/ContractFormComponent.vue');
const WorkPricesView = () => import('@views/contract/WorkPricesView.vue');
const WorkPriceFormComponent = () => import('@components/contracts/WorkPriceFormComponent.vue');
const WorkPricesBuilderComponent = () => import('@components/contracts/WorkPricesBuilderComponent.vue');
const WeeklySummaryListComponent = () => import('@components/contracts/WeeklySummaryListComponent.vue');

// Schedule & Chat
const ScheduleComponent = () => import('@components/schedule/ScheduleComponent.vue');
const ScheduleHouseChatsGeneralComponent = () => import('@components/schedule/ScheduleHouseChatsGeneralComponent.vue');

// Inventory
const ProductForm = () => import('@components/inventory/ProductForm.vue');
const WarehouseListView = () => import('@views/inventory/WarehouseListView.vue');
const WareHouseFormComponent = () => import('@components/inventory/WarehouseFormComponent.vue');
const DynamicForm = () => import('@components/inventory/DynamicForm.vue');
const ProductCategoryView = () => import('@views/inventory/ProductCategoryView.vue');
const ProductBrandView = () => import('@views/inventory/ProductBrandView.vue');
const ProductUnitView = () => import('@views/inventory/ProductUnitView.vue');
const UnitOfMeasureView = () => import('@views/inventory/UnitOfMeasureView.vue');
const UnitCategoryView = () => import('@views/inventory/UnitCategoryView.vue');
const PriceTypeView = () => import('@views/inventory/PriceTypeView.vue');
const ProductListView = () => import('@views/inventory/ProductListView.vue');

// Transactions
const DocTypeListView = () => import('@views/transactions/DocTypeListView.vue');
const DocTypeFormComponent = () => import('@components/transactions/DocTypeFormComponent.vue.vue');


// ───────────────────────────────────────────────────────────
// EXPORT ROUTER
// ───────────────────────────────────────────────────────────

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
    // props: true,
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
    meta: { requiresAuth: true, requiredPermissions: ['ctrctsapp.change_workprice'] }
  },
  {
    path: '/weekly-summary-list/',
    name: 'weekly-summary-list',
    component: WeeklySummaryListComponent,
    // props: true,
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

  
  // ───────────────────────────────────────────────────────────
  // INVENTORY MODULE                                        
  // ───────────────────────────────────────────────────────────
  {
    path: '/warehouses',
    name: 'warehouses',
    component: WarehouseListView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_warehouse'] },
  },
  {
    path: '/warehouse-form',
    name: 'warehouse-form',
    component: WareHouseFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_warehouse'] },
  },
  {
    path: '/warehouse/view/:id',
    name: 'warehouse-view',
    component: WareHouseFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_warehouse'] },
  },
  {
    path: '/warehouse/edit/:id',
    name: 'warehouse-edit',
    component: WareHouseFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_warehouse'] },
  },
  {
    path: '/product-categories',
    name: 'product-categories',
    component: ProductCategoryView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productcategory'] },
  },
  {
    path: '/admin/product-category/form',
    name: 'product-category-form',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_productcategory'] },
    props: () => ({
      schemaEndpoint: '/api/schema/product-category/',
      apiEndpoint: '/api/productcategory/',
      formTitle: 'Create Product Category',
      redirectAfterSave: '/product-categories',
      readOnly: false,
      objectId: null,
    }),
  },
  {
    path: '/admin/product-category/view/:id',
    name: 'product-category-view',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productcategory'] },
    props: route => ({
      schemaEndpoint: '/api/schema/productcategory/',
      apiEndpoint: '/api/productcategory/',
      objectId: route.params.id,
      formTitle: 'View Product Category',
      readOnly: true,
    }),
  },
  {
    path: '/admin/product-category/edit/:id',
    name: 'product-category-edit',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_productcategory'] },
    props: route => ({
      schemaEndpoint: '/api/schema/productcategory/',
      apiEndpoint: '/api/productcategory/',
      objectId: route.params.id,
      formTitle: 'Edit Product Category',
      redirectAfterSave: '/product-categories',
      readOnly: false,
    }),
  },
  {
    path: '/product-brands',
    name: 'product-brands',
    component: ProductBrandView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productbrand'] },
  },
  {
    path: '/admin/product-brand/form',
    name: 'product-brand-form',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_productbrand'] },
    props: {
      schemaEndpoint: '/api/schema/productbrand/',
      apiEndpoint: '/api/productbrand/',
      formTitle: 'Create Product Brand',
      readOnly: false,
      objectId: null,
      redirectAfterSave: '/product-brands',
    },
  },
  {
    path: '/admin/product-brand/edit/:id',
    name: 'product-brand-edit',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_productbrand'] },
    props: route => ({
      schemaEndpoint: '/api/schema/productbrand/',
      apiEndpoint: '/api/productbrand/',
      objectId: route.params.id,
      formTitle: 'Edit Product Brand',
      readOnly: false,
      redirectAfterSave: '/product-brands',
    }),
  },
  {
    path: '/admin/product-brand/view/:id',
    name: 'product-brand-view',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productbrand'] },
    props: route => ({
      schemaEndpoint: '/api/schema/productbrand/',
      apiEndpoint: '/api/productbrand/',
      objectId: route.params.id,
      formTitle: 'View Product Brand',
      readOnly: true,
      redirectAfterSave: '/product-brands',
    }),
  },
  // {
  //   path: '/product-units',
  //   name: 'product-units',
  //   component: ProductUnitView,
  //   meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productunit'] },
  // },
  // {
  //   path: '/admin/product-unit/form',
  //   name: 'product-unit-form',
  //   component: DynamicForm,
  //   meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_productunit'] },
  //   props: {
  //     schemaEndpoint: '/api/schema/productunit/',
  //     apiEndpoint: '/api/productunit/',
  //     formTitle: 'Create Product Unit',
  //     redirectAfterSave: '/product-units',
  //     readOnly: false,
  //   },
  // },
  // {
  //   path: '/admin/product-unit/view/:id',
  //   name: 'product-unit-view',
  //   component: DynamicForm,
  //   meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_productunit'] },
  //   props: route => ({
  //     schemaEndpoint: '/api/schema/productunit/',
  //     apiEndpoint: '/api/productunit/',
  //     objectId: route.params.id,
  //     formTitle: 'View Product Unit',
  //     redirectAfterSave: '/product-units',
  //     readOnly: true,
  //   }),
  // },
  {
    path: '/admin/product-unit/edit/:id',
    name: 'product-unit-edit',
    component: DynamicForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_productunit'] },
    props: route => ({
      schemaEndpoint: '/api/schema/productunit/',
      apiEndpoint: '/api/productunit/',
      objectId: route.params.id,
      formTitle: 'Edit Product Unit',
      redirectAfterSave: '/product-units',
      readOnly: false,
    }),
  },
  {
    path: '/unit-measures',
    name: 'unit-measures',
    component: UnitOfMeasureView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_unitofmeasure'] },
  },
  {
    path: '/admin/unit-measure/form',
    name: 'unit-measure-form',
    component: DynamicForm,
    props: {
      schemaEndpoint: '/api/schema/unitofmeasure/',
      apiEndpoint: '/api/unitsofmeasure/',
      formTitle: 'Create Unit of Measure',
      redirectAfterSave: '/unit-measures',
      readOnly: false,
    },
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_unitofmeasure'] },
  },
  {
    path: '/admin/unit-measure/view/:id',
    name: 'unit-measure-view',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/unitofmeasure/',
      apiEndpoint: '/api/unitsofmeasure/',
      objectId: route.params.id,
      formTitle: 'View Unit of Measure',
      redirectAfterSave: '/unit-measures',
      readOnly: true,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_unitofmeasure'] },
  },
  {
    path: '/admin/unit-measure/edit/:id',
    name: 'unit-measure-edit',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/unitofmeasure/',
      apiEndpoint: '/api/unitsofmeasure/',
      objectId: route.params.id,
      formTitle: 'Edit Unit of Measure',
      redirectAfterSave: '/unit-measures',
      readOnly: false,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_unitofmeasure'] },
  },
  {
    path: '/unit-categories',
    name: 'unit-categories',
    component: UnitCategoryView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_unitcategory'] },
  },
  {
    path: '/admin/unit-category/form',
    name: 'unit-category-form',
    component: DynamicForm,
    props: {
      schemaEndpoint: '/api/schema/unitcategory/',
      apiEndpoint: '/api/unitcategory/',
      formTitle: 'Create Unit Category',
      redirectAfterSave: '/unit-categories',
      readOnly: false,
    },
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_unitcategory'] },
  },
  {
    path: '/admin/unit-category/view/:id',
    name: 'unit-category-view',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/unitcategory/',
      apiEndpoint: '/api/unitcategory/',
      objectId: route.params.id,
      formTitle: 'View Unit Category',
      redirectAfterSave: '/unit-categories',
      readOnly: true,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_unitcategory'] },
  },
  {
    path: '/admin/unit-category/edit/:id',
    name: 'unit-category-edit',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/unitcategory/',
      apiEndpoint: '/api/unitcategory/',
      objectId: route.params.id,
      formTitle: 'Edit Unit Category',
      redirectAfterSave: '/unit-categories',
      readOnly: false,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_unitcategory'] },
  },
  {
    path: '/price-types',
    name: 'price-types',
    component: PriceTypeView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_pricetype'] },
  },
  {
    path: '/admin/price-type/form',
    name: 'price-type-form',
    component: DynamicForm,
    props: {
      schemaEndpoint: '/api/schema/pricetype/',
      apiEndpoint: '/api/pricetypes/',
      formTitle: 'Create Price Type',
      redirectAfterSave: '/price-types',
      readOnly: false,
    },
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_pricetype'] },
  },
  {
    path: '/admin/price-type/view/:id',
    name: 'price-type-view',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/pricetype/',
      apiEndpoint: '/api/pricetypes/',
      objectId: route.params.id,
      formTitle: 'View Price Type',
      redirectAfterSave: '/price-types',
      readOnly: true,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_pricetype'] },
  },
  {
    path: '/admin/price-type/edit/:id',
    name: 'price-type-edit',
    component: DynamicForm,
    props: route => ({
      schemaEndpoint: '/api/schema/pricetype/',
      apiEndpoint: '/api/pricetypes/',
      objectId: route.params.id,
      formTitle: 'Edit Price Type',
      redirectAfterSave: '/price-types',
      readOnly: false,
    }),
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_pricetype'] },
  },
  {
    path: '/products',
    name: 'product-list',
    component: ProductListView,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_product'] },
    props: true,
  },
  {
    path: '/products/form',
    name: 'product-form',
    component: ProductForm,
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.add_product'] },
    props: true,
  },
  {
    path: '/products/view/:id',
    name: 'product-view',
    component: ProductForm,
    props: route => ({ objectId: route.params.id }), // así lo pasas como prop
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.view_product'] },
  },
  {
    path: '/products/edit/:id',
    name: 'product-edit',
    component: ProductForm,
    props: route => ({ objectId: route.params.id }), // también aquí 
    meta: { requiresAuth: true, requiredPermissions: ['appinventory.change_product'] },
  },

  // ───────────────────────────────────────────────────────────
  // TRANSACTIONS MODULE                                        
  // ───────────────────────────────────────────────────────────

  {
    path: '/document-types',
    name: 'document-types',
    component: DocTypeListView,
    meta: { requiresAuth: true, requiredPermissions: ['apptransactions.view_documenttype'] },
  },
  {
    path: '/document-types/form',
    name: 'document-types-form',
    component: DocTypeFormComponent,
    meta: { requiresAuth: true, requiredPermissions: ['apptransactions.add_documenttype'] },
  },
];


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