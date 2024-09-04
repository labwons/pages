// const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
const __URL__ = '../../../src/json/treemap/treemap.json';
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
var view = 'map';
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
      margin:{l:0,r:0,t:0,b:25},
      annotations: [{
        x: 1,
        y: 1,
        xref: 'paper',
        yref: 'paper',
        text: __SRC__.Date,
        showarrow: false,
        xanchor: 'right',
        yanchor: 'top',
        font: {
            size: 12,
            color: 'white'
        }
        
      }]
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
  var minbar = 0;
  var unit = '%';
  var layout = {
    margin:{
      l:10, 
      r:0, 
      t:10, 
      b:22
    }, 
    xaxis:{
      autorange: false,
      showticklabels: false,
      showline: false,
      range:[0, 0], 
    },
    yaxis:{
      showline: false,
      zeroline: false,
      showticklabels: false
    },
    dragmode: false
  }
  var option = {
    scrollZoom: false,
    displayModeBar:false, 
    responsive:true, 
    showTips:false, 
  }

  if ((spec == 'PER') || (spec == 'PBR')) {
    unit = '';
  }

  indices.sort((i, j) => base[spec][i] - base[spec][j]);
  for (var key in base) {
    sorted[key] = indices.map(index => base[key][index]);
  }
  if (isNarrow.matches) {
    maxRange = 1.35 * Math.max(...abs(sorted[spec]));
  } else if (isMobile.matches) {
    maxRange = 1.3 * Math.max(...abs(sorted[spec]));
  } else if (isTablet.matches) {
    maxRange = 1.2 * Math.max(...abs(sorted[spec]));
  } else {
    maxRange = 1.1 * Math.max(...abs(sorted[spec]));
  }
  minbar = 0.45 * maxRange;

  layout.xaxis.range = [0, maxRange + minbar];
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
        size: 13,
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
    hovertemplate:'%{meta}<br>' + spec + ': %{text}' + unit + '<extra></extra>',
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
  $('.map-date').html(__SRC__.Date);
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
    if (view == 'map') {
      tops = getCoverNames();
      updateMap();
      searchReset();
    } else{
      updateBar();
    }
  })
  
  $('.map-option').on('change', function() {
    spec = $('.map-option').val();
    if (view == 'map') {
      updateMap();
    } else {
      updateBar();
    }
  
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
    if ( button.attr('class').includes('fa-map-o') ) {
      $('.map-type').empty();
      $('.map-type').append('<optgroup label="---- [대형주 / Large Cap]">');
      $('.map-type').append('<option value="LargeSectors" selected="selected">섹터</option>');
      $('.map-type').append('<option value="LargeIndustries">업종</option>');      
      $('.map-type').append('<optgroup label="---- [중형주 / Mid Cap]">');
      $('.map-type').append('<option value="MidSectors">섹터</option>');      
      $('.map-type').append('<option value="MidIndustries">업종</option>');
      view = 'bar';
      button.removeClass('fa-map-o');
      button.addClass('fa-signal');
      $('.map-searchbar').prop('disabled', true);
      if ($('.map-rewind').attr('class').includes('show')){
        rewindOff();
      }
    } else {
      $('.map-type').empty();
      $('.map-type').append('<option value="LargeCap" selected="selected">대형주</option>');
      $('.map-type').append('<option value="LargeCapWithoutSamsung">대형주(삼성전자 제외)</option>');
      $('.map-type').append('<option value="MidCap">중형주</option>');
      view = 'map';
      button.removeClass('fa-signal');
      button.addClass('fa-map-o');
      $('.map-searchbar').prop('disabled', false);
    }
    base = __SRC__[$('.map-type').val()];
    if (view == 'map') {
      updateMap();
    } else {
      updateBar();
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
    if (view == 'map') {
      !$('.slice').get(0).dispatchEvent(E_MOUSE);
      rewindOff();
    }
  })
  
  $('#market-map').on('plotly_click', function(e, d){
    if (view == 'map'){
      if ($('g.slice').length == 1) {
        rewindOff();
        return;
      }
      if (!tops.includes(d.points[0].label)){
        rewindOn();
      }
    } else {
      return;
    }
  })
})