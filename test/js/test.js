/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');

const ySliderWidth  = 16;
const ySliderHeight = ySliderWidth / 2;
const yDomOffset = parseFloat($('.y-range-slider').offset().top);
const yDomHeight = parseFloat($('.y-range-slider').height());


let SRC = null;

var mapTyp = 'WS';
var mapFrm = null;
var barTyp = 'industry';
var comOpt = 'D-1';
var viewMd = 'treemap';

var ySlope = null;
var yRange = null;
var yMaxActv = false;
var yMinActv = false;
var yHeight = null; // [px]
var yMaxPos = null; // [px] Absolute Position with respect to Window
var yMinPos = null; // [px] Absolute Position with respect to Window
var yMax = null;
var yMin = null;
var xmax = 100;
var xmin = 0;


/*--------------------------------------------------------------
# Functions
--------------------------------------------------------------*/
function yAbsolutePx2RelativePercent(px) {
  return 100 * (px - yDomOffset) / yDomHeight;
}

function setYRangeSlider(){
  var plotlyObj = $('#scatter .nsewdrag');

  yRange = $('#scatter')[0].layout.yaxis.range;
  yMax = yRange[1];
  yMin = yRange[0];

  if (plotlyObj.length) {
      yHeight = parseFloat(plotlyObj.attr('height'));
      yMaxPos = yDomOffset;
      yMinPos = yDomOffset + yHeight;
      ySlope = (yRange[0] - yRange[1]) / yHeight;
  } else {
    return
  }

  $('.y-range').css({
    "position": "absolute",
    "width": "2px",
    "height": yHeight,
    "background-color": "#c8c8c8",
    // "z-index": 10 // Deprecated
  });

  $('.y-range-upper, .y-range-lower').css({
    "position": "absolute",
    "width": ySliderWidth + "px",
    "height": ySliderHeight+ "px",
    "background-color": "#fff",
    "border": "0.5px solid grey",
    "border-radius": "30%",
    "cursor": "ns-resize",
    'transform': "translateX(-50%)"
  });

  $('.y-range-upper').css({
    'top': yAbsolutePx2RelativePercent(yMaxPos) + '%',
    'left': '50%',
    // "background-color": "#f00", // Deprecated
  });

  $('.y-range-lower').css({
    'top': yAbsolutePx2RelativePercent(yMinPos - ySliderHeight) + '%',
    'left': '50%',
    // "background-color": "#0f0", // Deprecated
  });

  $('.y-range-upper-block').css({
    'height': 0
  });
  $('.y-range-lower-block').css({
    'height': 0
  });
}


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

function setScale(){
  var tag = SRC.METADATA[comOpt];
  $('.map-legend span').each(function(n){
    if(tag.bound[n] == null){
      $(this).html('&nbsp; - &nbsp;');
    } else {
      $(this).html(String(tag.bound[n]) + tag.unit);
    }
    $(this).css('background-color', tag.scale[n]);
  })
}

function setScatterLayout() {
  return {
    dragmode: false,
    margin:{l:10, r:2, t:0, b:20},
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
    // annotations: [{
    //   text: '2024-11-25 ',
    //   x: 1,
    //   y: 1,
    //   xref: 'paper',
    //   yref: 'paper',      
    //   xanchor: 'right',
    //   yanchor: 'top',
    //   showarrow: false,      
    //   font: {
    //       size: 12,
    //       color: 'white'
    //   }
    // }]
  }
}


function setScatterOption() {
  return {
    displayModeBar:false,
    responsive:true,
    showTips:false
  }
}

function setScatter() {
  var xLabel = "D-1";
  var yLabel = "M-1";
  // var tag = SRC.METADATA[comOpt];
  var layout = setScatterLayout();
  var option = setScatterOption();
  var font = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

  var x = [];
  var y = [];
  var meta = [];
  var size = [];  
  var colors = [];
  Object.entries(SRC).forEach(([ticker, spec]) => {
    x.push(spec[xLabel]);
    y.push(spec[yLabel]);
    meta.push(spec["meta"]);
    // size.push(val.size);
    // colors.push(val[comOpt][1]);
  })

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
      opacity: 0.9,
      // marker: {
      //   colors: colors,
      //   visible: true
      // },
    }],
    layout,
    option
  ).then(function() {
    setYRangeSlider();
});
}



/*--------------------------------------------------------------
# FETCH & BINDINGS
--------------------------------------------------------------*/
$(document).ready(async function(){
  try {
    const response = await fetch('../../dev/json/group/specs.json');
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

  $(window).on('resize', function() {
    setYRangeSlider();
});

  $('.y-range-upper').on('mousedown touchstart', function(e) {
    yMaxActv = true;
  })

  $('.y-range-lower').on('mousedown touchstart', function(e) {
    yMinActv = true;
  })

  $('.scatter-sector').on('change', function() {   
    
  })

  $('.scatter-x').on('change', function() {
    
  })

  $('.scatter-y').on('change', function() {
    
  })

  $('.map-reset').click(function(){
       
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

function updateSliderYMax(event) {
  var yLimHigh = yDomOffset;
  var yLimLow = yMinPos - 2 * ySliderHeight;
  yMaxPos = event.pageY;
  if (!yMaxPos) {
    event.preventDefault();
    yMaxPos = event.touches[0].pageY;
  }
  console.log(yMaxPos);
  if (yMaxPos <= yLimHigh) yMaxPos = yLimHigh;
  if (yMaxPos >= yLimLow) yMaxPos = yLimLow;
  $('.y-range-upper').css('top', yAbsolutePx2RelativePercent(yMaxPos) + '%');
  $('.y-range-upper-block').css({
    'top': '0%',
    'height': yMaxPos - yDomOffset
  });

  yRange[1] = ySlope * (yMaxPos - yDomOffset) + yMax;
  Plotly.relayout('scatter', {
    'yaxis.range': yRange
  })
}

function updateSliderYMin(event) {
  var yLimHigh = yMaxPos + ySliderHeight;
  var yLimLow  = yDomOffset + yHeight - ySliderHeight;
  yMinPos = event.pageY;
  if (!yMinPos) {
    event.preventDefault();
    yMinPos = event.touches[0].pageY;
  }
  console.log(yMinPos);
  if (yMinPos >= yLimLow) yMinPos = yLimLow;
  if (yMinPos <= yLimHigh) yMinPos = yLimHigh;
  $('.y-range-lower').css('top', yAbsolutePx2RelativePercent(yMinPos) + '%');
  $('.y-range-lower-block').css({
    'top': yAbsolutePx2RelativePercent(yMinPos + ySliderHeight) + '%',
    'height': yDomHeight - yMinPos + ySliderHeight
  });
  
  yRange[0] = ySlope * (yMinPos - yDomOffset) + yMax;
  Plotly.relayout('scatter', {
    'yaxis.range': yRange
  })
}

$(document).on('mousemove touchmove', function(e) {
  if (yMaxActv) {
    updateSliderYMax(e);
  } else if (yMinActv) {
    updateSliderYMin(e);
  }
})


$(document).on('mouseup touchend', function() {
  yMaxActv = false;
  yMinActv = false;
})

$('#scatter').on('plotly_doubleclick', function() {
  setYRangeSlider();
})