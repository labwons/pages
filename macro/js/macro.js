const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const parseDate = (dateStr) => new Date(dateStr + 'T00:00:00Z')

var tr1 = {};
var tr2 = {};
var macro = null;

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
  // ticklabelposition: 'inside',
  // position: 0.01,
  showline: true,
  zeroline: false,
  showticklabels: true,
  tickangle: -90
};

var yaxis2 = {
  overlaying:'y',
  // ticklabelposition: 'inside',
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
    .select2({placeholder: obj.attr('data-name') + ' 지표/지수 선택'})
    .empty()
    .append('<option></option>');
    // .append('<option value="" disabled selected>' + obj.attr('data-name') + ' 지표/지수 선택</option>');
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

function chart(trace1={}, trace2={}) {
  if ($('.macro-before').css('display') == 'flex'){
    $('.macro-before').css('display', 'none');
  }
  // if (trace1){
  //   layout.yaxis.title = trace1.meta;
  // }
  // if (trace2){
  //   layout.yaxis2.title = trace2.meta;
  // }
  
  Plotly.newPlot('macro', [trace1, trace2], layout, option);
}


$(document).ready(async function(){
  try {
    const macroFetch = await fetch('../../dev/json/service/macro.json');
    if (!macroFetch.ok) {
      throw new Error('Network response was not ok');
    }
    macro = await macroFetch.json();
  } catch (error) {
    console.error('Fetch error:', error);
  }

  setSelect($('.macro-option1'), macro.META, true);
  setSelect($('.macro-option2'), macro.META, true);
  
  $('.macro-option1').on('change', function(){
    var key = $(this).val();
    if (key in macro.ECOS){
      var date = macro.ECOS[key].date;
      var data = macro.ECOS[key].data;
      var unit = macro.META[key].unit;      
    } else if (key in macro.WISE){
      var date = macro.WISE.date;
      var data = macro.WISE[key];
      var unit = '';
    } else {
      return;
    }
    tr1 = {
      x:date,
      y:data,
      type:"scatter",
      mode:"lines",
      name:macro.META[key].name,
      showlegend:true,
      line: {
        color:'black'
      },
      yaxis:'y1',
      hovertemplate:'%{y}' + unit,
      meta:macro.META[key].name + '[' + unit + ']'
    }
    chart(tr1, tr2);
  })

  $('.macro-option2').on('change', function(){
    if (tr1.length == 0){
      alert('Y1 지표/지수를 먼저 선택해주세요');
      $('.macro-option2').each(function() {
        $(this).find('option').first().prop('selected', true);
      });
      return
    }
    var key = $(this).val();
    if (key in macro.ECOS){
      var date = macro.ECOS[key].date;
      var data = macro.ECOS[key].data;
      var unit = macro.META[key].unit;      
    } else if (key in macro.WISE){
      var date = macro.WISE.date;
      var data = macro.WISE[key];
      var unit = '';
    } else {
      return;
    }
    tr2 = {
      x:date,
      y:data,
      type:"scatter",
      mode:"lines",
      name:macro.META[key].name,
      showlegend:true,
      line: {
        color:'royalblue'
      },
      yaxis:'y2',
      hovertemplate:'%{y}' + unit,
      meta:macro.META[key].name + '[' + unit + ']'
    }
    chart(tr1, tr2);
  })
})

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