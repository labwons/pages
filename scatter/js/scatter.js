/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const fontFamily = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';
const sectorColor = {
  "G10": "rgb(92,168,155)",
  "G15": "rgb(86, 152, 168)",
  "G20": "rgb(96, 103, 184)",
  "G25": "rgb(195, 102, 56)",
  "G30": "rgb(96, 185, 120)",
  "G35": "rgb(94, 156, 59)",
  "G40": "rgb(142, 182, 77)",
  "G45": "rgb(207, 90, 92)",
  "G50": "rgb(210, 145, 65)",
  "G55": "rgb(86, 80, 199)",
  "G99": "rgb(132, 62, 173)"
}
let SRC = null;
var group = 'all';
var xOpt = 'D-1';
var yOpt = 'Y-1';
var toolbox = false;
var sizing = true;


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
  var val = null;
  $('.scatter-x').empty();
  Object.entries(SRC.META).forEach(([key, obj]) => {
    val = obj.label;
    if (key == xOpt) val = 'X: ' + val;
    $('.scatter-x').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-x').val(xOpt);
}

function setY() {
  var val = null;
  $('.scatter-y').empty();
  Object.entries(SRC.META).forEach(([key, obj]) => {
    val = obj.label;
    if (key == yOpt) val = 'Y: ' + val;
    $('.scatter-y').append('<option value="' + key + '">' + val + '</option>');
  })
  $('.scatter-y').val(yOpt);
}

function toggleToolbox() {
  toolbox = !toolbox;
  if (toolbox) {
    $('.scatter-edit i')
    .removeClass('fa-edit')
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
    .addClass('fa-edit');
    $('.js-plotly-plot .plotly .modebar').css({'display':'none'})
    Plotly.relayout('scatter', {
      'dragmode': false,
    })
  }
}

function setSearchSelector(){
  $('.scatter-searchbar')
    .select2({placeholder: "종목명 검색"})
    .empty()
	  .append('<option></option>');
  
  $('.scatter-searchbar').append('<optgroup label="[종목 / Stocks]">');
  Object.entries(SRC.DATA)
  .sort((a, b) => b[1].size - a[1].size)
  .forEach(([ticker, obj]) => {
    if ((group == "all") || (group == obj.sectorCode) || (group == obj.industryCode)){
      $('.scatter-searchbar').append('<option value="' + ticker + '">' + obj.name + '</option>');
    }
  })
}

function setScatterLayout() {
  return {
    dragmode: toolbox ? true:false,
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
      // 'toImage','select2d','lasso2d','zoomOut2d','zoomIn2d','resetScale2d'
      'toImage','select2d','lasso2d','resetScale2d'
    ]    
  }
}

function setScatter() {
  var layout = setScatterLayout();
  var option = setScatterOption();
  var xName = SRC.META[xOpt].label;
  var xUnit = SRC.META[xOpt].unit;
  var yName = SRC.META[yOpt].label;
  var yUnit = SRC.META[yOpt].unit;

  var x = [];
  var y = [];
  var meta = [];
  var size = [];  
  var colors = [];
  Object.entries(SRC.DATA).forEach(([ticker, spec]) => {
    if ((group == "all") || (group == spec.sectorCode) || (group == spec.industryCode)){
      x.push(spec[xOpt]);
      y.push(spec[yOpt]);
      meta.push(spec["meta"]);
      if (sizing) {
        size.push(spec["size"]);
      } else {
        size.push(8);
      }
      colors.push(sectorColor[spec["sectorCode"]]);
    }
  })

  layout.xaxis.title = xName + (xUnit ? '[' + xUnit + ']' : '');
  layout.yaxis.title = yName + (yUnit ? '[' + yUnit + ']' : '');
  Plotly.newPlot(
    'scatter', 
    [{
      type:'scatter',
      x:x,
      y:y,
      mode:'markers',
      meta:meta,
      hovertemplate: '%{meta}<br>' + xName + ': %{x}' + xUnit + '<br>' + yName + ': %{y}' + yUnit + '<extra></extra>',
      hoverlabel: {
        font: {
          family: fontFamily,
          color: '#ffffff'
        }
      },
      marker: {
        size:size,
        // color: 'rolayblue',
        color:colors,
        line: {
          width:1.0,
          // color:'blue'
        },
        opacity: 0.7,        
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
    // console.log(SRC);
    setX();
    setY();
    setCategory();
    setScatter();
    setSearchSelector();
    if (window.matchMedia("(min-width: 1024px)").matches){
      toggleToolbox();
    }
  } catch (error) {
      console.error('Fetch error:', error);
  }

  $('.scatter-sector').on('change', function() {   
    group = $(this).val();
    setCategory();
    setScatter();
    setSearchSelector();
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
    toggleToolbox();
  })

  $('.scatter-sizing').on('click touch', function(){
    sizing = !sizing;
    if (sizing) {
      $('.scatter-sizing i')
      .removeClass('fa-exand')
      .addClass('fa-compress');
      setScatter();
    } else {
      $('.scatter-sizing i')
      .removeClass('fa-compress')
      .addClass('fa-expand');
      setScatter();
    }
  })

  $('.scatter-searchbar').on('select2:select', function (e) {
    var obj = SRC.DATA[e.params.data.id];
    Plotly.relayout('scatter', {
      'xaxis.range': [0.9 * obj[xOpt], 1.1 * obj[xOpt]],
      'yaxis.range': [0.9 * obj[yOpt], 1.1 * obj[yOpt]]
    })  
  });
  
})
