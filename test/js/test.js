/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const fontFamily = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

let SRC = null;
var group = 'all';
var xOpt = 'D-1';
var yOpt = 'Y-1';
var toolbox = false;


/*--------------------------------------------------------------
# Functions
--------------------------------------------------------------*/

function setCategory(){
  var sector = {};
  var industry = {};

  Object.entries(SRC.CATEGORY).forEach(([key, val]) => {
    if (key.startsWith('G')) {
      sector[key] = val;
    } else if (key.startsWith('W')) {
      industry[key] = val;
    }
  })

  $('.scatter-sector')
  .empty()
  .append('<option value="all">' + (group == 'all' ? '분류: 전체' : '전체') + '</option>')
  .append('<optgroup label="[섹터 / Sector]">');
  Object.entries(sector).forEach(([key, val]) => {
    if (key == group) val = '분류: ' + val;
    $('.scatter-sector').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-sector').append('<optgroup label="[업종 / Industry]">');
  Object.entries(industry).forEach(([key, val]) => {
    if (key == group) val = '분류: ' + val;
    $('.scatter-sector').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-sector').val(group);
}

function setX() {
  $('.scatter-x').empty();
  Object.entries(SRC.LABEL).forEach(([key, val]) => {
    if (key == xOpt) val = 'X값: ' + val;
    $('.scatter-x').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-x').val(xOpt);
}

function setY() {
  $('.scatter-y').empty();
  Object.entries(SRC.LABEL).forEach(([key, val]) => {
    if (key == yOpt) val = 'Y값: ' + val;
    $('.scatter-y').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-y').val(yOpt);
}

function setSearchSelector(){
  $('.scatter-searchbar')
    .select2({placeholder: "종목명/섹터/업종"})
    .empty()
	  .append('<option></option>');
  
  $('.scatter-searchbar').append('<optgroup label="[종목 / Stocks]">');
  Object.entries(SRC.DATA)
  .sort((a, b) => b[1].size - a[1].size)
  .forEach(item => {
    $('.scatter-searchbar').append('<option value="' + item[0] + '">' + item[1].name + '</option>');
  })
}

function setScatterLayout() {
  return {
    dragmode: false,
    margin:{l:20, r:2, t:0, b:35},
    xaxis:{
      showline:true,
      zerolinecolor:"lightgrey",
      gridcolor:"lightgrey",
    },
    yaxis:{
      ticklabelposition: 'inside',
      showline:true,
      zerolinecolor:"lightgrey",
      gridcolor:"lightgrey",
    },
    annotations: [{
      text: SRC.DATE,
      x: 1,
      y: 0,
      xref: 'paper',
      yref: 'paper',      
      xanchor: 'right',
      yanchor: 'bottom',
      showarrow: false,
      align: 'right',
      font: {
        family:fontFamily,
        size: 12,
        color: 'black'
      }
    }, {
      text: 'LAB￦ONS',
      x: 0,
      y: 0,
      xref: 'paper',
      yref: 'paper',      
      xanchor: 'left',
      yanchor: 'bottom',
      showarrow: false,
      align: 'left',
      font: {
        family:fontFamily,
        size: 12,
        color: 'black'
      }
    }]
  }
}

function setScatterOption() {
  return {
    showTips:false,
    responsive:true,
    displayModeBar:true,
    displaylogo:false,
    modeBarButtonsToRemove: [
      'toImage','select2d','lasso2d','zoomOut2d','zoomIn2d','resetScale2d'
    ]    
  }
}

function setScatter() {
  var layout = setScatterLayout();
  var option = setScatterOption();
  var xName = SRC.LABEL[xOpt];
  var yName = SRC.LABEL[yOpt];

  var x = [];
  var y = [];
  var meta = [];
  var size = [];  
  var colors = [];
  Object.entries(SRC.DATA).forEach(([ticker, spec]) => {
    x.push(spec[xOpt]);
    y.push(spec[yOpt]);
    meta.push(spec["meta"]);
    size.push(spec["size"]);
    // colors.push(val[comOpt][1]);
  })

  layout.xaxis.title = xName;
  layout.yaxis.title = yName;
  Plotly.newPlot(
    'scatter', 
    [{
      type:'scatter',
      x:x,
      y:y,
      mode:'markers',
      meta:meta,
      hovertemplate: '%{meta}<br>' + xName + ': %{x}<br>' + yName + ': %{y}<extra></extra>',
      hoverlabel: {
        font: {
          family: fontFamily,
          color: '#ffffff'
        }
      },
      marker: {
        size:size,
        color: 'rolayblue',
        line: {
          width:1.0,
          color:'blue'
        },
        opacity: 0.6,        
      },
    }],
    layout,
    option
  ).then(function(){
    if (!toolbox) {
      $('.js-plotly-plot .plotly .modebar').css({'display':'none'});
    }
  });
}



/*--------------------------------------------------------------
# FETCH & BINDINGS
--------------------------------------------------------------*/
$(document).ready(async function(){
  try {
    const response = await fetch('../../dev/json/service/bubble.json');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    
    SRC = await response.json();
    console.log(SRC);

    setX();
    setY();
    setCategory();
    setScatter();
    setSearchSelector();
  } catch (error) {
      console.error('Fetch error:', error);
  }

  $('.scatter-sector').on('change', function() {   
    group = $(this).val();
    setCategory();
  })

  $('.scatter-x').on('change', function() {
    xOpt = $(this).val();
    setX();
    setScatter();
  })

  $('.scatter-y').on('change', function() {
    yOpt = $(this).val();
    setY();
    setScatter();
  })

  $('.scatter-edit').on('click touch', function(){
    toolbox = !toolbox;
    if (toolbox) {
      $('.scatter-edit i')
      .removeClass('fa-pencil')
      .addClass('fa-lock');
      $('.js-plotly-plot .plotly .modebar').css({
        'display':'flex',
        'background-color':'rgba(200, 200, 200, 0.4)'
      })
      $('.js-plotly-plot .plotly .modebar-group').css({
        'padding':'0'
      })
      $('.js-plotly-plot .plotly .modebar-btn').css({
        'padding':'0 5px'
      })
      Plotly.relayout('scatter', {
        'dragmode': "zoom",
      })
    } else {
      $('.scatter-edit i')
      .removeClass('fa-lock')
      .addClass('fa-pencil');
      $('.js-plotly-plot .plotly .modebar').css({'display':'none'})
      Plotly.relayout('scatter', {
        'dragmode': false,
      })
    }
    
  })

  $('.scatter-searchbar').on('select2:select', function (e) {
    // var ticker = e.params.data.id;
    // if (ticker.startsWith('W')) {
    //   var elem = SRC[mapTyp].industry[ticker];
    //   clickTreemap(elem.name);
    //   return
    // } else if (ticker.startsWith('G')) {
    //   var elem = SRC[mapTyp].sector[ticker];
    //   clickTreemap(elem.name);
    //   return
    // } else {
    //   var elem = SRC.TICKERS[ticker];
    //   clickTreemap(elem.ceiling);
    //   setTimeout(function(){
    //     clickTreemap(elem.name);
    //   }, 1000);      
    // }
  });
  
})
