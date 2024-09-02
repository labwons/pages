const INDEX_KEY = {'WI100': '에너지', 'WI110': '화학', 'WI200': '비철금속', 'WI210': '철강', 'WI220': '건설', 'WI230': '기계', 'WI240': '조선', 'WI250': '상사,자본재',
  'WI260': '운송', 'WI300': '자동차', 'WI310': '화장품,의류', 'WI320': '호텔,레저', 'WI330': '미디어,교육', 'WI340': '소매(유통)', 'WI400': '필수소비재',
  'WI410': '건강관리', 'WI500': '은행', 'WI510': '증권', 'WI520': '보험', 'WI600': '소프트웨어', 'WI610': 'IT하드웨어', 'WI620': '반도체', 'WI630': 'IT가전',
  'WI640': '디스플레이', 'WI700': '통신서비스', 'WI800': '유틸리티'}
const INDEX_URL = "https://raw.githubusercontent.com/labwons/pages/main/src/json/macro/index.json";
var index_data = null;
var index = null;


function chart() {
  var asset = {
    x: index_data.date,
    y: index_data[index],
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
      const response = await fetch(INDEX_URL);
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      index_data = await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
    }
    // chart();
})

$(document).ready(function(){
  for(let key in INDEX_KEY){
    $('.industry').append('<option value="' + key + '">' + INDEX_KEY[key] + '</option>');
  }
  
  $('.industry').on('change', function(){
    $('#industry-macro').html('');
    index = $(this).val();
    chart();
  })
})