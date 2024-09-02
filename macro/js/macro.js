const INDEX_KEY = {'WI100': '에너지', 'WI110': '화학', 'WI200': '비철금속', 'WI210': '철강', 'WI220': '건설', 'WI230': '기계', 'WI240': '조선', 'WI250': '상사,자본재',
  'WI260': '운송', 'WI300': '자동차', 'WI310': '화장품,의류', 'WI320': '호텔,레저', 'WI330': '미디어,교육', 'WI340': '소매(유통)', 'WI400': '필수소비재',
  'WI410': '건강관리', 'WI500': '은행', 'WI510': '증권', 'WI520': '보험', 'WI600': '소프트웨어', 'WI610': 'IT하드웨어', 'WI620': '반도체', 'WI630': 'IT가전',
  'WI640': '디스플레이', 'WI700': '통신서비스', 'WI800': '유틸리티'}
const INDEX_URL = "https://raw.githubusercontent.com/labwons/pages/main/src/json/macro/index.json";
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');

var index_data = null;
var macro_data = null;
var index = null;
var macro = null;
var layout = {
  margin:{
    l:80, 
    r:80, 
    t:10, 
    b:30
  }, 
  hovermode: 'x unified',
  legend: {
    bgcolor:'white',
    borderwidth:0,
    itemclick:'toggle',
    itemdoubleclick:'toggleothers',
    orientation:'h',
    valign:'middle',
    xanchor:'right',
    x:1.0,
    yanchor:'top',
    y:1.0
  },
  xaxis:{
    // title: '날짜',
    tickformat: "%Y/%m/%d",
    range:['2021-01-01', '2024-08-29'],
    showticklabels: true,
    showline: true,
    rangeselector: {
      buttons: [
        { count: 1, label: '1Y', step: 'year', stepmode: 'backward' },
        { count: 3, label: '3Y', step: 'year', stepmode: 'backward' },
        { count: 5, label: '5Y', step: 'year', stepmode: 'backward' },
        { step: 'all', label: 'All' }
      ]
    },
    
  },
  yaxis:{
    // title: index,
    // range: [Math.min(...index_data[index]), Math.min(...index_data[index])],
    showline: false,
    zeroline: false,
    showticklabels: false
  },
  yaxis2: {
    // title:macro,
    overlaying:'y',
    side:'right',
    zeroline:false,
    showline:false,
    showgrid:false,
    showticklabels: false
  },
  dragmode: 'pan'
  // dragmode: false
}

function traceAsset() {
  if (index == null){
    return {};
  }
  // layout.yaxis.title = INDEX_KEY[index];
  return {
    x: index_data.date,
    y: index_data[index],
    type: "scatter",
    mode: "lines",
    name: INDEX_KEY[index],
    showlegend:true,
    line: {
      color: 'black'
    },
    yaxis: 'y'
  };
}

function traceMacro() {
  if (macro == null) {
    return {};
  }
  if (macro in INDEX_KEY) {
    var src = index_data;
    var nm = INDEX_KEY[macro];
  } else {
    var src = macro_data;
    var nm = MACRO_KEY[macro];
  }
  // layout.yaxis2.title = nm;
  return {
    x: src.date,
    y: src[macro],
    type: "scatter",
    mode: "lines",
    name: nm,
    yaxis: 'y2'
  }
}

function chart() {
  if (isNarrow.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } else if (isMobile.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } else if (isTablet.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } else {
    layout.margin.l = 10;
    layout.margin.r = 10;
  }
  var option = {
    // scrollZoom: false,
    displayModeBar:false, 
    responsive:true, 
    showTips:false, 
  }

  Plotly.newPlot('industry-macro', [traceAsset(), traceMacro()], layout, option);
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
    $('.option-industry').append('<option value="' + key + '">' + INDEX_KEY[key] + '</option>');
  }
  
  $('.industry').on('change', function(){
    $('#industry-macro').html('');
    index = $(this).val();
    chart();
  })

  $('.macro').on('change', function(){
    macro = $(this).val();
    chart();
  })
})