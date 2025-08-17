<template>
  <div>
    <div class="row mb-3">
      <div class="col-md-4">
        <label for="category">Filter by Category:</label>
        <select class="form-select" v-model="selectedCategory" @change="handleCategoryChange">
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.name">
            {{ cat.name }}
          </option>
        </select>
      </div>
      <div class="col-md-4 d-flex align-items-end justify-content-center">
        <div class="text-muted mb-4"></div>
        <i>Showing data from the last 16 weeks</i>
      </div>
      <div class="col-md-3 d-flex align-items-end justify-content-end me-2"
        v-if="hasPermission('appschedule.view_event')">

        <!-- Dropdown Excel Export -->
        <div class="btn-group">
          <button
            class="btn btn-sm btn-outline-success btn-lg dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false">
            <img src="@/assets/img/microsoft-excel-icon.svg" alt="Excel" width="20" class="me-1" />
            Download Excel Report
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click.prevent="downloadSupervisorExcel(16)">Last 4 Months</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="downloadSupervisorExcel(24)">Last 6 Months</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="downloadSupervisorExcel(32)">Last 8 Months</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="downloadSupervisorExcel(52)">Last 12 Months</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="chart-container">
      <!-- Muestra el canvas solo cuando el DOM está listo -->
      <canvas ref="barChart" v-show="isChartVisible"></canvas>
    </div>
  </div>
</template>

<script>
  import { defineComponent, ref, onMounted, nextTick } from 'vue';
  import { Chart, registerables } from 'chart.js';
  import axios from 'axios';

  Chart.register(...registerables);

  const colorPalette = [
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 99, 132, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 159, 64, 0.7)',
    'rgba(201, 203, 207, 0.7)',
    'rgba(0, 128, 0, 0.7)',
    'rgba(255, 20, 147, 0.7)',
    'rgba(0, 191, 255, 0.7)'
  ];

  const colorMap = {};

  const colorForLabel = label => {
    if (!colorMap[label]) {
      const nextColor = colorPalette[Object.keys(colorMap).length % colorPalette.length];
      colorMap[label] = nextColor;
    }
    return colorMap[label];
  };

  export default defineComponent({
    name: 'WeeklySupervisorChart',
    setup() {
      const barChart = ref(null);
      const chartInstance = ref(null);
      const selectedCategory = ref('');
      const categories = ref([]);
      const isChartVisible = ref(false);
      const selectedWeeks = ref(16);

      const fetchCategories = async () => {
        try {
          const res = await axios.get('/api/categories/');
          categories.value = res.data;
        } catch (err) {
          console.error('Error loading categories:', err);
        }
      };

      const fetchChartData = async () => {
        isChartVisible.value = false;

        try {
          const res = await axios.get('/api/supervisor-stats/', {
            params: {
              weeks: selectedWeeks.value,
              category: selectedCategory.value || undefined,
            },
          });

          await nextTick();
          updateChart(res.data);
        } catch (err) {
          console.error('Error loading chart data:', err);
        }
      };

      const updateChart = data => {
        if (!barChart.value || !barChart.value.getContext) {
          console.warn('Canvas not ready');
          return;
        }

        if (chartInstance.value) {
          chartInstance.value.destroy();
          chartInstance.value = null;
        }

        chartInstance.value = new Chart(barChart.value.getContext('2d'), {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: data.datasets.map(ds => ({
              label: ds.label,
              data: ds.data,
              backgroundColor: colorForLabel(ds.label),
            })),
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'top' },
              tooltip: { mode: 'index', intersect: false },
            },
            scales: {
              x: {
                title: { display: true, text: 'Weeks' },
              },
              y: {
                beginAtZero: true,
                title: { display: true, text: 'Jobs' },
              },
            },
          },
        });

        isChartVisible.value = true;
      };

      const handleCategoryChange = () => {
        fetchChartData();
      };

      const downloadSupervisorExcel = async (weeks) => {
        const params = new URLSearchParams({
          weeks,
          category: selectedCategory.value || '',
        });

        try {
          const response = await axios.get(`/api/supervisor-stats-excel/?${params.toString()}`, { responseType: 'blob' });
          const blob = new Blob([response.data], { type: response.headers['content-type'] });
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);

          const today = new Date();
          const formattedToday = today.toISOString().split('T')[0];
          link.download = `supervisor-stats_${formattedToday}_last${weeks}weeks.xlsx`;
          link.click();
          Swal.fire("Excel Ready!", "The file has been downloaded successfully.", "success");
        } catch (err) {
          console.error("Excel Download Error:", err);
        }
      };

      onMounted(() => {
        fetchCategories();
        fetchChartData();
      });

      return {
        barChart,
        selectedCategory,
        categories,
        isChartVisible,
        handleCategoryChange,
        downloadSupervisorExcel
      };
    },
  });
</script>

<style scoped>
  .chart-container {
    position: relative;
    width: 100%;
    height: 380px;
    overflow: hidden;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>
