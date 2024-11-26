/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const abs = (array) => {return array.map(Math.abs);}

let SRC = null;

var mapTyp = 'WS';
var mapFrm = null;
var barTyp = 'industry';
var comOpt = 'D-1';
var viewMd = 'treemap';

var ymax_active = false;
var ymax = 100;
var ymin = 0;
var xmax = 100;
var xmin = 0;


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
    margin:{l:50, r:2, t:0, b:15},
    xaxis:{
      showline:true,
      zerolinecolor:"lightgrey",
      gridcolor:"lightgrey",
      rangeslider: {},
    },
    yaxis:{
      ticklabelposition: 'inside',
      showline:true,
      zerolinecolor:"lightgrey",
      gridcolor:"lightgrey",
      rangeslider: {}
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
  var yLabel = "Y-1";
  // var tag = SRC.METADATA[comOpt];
  var layout = setScatterLayout();
  var option = setScatterOption();
  var font = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

  var x = [];
  var y = [];
  var parents = [];
  var values = [];
  var meta = [];
  var text = [];
  var colors = [];
  Object.entries(SRC).forEach(([ticker, spec]) => {
    x.push(spec[xLabel]);
    y.push(spec[yLabel]);
    meta.push(spec["meta"]);
    // values.push(val.size);
    // customdata.push(key);
    // meta.push(val.meta);
    // text.push(val[comOpt][0]);
    // colors.push(val[comOpt][1]);
  })

  // $("#x-range-max").attr("max", Math.max(...x));
  // $("#x-range-max").attr("min", Math.max(...x));

  Plotly.newPlot(
    'scatter', 
    [{
      type:'scatter',
      x:x,
      y:y,
      mode:'markers',
      // customdata: customdata,
      meta:meta,
      // text:text,
      // textposition:'middle center',
      // textfont:{
      //   family:font,
      //   color:'#ffffff'
      // },
      // texttemplate: '%{label}<br>%{text}',
      // hovertemplate: '%{meta}' + tag.label + ': %{text}<extra></extra>',
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
  );
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
    // setTypeSelector();
    // setOptionSelector();
    // setFrame();
    // setScatter();
    // setScale();
    // setSearchSelector();
  } catch (error) {
      console.error('Fetch error:', error);
  }

  $('.circle-1').on('mousedown', function(e) {
    ymax_active = true;
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
  
  $('#market-map').on('plotly_click', function(e, d){
    
  })
})

$(document).on('mousemove', function(e) {
  if (ymax_active) {
    let yrange = $('.range-slider');
    let ylimit = yrange.height() - 20;
    let newY = e.pageY - yrange.offset().top;
    
    if (newY <= 0) newY = 0;
    if (newY >= ylimit) newY = ylimit;
    $('.circle-1').css('top', newY + 'px');
  }

})

$(document).on('mouseup', function() {
  ymax_active = false;
})