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
  data: {
    labels: [],
    datasets: [
      {
        label,
        borderWidth: 2,
        fill: false,
        borderColor: color,
        data: [],
        // point styling for smooth updates
        pointBackgroundColor: color,
        pointBorderColor: color,
        pointRadius: 3,
        pointHoverRadius: 5
      },
      { // anomaly layer pre-configured for smooth updates
        label: "Anomalies",
        type: "scatter",
        data: [],
        showLine: false,
        pointBackgroundColor: "red",
        pointRadius: 6
      }
    ]
  },
  options: {
    responsive: true,
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart'
    },
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
  // initialize charts with an anomaly dataset built in
  const tempChart = new Chart(document.getElementById("tempChart"), chartCfg("Temperature (°F)", "purple"));
  const humChart = new Chart(document.getElementById("humChart"), chartCfg("Humidity (%)", "blue"));
  const presChart = new Chart(document.getElementById("presChart"), chartCfg("Pressure (hPa)", "green"));
  const anomalyChart = new Chart(document.getElementById("anomalyChart"), chartCfg("Anomaly Score", "orange"));

  async function fetchData() {
    try {
      const res = await fetch("/data");
      const rows = await res.json();
      if (!rows.length) return;

      // extract arrays
      const ts = rows.map(r => r.timestamp);
      const temps = rows.map(r => r.temperature);
      const hums = rows.map(r => r.humidity);
      const press = rows.map(r => r.pressure);
      const anomaly_score = rows.map(r => r.raw_scores);

      // extract anomalies
      const anomTemps = rows.filter(r => r.is_anomaly)
        .map(r => ({ x: r.timestamp, y: r.temperature }));
      const anomHums = rows.filter(r => r.is_anomaly)
        .map(r => ({ x: r.timestamp, y: r.humidity }));
      const anomPress = rows.filter(r => r.is_anomaly)
        .map(r => ({ x: r.timestamp, y: r.pressure }));
      const anomScores = rows.filter(r => r.is_anomaly)
        .map(r => ({ x: r.timestamp, y: r.raw_scores }));

      // update temp chart in-place
      tempChart.data.labels = ts;
      tempChart.data.datasets[0].data = temps;
      tempChart.data.datasets[1].data = anomTemps;
      tempChart.update();

      // update humidity chart
      humChart.data.labels = ts;
      humChart.data.datasets[0].data = hums;
      humChart.data.datasets[1].data = anomHums;
      humChart.update();

      // update pressure chart
      presChart.data.labels = ts;
      presChart.data.datasets[0].data = press;
      presChart.data.datasets[1].data = anomPress;
      presChart.update();

      // update anomaly score chart
      anomalyChart.data.labels = ts;
      anomalyChart.data.datasets[0].data = anomaly_score;
      anomalyChart.data.datasets[1].data = anomScores;
      anomalyChart.update();

    } catch (err) {
      console.error("Error fetching /data:", err);
    }
  }

  fetchData();               // initial load
  setInterval(fetchData, 1000); // refresh each 1 seconds
});
