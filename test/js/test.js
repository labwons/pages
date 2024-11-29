/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');

let SRC = null;

var mapTyp = 'WS';
var mapFrm = null;
var barTyp = 'industry';
var comOpt = 'D-1';
var viewMd = 'treemap';
var toolbox = false;


/*--------------------------------------------------------------
# Functions
--------------------------------------------------------------*/



function setFrame(){
  mapFrm = SRC.TICKERS;
  Object.values(SRC[mapTyp]).forEach(val => {
    mapFrm = Object.assign({}, mapFrm, val);
  })
}

function setTypeSelector() {
  if (viewMd == 'treemap') {
    $('.map-type')
    .empty()
    .append('<option value="WS">대형주</option>')
    .append('<option value="NS">대형주(삼성전자 제외)</option>')
    $('.map-type option[value="' + mapTyp + '"]').prop('selected', true);
  } else {
    $('.map-type')
    .empty()
    .append('<option value="sector">섹터 Sector</option>')
    .append('<option value="industry">업종 Industry</option>')
    $('.map-type option[value="' + barTyp + '"]').prop('selected', true);
  }
}

function setOptionSelector() {
  Object.entries(SRC.METADATA).forEach(([key, val]) => {
    if((key == "DATE") || (key == "DUPLICATEDGROUP")) {
      return
    }
    $('.map-option').append('<option value="' + key + '">' + val.label + '</option>');
  })
  $('.map-option option[value="' + comOpt + '"]').prop('selected', true);
}

function setSearchSelector(){
  $('.map-searchbar')
    .select2({placeholder: "종목명/섹터/업종"})
    .empty()
	  .append('<option></option>');
  
  $('.map-searchbar').append('<optgroup label="[종목 / Stocks]">');
  Object.entries(SRC.TICKERS)
  .sort((a, b) => b[1].size - a[1].size)
  .forEach(item => {
    if ((mapTyp === "NS") && (item[0] === '005930')) {
      return;
    }
    $('.map-searchbar').append('<option value="' + item[0] + '">' + item[1].name + '</option>');
  })

  $('.map-searchbar').append('<optgroup label="[섹터 / Sectors]">');
  Object.entries(SRC[mapTyp].sector).forEach(([key, val]) => {
    $('.map-searchbar').append('<option value="' + key + '">' + val.name + '</option>');
  })
  $('.map-searchbar').append('<optgroup label="[업종 / Industries]">');
  Object.entries(SRC[mapTyp].industry).forEach(([key, val]) => {
    $('.map-searchbar').append('<option value="' + key + '">' + val.name + '</option>');
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
  var xKey = 'D-1';
  var yKey = 'M-1';
  var xLabel = SRC.LABEL[xKey];
  var yLabel = SRC.LABEL[yKey];
  // var tag = SRC.METADATA[comOpt];
  var layout = setScatterLayout();
  var option = setScatterOption();
  var font = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

  var x = [];
  var y = [];
  var meta = [];
  var size = [];  
  var colors = [];
  Object.entries(SRC.DATA).forEach(([ticker, spec]) => {
    x.push(spec[xKey]);
    y.push(spec[yKey]);
    meta.push(spec["meta"]);
    size.push(spec["size"]);
    // colors.push(val[comOpt][1]);
  })

  layout.xaxis.title = xLabel;
  layout.yaxis.title = yLabel;
  Plotly.newPlot(
    'scatter', 
    [{
      type:'scatter',
      x:x,
      y:y,
      mode:'markers',
      meta:meta,
      hovertemplate: '%{meta}<br>' + xLabel + ': %{x}<br>' + yLabel + ': %{y}<extra></extra>',
      hoverlabel: {
        font: {
          family: font,
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
    $('.js-plotly-plot .plotly .modebar').css({'display':'none'});    
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
    // console.log(SRC);
    // setYRangeSlider();
    // setTypeSelector();
    // setOptionSelector();
    // setFrame();
    setScatter();
    // setScale();
    // setSearchSelector();
  } catch (error) {
      console.error('Fetch error:', error);
  }

  $('.scatter-sector').on('change', function() {   
    
  })

  $('.scatter-x').on('change', function() {
    
  })

  $('.scatter-y').on('change', function() {
    
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
