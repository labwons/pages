const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
// const __URL__ = '../../../src/json/treemap/treemap.json';
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const abs = (array) => {return array.map(Math.abs);}

let __SRC__ = null;
let E_MOUSE = document.createEvent('MouseEvent');

var base = null;
var data = null;
var spec = null;
var tops = null;
var maxRange = 1.1;


/*--------------------------------------------------------------
# Functions
--------------------------------------------------------------*/
function getCoverNames(){
  tops = [];
  for (var n = base.meta.length - 2; n > 0; n--) {
    tops.push(base.name[n]);
    if (base.meta[n].includes('종가')) { return tops; }
  }
  return tops;
}

function searchReset(){
	$('.map-searchbar').empty();
	$('.map-searchbar').append('<option></option>');
	for (var n = 0; n < base.name.length; n++){
		$('.map-searchbar').append('<option>' + base.name[n] + '</option>');
	}
}

function clickTreemap(item){
  var elements = $('g.slicetext');
	for (var n = 0; n < elements.length; n++){
		if ($(elements[n]).text().includes(item)){
      !$(elements[n]).get(0).dispatchEvent(E_MOUSE);
			return;
		}
	}
}

function rewindOn(){
  if( !$('.map-rewind').attr('class').includes('show') ) {
    $('.map-rewind').toggleClass('show');
  }
}

function rewindOff(){
  if( $('.map-rewind').attr('class').includes('show') ) {
    $('.map-rewind').toggleClass('show');
  }
}

function updateMap() {
  unit = (spec == 'PER' || spec == 'PBR') ? '' : '%';
  data = [{
    type:'treemap',
    branchvalues:'total',
    labels:base.name,
    parents:base.cover,
    values:base.size,
    meta:base.meta,
    text:base[spec],
	  textposition:'middle center',
    textfont:{
      family:'NanumGothic, Nanum Gothic, Open Sans, sans-serif',
      color:'#ffffff'
    },
    texttemplate: '%{label}<br>%{text:.2f}' + unit,
    hovertemplate: '%{meta}<br>' + spec + ': %{text}' + unit + '<extra></extra>',
    hoverlabel: {
      font: {
        family: 'NanumGothic, Nanum Gothic, Open Sans, sans-serif',
        color: '#ffffff'
      }
    },
    opacity: 0.9,
    marker: {
      colors: base[spec + '-C'],
      visible: true
    },
    root_color:'lightgrey'
  }];
  Plotly.newPlot(
    'market-map', 
    data,
    {
      // height: 650,
      margin:{l:0,r:0,t:0,b:25}
    },
    {
      displayModeBar:false,
      responsive:true,
      showTips:false
    }
  );
}

function updateBar() {
  let sorted = {};
  let indices = base[spec].map((value, index) => index);
  var minbar = 1;
  var unit = '%';
  var layout = {
    margin:{
      l:10, 
      r:10, 
      t:10, 
      b:22
    }, 
    autorange:false,
    xaxis:{
      showticklabels: false,
      showline: false,
      range:[0, 0], 
    },
    yaxis:{
      showline: false,
      zeroline: false,
      showticklabels: false
    },

  }
  var option = {
    scrollZoom: false,
    displayModeBar:false, 
    responsive:true, 
    showTips:false, 
    modeBarButtonsToRemove: ['zoom2d', 'pan2d', 'select2d', 'lasso2d'], // 기본 확대/축소 도구 제거
    doubleClick: 'reset'
    // staticPlot:true
  }

  if ((spec == 'PER') || (spec == 'PBR')) {
    unit = '';
  }

  indices.sort((i, j) => base[spec][i] - base[spec][j]);
  for (var key in base) {
    sorted[key] = indices.map(index => base[key][index]);
  }

  if (isMobile.matches){
    maxRange = isNarrow.matches ? 1.35 : 1.3;
    minbar = isNarrow.matches ? 2.4 : 1.8;
  } else {
    minbar = 1;
    maxRange = 1.1;        
  }

  layout.xaxis.range = [0, maxRange * sorted[spec][sorted[spec].length - 1] + minbar];
  layout.annotations = sorted.name.map(function(y, i) {
    return {
      x: 0,
      y: y,
      xref: 'x',
      yref: 'y',
      text: y,
      showarrow: false,
      font: {
        color: 'white',
        size: 14,
      },
      xanchor: 'left',
      yanchor: 'middle',
    };
  });

  data = [{
    type: 'bar',
    x: abs(sorted[spec]).map(function(x) {return x += minbar;}),
    y: sorted.name,
    orientation:'h',
    marker:{
      color:sorted[spec + '-C']
    },
    text:sorted[spec],
    texttemplate:'%{text}' + unit,
    textposition:'outside',
    meta:sorted.meta,
    hovertemplate:'%{meta}<br>' + spec + ': %{x}' + unit + '<extra></extra>',
    opacity:0.9
  }];
  Plotly.newPlot('market-map', data, layout, option);
}


$(document).ready(async function(){
  try {
    const response = await fetch(__URL__);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    __SRC__ = await response.json();
  } catch (error) {
      console.error('Fetch error:', error);
  }

  base = __SRC__[$('.map-type').val()];
  spec = $('.map-option').val();
  tops = getCoverNames();
  updateMap();
  searchReset();
})


$(document).ready(function() {

  /*--------------------------------------------------------------
  # Initialize
  --------------------------------------------------------------*/
  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }

  $('.map-searchbar').select2({
    placeholder: "종목명/섹터/업종"
  })
  
  E_MOUSE.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);


  /*--------------------------------------------------------------
  # Event Bindings
  --------------------------------------------------------------*/
  $('.map-type').on('change', function() {
    base = __SRC__[$('.map-type').val()];
    tops = getCoverNames();
    updateMap();
    searchReset();
  })
  
  $('.map-option').on('change', function() {
    spec = $('.map-option').val();
    updateMap();
  
    if ((spec == 'PER') || (spec == 'PBR')) {
      $('.map-lowest').html('고평가');
      $('.map-lower').html('');
      $('.map-low').html('');
      $('.map-middle').html('평균');
      $('.map-high').html('');
      $('.map-higher').html('');
      $('.map-highest').html('저평가');
    } else if (spec == 'DIV') {
      $('.map-lowest').html('');
      $('.map-lower').html('');
      $('.map-low').html('');
      $('.map-middle').html('0%');
      $('.map-high').html('2%');
      $('.map-higher').html('4%');
      $('.map-highest').html('6%');
    } else if (spec == 'D-1') {
      $('.map-lowest').html('-3%');
      $('.map-lower').html('-2%');
      $('.map-low').html('-1%');
      $('.map-middle').html('0%');
      $('.map-high').html('1%');
      $('.map-higher').html('2%');
      $('.map-highest').html('3%');
    } else if (spec == 'W-1') {
      $('.map-lowest').html('-6%');
      $('.map-lower').html('-4%');
      $('.map-low').html('-2%');
      $('.map-middle').html('0%');
      $('.map-high').html('2%');
      $('.map-higher').html('4%');
      $('.map-highest').html('6%');
    } else if (spec == 'M-1') {
      $('.map-lowest').html('-10%');
      $('.map-lower').html('-6.7%');
      $('.map-low').html('-3.3%');
      $('.map-middle').html('0%');
      $('.map-high').html('3.3%');
      $('.map-higher').html('6.7%');
      $('.map-highest').html('10%');
    } else if (spec == 'M-3') {
      $('.map-lowest').html('-18%');
      $('.map-lower').html('-12%');
      $('.map-low').html('-6%');
      $('.map-middle').html('0%');
      $('.map-high').html('6%');
      $('.map-higher').html('12%');
      $('.map-highest').html('18%');
    } else if (spec == 'M-6') {
      $('.map-lowest').html('-24%');
      $('.map-lower').html('-16%');
      $('.map-low').html('-8%');
      $('.map-middle').html('0%');
      $('.map-high').html('8%');
      $('.map-higher').html('16%');
      $('.map-highest').html('24%');
    } else if (spec == 'Y-1') {
      $('.map-lowest').html('-30%');
      $('.map-lower').html('-20%');
      $('.map-low').html('-10%');
      $('.map-middle').html('0%');
      $('.map-high').html('10%');
      $('.map-higher').html('20%');
      $('.map-highest').html('30%');
    }
  })
  
  $('.map-reset').click(function(){
    updateMap();
    rewindOff();
    $('.map-searchbar').val(null).trigger('change');
  })
  
  $('.map-switch').click(function(){
    var button = $(this).find('i');
    if ( button.attr('class').includes('fa-map-marker') ) {
      $('.map-type').empty();
      $('.map-type').append('<option value="LargeSectors">섹터(대형주)</option>');
      $('.map-type').append('<option value="MidSectors">섹터(중형주)</option>');
      $('.map-type').append('<option value="LargeIndustries">업종(대형주)</option>');      
      $('.map-type').append('<option value="MidIndustries">업종(중형주)</option>');
      base = __SRC__['LargeSectors'];;
      updateBar();
      button.removeClass('fa-map-marker');
      button.addClass('fa-signal');
    } else {
      $('.map-type').empty();
      $('.map-type').append('<option value="LargeCap">대형주</option>');
      $('.map-type').append('<option value="LargeCapWithoutSamsung">대형주(삼성전자 제외)</option>');
      $('.map-type').append('<option value="MidCap">중형주</option>');
      base = __SRC__['LargeCap'];;
      updateMap();
      button.removeClass('fa-signal');
      button.addClass('fa-map-marker');
    }
  })
  
  $('.map-searchbar').on('select2:select', function (e) {
    var selected = e.params.data.text;
  
    if (tops.includes(selected)) {
      clickTreemap(selected);
      return;
    } 
    clickTreemap(base.cover[base.name.indexOf(selected)]);
    
    setTimeout(function(){
      clickTreemap(selected);
    }, 1000)
  });
  
  $('.map-rewind').click(function(){
    !$('.slice').get(0).dispatchEvent(E_MOUSE);
    rewindOff();
  })
  
  $('#market-map').on('plotly_click', function(e, d){
    if ($('g.slice').length == 1) {
      rewindOff();
      return;
    }
    if (!tops.includes(d.points[0].label)){
      rewindOn();
    }
  })
})