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

// Ensure charts use JetBrains Mono to match the app CSS
const FONT_FAMILY = `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace`;
Chart.defaults.font.family = FONT_FAMILY;

// Use CSS variables to style chart axes so they contrast with dark backgrounds
const cssVars = getComputedStyle(document.documentElement);
const TEXT_COLOR = (cssVars.getPropertyValue('--text') || '#e5e7eb').trim();
const MUTED_COLOR = (cssVars.getPropertyValue('--muted') || '#9ca3af').trim();

function hexToRGBA(hex, alpha = 1) {
  let c = hex.replace('#', '').trim();
  if (c.length === 3) c = c.split('').map(ch => ch + ch).join('');
  const num = parseInt(c, 16);
  const r = (num >> 16) & 255;
  const g = (num >> 8) & 255;
  const b = num & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

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
        pointBackgroundColor: "#9e0000ff",
        pointRadius: 5.5
      }
    ]
  },
  options: {
    responsive: true,
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart'
    },
    plugins: {
      legend: {
        labels: { color: TEXT_COLOR }
      }
    },
    scales: {
      x: {
        type: "time",
        time: { parser: "yyyy-MM-dd HH:mm:ss", tooltipFormat: "PPpp" },
        title: { display: true, text: "Time (MST)", color: TEXT_COLOR },
        ticks: { color: TEXT_COLOR },
        grid: {
          color: hexToRGBA(MUTED_COLOR, 0.25),
          borderColor: hexToRGBA(MUTED_COLOR, 0.5)
        }
      },
      y: {
        title: { display: true, text: label, color: TEXT_COLOR },
        ticks: { color: TEXT_COLOR },
        grid: {
          color: hexToRGBA(MUTED_COLOR, 0.25),
          borderColor: hexToRGBA(MUTED_COLOR, 0.5)
        }
      }
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // initialize charts with an anomaly dataset built in
  const tempChart = new Chart(document.getElementById("tempChart"), chartCfg("Temperature (°F)", '#701f5fff'));
  const humChart = new Chart(document.getElementById("humChart"), chartCfg("Humidity (%)", "#2563eb"));
  const presChart = new Chart(document.getElementById("presChart"), chartCfg("Pressure (hPa)", "#189044ff"));
  const anomalyChart = new Chart(document.getElementById("anomalyChart"), chartCfg("Anomaly Score", "#fba364ff"));

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
