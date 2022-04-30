const SELECTOR_ID = 'ticker_selector'

document.addEventListener('DOMContentLoaded', () => {
  const chart = Highcharts.chart('container', {
    title: {text: 'Important Financial Data'},
    credits: {enabled: false},
    yAxis: {title: {text: 'Price'}},
    xAxis: {title: {text: 'Time'}, type: 'datetime'},
    legend: {enabled: false,},
    plotOptions: {line: {marker: {enabled: false}}},
    series: [{name: 'prices', type: 'spline', marker: {enabled: false}}]
  });

  document.getElementById(SELECTOR_ID).addEventListener("change", function() {
    fillChartData(chart, this.value)
  });
  createConnection(chart);
  fillSelectorOptions();
})

function createConnection(chart) {
    let socket = io.connect(`http://${document.domain}:${location.port}`);
    socket.on('prices', msg => {
      const point = msg[get_selected_ticker()];
      point[0] = point[0] * 1000 - get_time_shift();
      chart.series[0].addPoint(point);
    });
}

function fillSelectorOptions() {
  const select = document.getElementById(SELECTOR_ID);
  fetch(`http://${document.domain}:${location.port}/ticker_names`)
      .then(response => response.json())
      .then(data => {
        for (let ticker_name of data) {
          const opt = document.createElement('option');
          opt.value = ticker_name;
          const splitted_name = ticker_name.split('_')
          opt.innerHTML = `${splitted_name[0].toUpperCase()} ${splitted_name[1]}`;
          select.appendChild(opt);
        }
        select.dispatchEvent(new Event('change'))
      });
}

function fillChartData(chart, ticker_name) {
    fetch(`http://${document.domain}:${location.port}/ticker_data?ticker_name=${ticker_name}`)
      .then(response => response.json())
      .then(data => {
        data = data.map(el => [el[0] * 1000 - get_time_shift(), el[1]]);
        chart.series[0].setData(data)
      })
}

function get_time_shift() {
  return new Date().getTimezoneOffset() * 60 * 1000;
}

function get_selected_ticker() {
  return document.getElementById(SELECTOR_ID).value
}
