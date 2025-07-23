// Register needed components once (Chart.js v4)
Chart.register(
  Chart.TimeScale,
  Chart.LineController,
  Chart.LineElement,
  Chart.PointElement,
  Chart.Legend,
  Chart.Title,
  Chart.LinearScale,
  Chart.CategoryScale
);

const chartCfg = (label, color) => ({
  type: "line",
  data: { labels: [], datasets: [{ label, borderWidth: 2, fill: false, borderColor: color, data: [] }] },
  options: {
    responsive: true,
    scales: {
      x: {
        type: "time",
        time: { parser: "yyyy-MM-dd HH:mm:ss", tooltipFormat: "PPpp" },
        title: { display: true, text: "Time (MST)" }
      },
      y: { title: { display: true, text: label } }
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // create three separate charts
  const tempChart = new Chart(document.getElementById("tempChart"), chartCfg("Temperature (°C)", "red"));
  const humChart  = new Chart(document.getElementById("humChart"),  chartCfg("Humidity (%)",    "blue"));
  const presChart = new Chart(document.getElementById("presChart"), chartCfg("Pressure (hPa)",  "green"));

  async function fetchData() {
    try {
      const res  = await fetch("/data");
      const rows = await res.json();
      if (!rows.length) return;

      // timestamps (labels)
      const ts = rows.map(r => r.timestamp);

      // Update each chart independently
      tempChart.data.labels       = ts;
      tempChart.data.datasets[0].data = rows.map(r => r.temperature);

      humChart.data.labels        = ts;
      humChart.data.datasets[0].data  = rows.map(r => r.humidity);

      presChart.data.labels       = ts;
      presChart.data.datasets[0].data = rows.map(r => r.pressure);

      tempChart.update();
      humChart.update();
      presChart.update();
    } catch (err) {
      console.error("Error fetching /data:", err);
    }
  }

  fetchData();               // initial load
  setInterval(fetchData, 1000); // refresh each second
});
