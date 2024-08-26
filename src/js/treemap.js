// const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
const __URL__ = '../../../src/json/treemap/treemap.json';


let __SRC__ = null;
let E_MOUSE = document.createEvent('MouseEvent');

var base = null;
var data = null;
var spec = null;
var tops = null;


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

function updateMarketMap() {
  unit = (spec == 'PER' || spec == 'PBR') ? '' : '%';
  data = {
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
  }
  Plotly.newPlot(
    'market-map', 
    [data],
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

$('.map-type').on('change', function() {
  base = __SRC__[$('.map-type').val()];
  tops = getCoverNames();
  updateMarketMap();
  searchReset();
})

$('.map-option').on('change', function() {
  spec = $('.map-option').val();
  updateMarketMap();

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

$('.map-reset').click(function(){
    updateMarketMap();
    rewindOff();
    $('.map-searchbar').val(null).trigger('change');
})

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
  updateMarketMap();
  searchReset();
})


$(document).ready(function() {
  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }

  $('.map-searchbar').select2({
    placeholder: "종목명/섹터/업종"
  })
  
  E_MOUSE.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
})