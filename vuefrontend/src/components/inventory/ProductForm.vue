<template>
  <div class="container mt-4">
    <div class="card shadow" style="height: auto">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">{{ objectId ? 'Edit Product' : 'Create Product' }}</h5>
        <button class="btn btn-secondary btn-sm" @click="cancelForm">Back</button>
      </div>

      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <!-- Campos del producto -->
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Name</label>
              <input v-model="product.name" type="text" class="form-control" required />
            </div>

            <div class="col-md-6 mb-3">
              <label>SKU</label>
              <input v-model="product.sku" type="text" class="form-control" required />
            </div>

            <!-- Category -->
            <div class="col-md-6 mb-3">
              <label>Category</label>
              <div class="d-flex align-items-center">
                <v-select
                  :options="categories"
                  v-model="product.category"
                  :reduce="cat => cat.id"
                  label="name"
                  placeholder="Select Category"
                  class="flex-grow-1"
                  :disabled="isReadOnly"
                  @open="loadCategories" />
                <button
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openCategoryModal('add')"
                  :disabled="isReadOnly || !hasPermission('appinventory.add_productcategory')">
                  <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15" />
                </button>
                <button
                  v-if="product.category"
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openCategoryModal('edit', product.category)"
                  :disabled="isReadOnly || !hasPermission('appinventory.change_productcategory')">
                  <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15" />
                </button>
              </div>
            </div>

            <!-- Brand -->
            <div class="col-md-6 mb-3">
              <label>Brand</label>
              <div class="d-flex align-items-center">
                <v-select
                  :options="brands"
                  v-model="product.brand"
                  :reduce="brand => brand.id"
                  label="name"
                  placeholder="Select Brand"
                  class="flex-grow-1"
                  :disabled="isReadOnly"
                  @open="loadBrands" />
                <button
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openBrandModal('add')"
                  :disabled="isReadOnly || !hasPermission('appinventory.add_productbrand')">
                  <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15" />
                </button>
                <button
                  v-if="product.brand"
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openBrandModal('edit', product.brand)"
                  :disabled="isReadOnly || !hasPermission('appinventory.change_productbrand')">
                  <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15" />
                </button>
              </div>
            </div>

            <!-- Default Unit -->
            <div class="col-md-6 mb-3">
              <label>Default Unit</label>
              <div class="d-flex align-items-center">
                <v-select
                  :options="units"
                  v-model="product.unit_default"
                  :reduce="unit => unit.id"
                  label="name"
                  placeholder="Select Unit"
                  class="flex-grow-1"
                  :disabled="isReadOnly"
                  @open="loadUnits" />
                <button
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openUnitModal('add')"
                  :disabled="isReadOnly || !hasPermission('appinventory.add_unitofmeasure')">
                  <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15" />
                </button>
                <button
                  v-if="product.unit_default"
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="openUnitModal('edit', product.unit_default)"
                  :disabled="isReadOnly || !hasPermission('appinventory.change_unitofmeasure')">
                  <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15" />
                </button>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label>Reorder Level</label>
              <input v-model="product.reorder_level" type="number" step="0.01" class="form-control" />
            </div>

            <div class="col-md-6 mb-3 d-flex align-items-center gap-2">
              <input v-model="product.is_active" type="checkbox" class="form-check-input" id="isActive" />
              <label for="isActive" class="form-check-label">Active</label>
            </div>
          </div>

          <!-- Tabla combinada ProductUnit + ProductPrice -->
          <ProductPriceUnitTable
            v-model="productPriceUnits"
            :priceTypes="priceTypes"
            :units="units"
            @open-modal="handleOpenModal"
            @edit-modal="handleEditModal"
            @refresh-priceTypes="loadPriceTypes"
            @refresh-units="loadUnits" />

          <div class="mt-4">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" class="btn btn-secondary ms-2" @click="cancelForm">Cancel</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Modales para agregar/editar Category, Brand y Unit -->
    <CategoryModal ref="categoryModal" :objectId="modalObjectId" @refreshCategories="loadCategories" />
    <BrandModal ref="brandModal" :objectId="modalObjectId" @refreshBrands="loadBrands" />
    <UnitModal ref="unitModal" :objectId="modalObjectId" @refreshUnits="loadUnits" />
    <PriceTypeModal ref="priceTypeModal" :objectId="modalObjectId" @refresh="loadPriceTypes" />
  </div>
</template>

<script>
  import axios from 'axios';
  import VSelect from 'vue-select';
  import 'vue-select/dist/vue-select.css';
  import Swal from 'sweetalert2';
  import ProductPriceUnitTable from '@/components/inventory/ProductPriceUnitTable.vue';
  import CategoryModal from '@/components/inventory/CategoryModal.vue';
  import BrandModal from '@/components/inventory/BrandModal.vue';
  import UnitModal from '@/components/inventory/UnitModal.vue';
  import PriceTypeModal from '@/components/inventory/PriceTypeModal.vue';

  export default {
    name: 'ProductForm',
    components: {
      ProductPriceUnitTable,
      VSelect,
      CategoryModal,
      BrandModal,
      UnitModal,
      PriceTypeModal,
    },
    props: {
      objectId: {
        type: [Number, String],
        default: null,
      },
    },
    data() {
      return {
        product: {
          name: '',
          sku: '',
          category: '',
          brand: '',
          unit_default: '',
          reorder_level: 0,
          is_active: true,
        },
        productPriceUnits: [],
        categories: [],
        brands: [],
        units: [],
        priceTypes: [],
        modalObjectId: null,
        isReadOnly: false,
      };
    },
    created() {
      this.loadInitialData();
      if (this.objectId) this.loadProduct();
    },
    methods: {
      async loadInitialData() {
        try {
          const [catRes, brandRes, unitRes, priceTypeRes] = await Promise.all([
            axios.get('/api/productcategory/'),
            axios.get('/api/productbrand/'),
            axios.get('/api/unitsofmeasure/'),
            axios.get('/api/pricetypes/'),
          ]);

          this.categories = catRes.data;
          this.brands = brandRes.data;
          this.units = unitRes.data;
          this.priceTypes = priceTypeRes.data;
        } catch (err) {
          console.error('Failed to load select options', err);
        }
      },
      async loadProduct() {
        try {
          const res = await axios.get(`/api/products/${this.objectId}/`);
          this.product = res.data;
          this.productPriceUnits = res.data.price_units || [];
          if (res.data.prices?.length > 0) {
            res.data.prices.forEach(price => {
              const match = this.productPriceUnits.find(pu => pu.unit === price.unit);
              if (match) {
                Object.assign(match, price);
              } else {
                this.productPriceUnits.push(price);
              }
            });
          }
        } catch (err) {
          console.error('Error loading product:', err);
        }
      },
      async handleSubmit() {
        try {
          // 1. Limpieza y validación de los datos de precios
          const cleanedPriceUnits = [];
          const cleanedPrices = [];
          let hasError = false;
          let errorMessages = [];

          this.productPriceUnits.forEach((pu, idx) => {
            // Conversión segura a ID
            const unitId = typeof pu.unit === 'object' ? pu.unit?.id : pu.unit;
            const priceTypeId = typeof pu.price_type === 'object' ? pu.price_type?.id : pu.price_type;

            // Validación de campos obligatorios
            if (!unitId || !priceTypeId) {
              hasError = true;
              errorMessages.push(`Fila ${idx + 1}: Falta unidad o tipo de precio.`);
              return;
            }

            // Validación de price (debe ser número válido)
            let priceValue = pu.price;
            if (priceValue === '' || priceValue === null || priceValue === undefined) priceValue = null;
            else priceValue = Number(priceValue);

            // Si hay precio, debe ser número válido
            if (priceValue !== null && (isNaN(priceValue) || priceValue < 0)) {
              hasError = true;
              errorMessages.push(`Fila ${idx + 1}: El precio es inválido.`);
              return;
            }

            // Validación de fechas (puedes hacer más robusto si lo deseas)
            const validFrom = pu.valid_from || null;
            const validUntil = pu.valid_until || null;

            // Armar objeto de unidad/precio
            cleanedPriceUnits.push({
              unit: unitId,
              is_purchase: !!pu.is_purchase,
              is_sale: !!pu.is_sale,
            });

            // Solo agregar precios completos
            if (priceTypeId && unitId && priceValue !== null) {
              cleanedPrices.push({
                price_type: priceTypeId,
                unit: unitId,
                price: priceValue,
                is_default: !!pu.is_default,
                valid_from: validFrom,
                valid_until: validUntil,
                is_active: pu.is_active !== false, // default true
              });
            }
          });

          if (hasError) {
            // Mostrar errores y abortar
            Swal.fire({
              icon: 'error',
              title: 'Errores en los precios',
              html: `<ul style="text-align:left">${errorMessages.map(e => `<li>${e}</li>`).join('')}</ul>`
            });
            return;
          }

          // 2. Armar el payload limpio
          const payload = {
            name: this.product.name,
            sku: this.product.sku,
            category: typeof this.product.category === 'object' ? this.product.category?.id : this.product.category,
            brand: typeof this.product.brand === 'object' ? this.product.brand?.id : this.product.brand,
            unit_default: typeof this.product.unit_default === 'object' ? this.product.unit_default?.id : this.product.unit_default,
            reorder_level: this.product.reorder_level,
            is_active: !!this.product.is_active,
            price_units: cleanedPriceUnits,
            prices: cleanedPrices,
          };

          // 3. Logs de depuración
          console.log('🟢 ProductPriceUnits originales:', this.productPriceUnits);
          console.log('🟢 cleanedPriceUnits:', cleanedPriceUnits);
          console.log('🟢 cleanedPrices:', cleanedPrices);
          console.log('🟢 Payload final:', payload);

          // 4. Envío
          const url = this.objectId ? `/api/products/${this.objectId}/` : '/api/products/';
          const method = this.objectId ? 'put' : 'post';

          await axios({ method, url, data: payload });

          Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: 'Producto guardado correctamente',
          });
          this.$router.push('/products');
        } catch (err) {
          console.error('Failed to save product:', err);
          if (err.response?.data) {
            const errors = err.response.data;
            const errorMsg = typeof errors === 'object' ? JSON.stringify(errors, null, 2) : errors;
            Swal.fire({
              icon: 'error',
              title: 'Validation Error',
              html: `<pre style="text-align:left">${errorMsg}</pre>`
            });
          } else {
            Swal.fire('Error', 'Failed to save product', 'error');
          }
        }
      },
      cancelForm() {
        this.$router.back();
      },
      openCategoryModal(mode, id = null) {
        this.modalObjectId = mode === 'edit' ? id : null;
        this.$refs.categoryModal.openModal();
      },
      openBrandModal(mode, id = null) {
        this.modalObjectId = mode === 'edit' ? id : null;
        this.$refs.brandModal.openModal();
      },
      openUnitModal(mode, id = null) {
        this.modalObjectId = mode === 'edit' ? id : null;
        this.$refs.unitModal.openModal();
      },
      loadCategories() {
        axios.get('/api/productcategory/').then(res => {
          this.categories = res.data;
        });
      },
      loadBrands() {
        axios.get('/api/productbrand/').then(res => {
          this.brands = res.data;
        });
      },
      loadUnits() {
        axios.get('/api/unitsofmeasure/').then(res => {
          this.units = res.data;
        });
      },
      loadPriceTypes() {
        axios.get('/api/pricetypes/').then(res => {
          this.priceTypes = res.data;
        });
      },
      handleOpenModal(type) {
        this.modalObjectId = null;
        if (type === 'priceType') this.$refs.priceTypeModal.openModal();
        if (type === 'unit') this.$refs.unitModal.openModal();
      },
      handleEditModal({ type, id }) {
        this.modalObjectId = id;
        if (type === 'priceType') this.$refs.priceTypeModal.openModal();
        if (type === 'unit') this.$refs.unitModal.openModal();
      },
    },
  };
</script>

