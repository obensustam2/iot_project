<template>
  <div class="table-container">
    <h2>🌡️ Temperature Logs by Device</h2>
    <p v-if="error" class="error">Error: {{ error }}</p>

    <div v-for="(entries, device) in deviceTables" :key="device" class="device-table">
      <h3>📟 {{ device }}</h3>
      <table>
        <thead>
          <tr>
            <th class="temp-col">Temperature (°C)</th>
            <th class="time-col">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, index) in entries" :key="index">
            <td class="temp-col">{{ entry.temperature }}</td>
            <td class="time-col">{{ new Date(entry.time).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script>
export default {
  name: "TemperatureTable",
  data() {
    return {
      deviceTables: {},
      error: null
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://localhost:8000/api/temperature");
        const result = await response.json();

        if (result.error) {
          this.error = result.error;
        } else {
          this.deviceTables = result;
        }
      } catch (err) {
        this.error = "Could not connect to backend";
      }
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 10000);
  }
};
</script>

<style scoped>
.table-container {
  max-width: 600px;
  margin: 0 auto;
  font-family: sans-serif;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  text-align: center;
}
th {
  background: #eee;
}
.device-col {
  background-color: #f9f4ff;
  color: #5026a7;
}
.temp-col {
  background-color: #fff8e7;
  color: #b95e00;
}
.time-col {
  background-color: #e6f7ff;
  color: #0078b3;
}
.error {
  color: red;
  font-weight: bold;
}
</style>
