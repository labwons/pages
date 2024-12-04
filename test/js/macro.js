const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const parseDate = (dateStr) => new Date(dateStr + 'T00:00:00Z')

var tr1 = {};
var tr2 = {};
var ecos = null;

var legend = {
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
};

var xaxis = {
  type:'date',
  tickformat: "%Y/%m/%d",
  showticklabels: true,
  showline: true,
  // range:['2023-12-04', '2024-12-04'],
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
  }
};

var yaxis = {
  side: 'left',
  ticklabelposition: 'inside',
  // position: 0.01,
  showline: true,
  zeroline: false,
  showticklabels: true,
  tickangle: -90
};

var yaxis2 = {
  overlaying:'y',
  ticklabelposition: 'inside',
  side:'right',
  // position: 0,
  zeroline:false,
  showline:true,
  showgrid:false,
  showticklabels: true,
  tickangle: -90,
  linecolor: 'royalblue'
};

var layout = {
  margin:{
    l:20, 
    r:20, 
    t:0, 
    b:20
  }, 
  dragmode: 'pan',
  hovermode: 'x unified',
  legend: legend,
  xaxis: xaxis,
  yaxis: yaxis,
  yaxis2: yaxis2,
}

var option = {
  displayModeBar:true, 
  responsive:true, 
  showTips:false, 
  displaylogo:false,
  modeBarButtonsToRemove: [
    // 'toImage','select2d','lasso2d','zoomOut2d','zoomIn2d','resetScale2d'
    'toImage','select2d','lasso2d','resetScale2d'
  ]  
}

function setSelect(obj, meta, clear=false){
  if (clear) {
    obj
    .empty()
    .append('<option value="" disabled selected>' + obj.attr('data-name') + ' 지표/지수 선택</option>');
  }
  var categories = {};
  Object.entries(meta).forEach(([key, item]) => {
    if (!(item.category in categories)) {
      categories[item.category] = [];
    }
    categories[item.category].push({
      'key': key,
      'name': item.name
    });
  })

  Object.keys(categories).forEach(category => {
    obj.append('<optgroup label="[' + category + ']">');
    categories[category].forEach(item => {
      obj.append('<option value="' + item.key + '">' + item.name + '</option>');
    })
  })
}

function trace(data) {
  return {
    x: data.date,
    y: data.data,
    type: "scatter",
    mode: "lines",
    name: "",
    showlegend:true,
    line: {
      color: 'black'
    },
    yaxis: 'y1'
  };
}

function chart(trace1={}, trace2={}) {
  if ($('.bar-before').css('display') == 'flex'){
    $('.bar-before').css('display', 'none');
  }
  if (trace1){
    layout.yaxis.title = trace1.meta;
  }
  if (trace2){
    layout.yaxis2.title = trace2.meta;
  }
  
  Plotly.newPlot('macro', [trace1, trace2], layout, option);
}


$(document).ready(async function(){
  try {
    const ecosFetch = await fetch('../../dev/json/macro/ecos.json');
    if (!ecosFetch.ok) {
      throw new Error('Network response was not ok');
    }
    ecos = await ecosFetch.json();
  } catch (error) {
    console.error('Fetch error:', error);
  }

  setSelect($('.bar-option1'), ecos.META, true);
  setSelect($('.bar-option2'), ecos.META, true);
  
  $('.bar-option1').on('change', function(){
    var key = $(this).val();
    if (key in ecos.DATA){
      tr1 = trace(ecos.DATA[key]);
      tr1.name = ecos.META[key].name;
      tr1.yaxis = 'y1';
      tr1.line.color='black';
      tr1.hovertemplate = '%{y}' + ecos.META[key].unit;
      tr1.meta = ecos.META[key].name + '[' + ecos.META[key].unit + ']';
    }
    chart(tr1, tr2);
  })

  $('.bar-option2').on('change', function(){
    if (tr1.length == 0){
      alert('Y1 지표/지수를 먼저 선택해주세요');
      $('.bar-option2').each(function() {
        $(this).find('option').first().prop('selected', true);
      });
      return
    }
    var key = $(this).val();
    if (key in ecos.DATA){
      tr2 = trace(ecos.DATA[key]);
      tr2.name = ecos.META[key].name;
      tr2.yaxis = 'y2';
      tr2.line.color='royalblue';
      tr2.hovertemplate = '%{y}' + ecos.META[key].unit;
      tr2.meta = ecos.META[key].name + '[' + ecos.META[key].unit + ']';
    }
    chart(tr1, tr2);
  })
})

