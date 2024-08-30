let id_a = "WI100";
let url_a = "https://raw.githubusercontent.com/labwons/pages/main/src/json/indices/" + id_a + ".json";
var data_a = null;

function chart() {
  var asset = {
    x: data_a.date,
    y: data_a.value,
    type: "scatter",
    mode: "lines",
    name: "test", // #TODO <select>의 html 값으로 채울 것
    yaxis: 'y'
  };
  // var macro =
  var layout = {
    xaxis: {
      title: '날짜',
    },
    yaxis: {
      title: 'INDEX',
    }
  };
  Plotly.newPlot('data', [asset], layout);
}


$(document).ready(async function(){
    try {
      const response = await fetch(url_a);
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      data_a = await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
    }
    chart();
  })