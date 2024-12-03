const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const parseDate = (dateStr) => new Date(dateStr + 'T00:00:00Z')

var index_data = null;
var index = null;
var index_start = null;
var index_end = null;

var macro_data = null;
var macro = null;

var layout = {
  margin:{
    l:20, 
    r:20, 
    t:10, 
    b:20
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
    showticklabels: true,
    showline: true,
    rangeselector: {
      buttons: [
        { step: 'all', label: 'All' },
        { count: 6, label: '6M', step:'month', stepmode: 'backward'},
        { count: 1, label: 'YTD', step:'year', stepmode: 'todate'},
        { count: 1, label: '1Y', step: 'year', stepmode: 'backward' },
        { count: 3, label: '3Y', step: 'year', stepmode: 'backward' },
        { count: 5, label: '5Y', step: 'year', stepmode: 'backward' }        
      ],
      xanchor: 'left',
      x: 0,
      yanchor: 'top',
      y:1.025
    },
    
  },
  yaxis:{
    side: 'left',
    // position: 0.01,
    showline: true,
    zeroline: false,
    showticklabels: true,
    tickangle: -90
  },
  yaxis2: {
    overlaying:'y',
    side:'right',
    // position: 0,
    zeroline:false,
    showline:true,
    showgrid:false,
    showticklabels: true,
    tickangle: -90,
    linecolor: 'royalblue'
  },
  dragmode: 'pan'
  // dragmode: false
}

function traceAsset() {
  if (index == null){
    return {};
  }
  var data = index_data[index];
  var range = data.slice(index_start);
  layout.yaxis.range = [0.95 * Math.min(...range), 1.05 * Math.max(...range)];
  return {
    x: data.date,
    y: data.data,
    type: "scatter",
    mode: "lines",
    name: index,
    showlegend:true,
    line: {
      color: 'black'
    },
    yaxis: 'y1'
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
  const date_look_for = parseDate(index_data.date[index_start]);
  const dates = src.date.map(parseDate);
  const macro_start = (() => {
    const findClosestDateIndex = (targetDate, dates) => {
      let closestIndex = 0;
      let minDiff = Math.abs(targetDate - dates[0]);

      for (let i = 1; i < dates.length; i++) {
        const diff = Math.abs(targetDate - dates[i]);
        if (diff < minDiff) {
          minDiff = diff;
          closestIndex = i;
        }
      }
      return closestIndex;
    };
    return findClosestDateIndex(targetDate, dates);
  })();

  return {
    x: src.date,
    y: src[macro],
    type: "scatter",
    mode: "lines",
    name: nm,
    yaxis: 'y2',
    line: {
      color: 'royalblue'
    }
  }
}

function chart() {
  if ($('.bar-before').css('display') == 'flex'){
    $('.bar-before').css('display', 'none');
  }
  if (isNarrow.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } else if (isMobile.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } else if (isTablet.matches) {
    layout.margin.l = 10;
    layout.margin.r = 10;
  } 
  var option = {
    // scrollZoom: false,
    displayModeBar:false, 
    responsive:true, 
    showTips:false, 
  }
  // layout.xaxis.range = [index_data.date[index_start], index_data.date[index_end]];


  Plotly.newPlot('industry-macro', [traceAsset(), traceMacro()], layout, option);
}


$(document).ready(async function(){
  try {
    const response = await fetch('../../dev/json/macro/ecos.json');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    index_data = await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
  }
  for(let key in index_data){
    $('.industry').append('<option value="' + key + '">' + key + '</option>');
    $('.option-industry').append('<option value="' + key + '">' + key + '</option>');
    
  }
  index_start = index_data.date.length - 252 * 3;
  index_end = index_data.date.length - 1;
})

$(document).ready(function(){
  
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