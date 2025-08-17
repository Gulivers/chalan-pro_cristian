<template>
  <div>
    <h5 class="mb-3">Price and Unit Settings</h5>
    <div class="table-responsive">
      <table class="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Price Type</th>
            <th>Unit</th>
            <th>Purchase</th>
            <th>Sale</th>
            <th>Price</th>
            <th>Default</th>
            <th>Valid From</th>
            <th>Valid Until</th>
            <th>Active</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in priceUnitRows" :key="index">
            <!-- Price Type -->
            <td>
              <div class="d-flex align-items-center w-100" style="min-width: 240px">
                <v-select
                  :options="priceTypes"
                  v-model="row.price_type"
                  :reduce="type => type.id"
                  label="name"
                  placeholder="Select Price Type"
                  class="flex-grow-1 min-w-0"
                  @open="$emit('refresh-priceTypes')" />
                <button class="btn btn-outline-secondary btn-sm ms-1" type="button" @click="openModal('priceType')">
                  <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15" />
                </button>
                <button
                  v-if="row.price_type"
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="editModal('priceType', row.price_type)">
                  <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15" />
                </button>
              </div>
            </td>

            <!-- Unit -->
            <td>
              <div class="d-flex align-items-center w-100" style="min-width: 240px">
                <v-select
                  :options="units"
                  v-model="row.unit"
                  :reduce="unit => unit.id"
                  label="name"
                  placeholder="Select Unit"
                  class="flex-grow-1 min-w-0"
                  @open="$emit('refresh-units')" />
                <button class="btn btn-outline-secondary btn-sm ms-1" type="button" @click="openModal('unit')">
                  <img src="@assets/img/icon-addlink.svg" alt="Add" width="15" height="15" />
                </button>
                <button
                  v-if="row.unit"
                  class="btn btn-outline-secondary btn-sm ms-1"
                  type="button"
                  @click="editModal('unit', row.unit)">
                  <img src="@assets/img/icon-changelink.svg" alt="Edit" width="15" height="15" />
                </button>
              </div>
            </td>

            <!-- Purchase -->
            <td class="text-center">
              <input type="checkbox" v-model="row.is_purchase" class="form-check-input" />
            </td>

            <!-- Sale -->
            <td class="text-center">
              <input type="checkbox" v-model="row.is_sale" class="form-check-input" />
            </td>

            <!-- Price -->
            <td style="min-width: 105px">
              <input
                type="number"
                step="0.01"
                class="form-control form-control-sm w-100"
                v-model="row.price"
                placeholder="Enter price" />
            </td>

            <!-- Default -->
            <td class="text-center">
              <input
                type="radio"
                name="defaultRow"
                class="form-check-input"
                :checked="row.is_default"
                @change="setDefault(index)" />
            </td>

            <!-- Dates -->
            <td>
              <input type="date" v-model="row.valid_from" class="form-control" />
            </td>
            <td>
              <input type="date" v-model="row.valid_until" class="form-control" />
            </td>

            <!-- Active -->
            <td class="text-center">
              <input type="checkbox" v-model="row.is_active" class="form-check-input" />
            </td>

            <!-- Delete -->
            <td class="text-center">
              <button class="btn btn-sm btn-outline-danger" @click="removeRow(index)">❌</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <button type="button" class="btn btn-outline-primary btn-sm mt-2" @click="addRow">+ Add Row</button>
  </div>
</template>

<script>
  import VSelect from 'vue-select';
  import 'vue-select/dist/vue-select.css';

  export default {
    components: {
      VSelect,
    },
    name: 'ProductPriceUnitTable',
    props: {
      modelValue: Array,
      priceTypes: Array,
      units: Array,
    },
    emits: ['update:modelValue'],
    computed: {
      priceUnitRows: {
        get() {
          return this.modelValue;
        },
        set(newVal) {
          this.$emit('update:modelValue', newVal);
        },
      },
    },
    methods: {
      addRow() {
        this.priceUnitRows.push({
          price_type: '',
          unit: '',
          is_purchase: false,
          is_sale: false,
          price: '',
          is_default: false,
          valid_from: '',
          valid_until: '',
          is_active: true,
        });
      },
      removeRow(index) {
        this.priceUnitRows.splice(index, 1);
      },
      setDefault(index) {
        this.priceUnitRows.forEach((row, i) => {
          row.is_default = i === index;
        });
      },
      openModal(type) {
        this.$emit('open-modal', type);
      },
      editModal(type, id) {
        if (id) {
          this.$emit('edit-modal', { type, id });
        }
      },
    },
  };
</script>