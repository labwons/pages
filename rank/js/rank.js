const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/rank/rank.json';
// const __URL__ = '../../../src/json/treemap/treemap.json';
const abs = (array) => {
    return array.map(Math.abs);
}
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');


let __SRC__ = null;

var base = null;
var data = null;
var spec = null;
// var leftMargin = 115;
var maxRange = 1.1;


function updateBar() {
  base = __SRC__[$('.bar-type').val() + '_' + $('.bar-option').val()];
  console.log(base);
  let sorted = {};
  let indices = base[spec].map((value, index) => index);
  var minbar = 0;
  var unit = '%';
  var layout = {
    margin:{
      l:10, 
      r:10, 
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
  layout.annotations.push({
    x: maxRange + minbar,
    y: sorted.name[parseInt(sorted.name.length / 2)],
    xref: 'x',
    yref: 'y',
    text: base.count,
    showarrow: false,
    font: {
      color: 'black',
      size: 14,
    },
    xanchor: 'right',
    yanchor: 'middle'
  })

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
  Plotly.newPlot('stock-rank', data, layout, option);
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
  $('.bar-type').append('<optgroup label="[섹터 / SECTOR]">');
  for (let sector of __SRC__.sectors){
    $('.bar-type').append('<option value="' + sector + '">' + sector + '</option>');
  }
  $('.bar-type').append('<optgroup label="[업종 / INDUSTRY]">');
  for (let industry of __SRC__.industries){
    $('.bar-type').append('<option value="' + industry + '">' + industry + '</option>');
  }
  spec = $('.bar-option').val();
  base = __SRC__[__SRC__.sectors[0] + '_' + spec];
  updateBar();
})


$(document).ready(function() {
  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }

  $('.bar-type').on('change', function() {
    updateBar();
  })

  $('.bar-option').on('change', function() {    
    spec = $('.bar-option').val();
    updateBar();

    if ((spec == 'PER') || (spec == 'PBR')) {
      $('.bar-lowest').html('고평가');
      $('.bar-lower').html('');
      $('.bar-low').html('');
      $('.bar-middle').html('평균');
      $('.bar-high').html('');
      $('.bar-higher').html('');
      $('.bar-highest').html('저평가');
    } else if (spec == 'DIV') {
      $('.bar-lowest').html('');
      $('.bar-lower').html('');
      $('.bar-low').html('');
      $('.bar-middle').html('0%');
      $('.bar-high').html('2%');
      $('.bar-higher').html('4%');
      $('.bar-highest').html('6%');
    } else if (spec == 'D-1') {
      $('.bar-lowest').html('-3%');
      $('.bar-lower').html('-2%');
      $('.bar-low').html('-1%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('1%');
      $('.bar-higher').html('2%');
      $('.bar-highest').html('3%');
    } else if (spec == 'W-1') {
      $('.bar-lowest').html('-6%');
      $('.bar-lower').html('-4%');
      $('.bar-low').html('-2%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('2%');
      $('.bar-higher').html('4%');
      $('.bar-highest').html('6%');
    } else if (spec == 'M-1') {
      $('.bar-lowest').html('-10%');
      $('.bar-lower').html('-6.7%');
      $('.bar-low').html('-3.3%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('3.3%');
      $('.bar-higher').html('6.7%');
      $('.bar-highest').html('10%');
    } else if (spec == 'M-3') {
      $('.bar-lowest').html('-18%');
      $('.bar-lower').html('-12%');
      $('.bar-low').html('-6%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('6%');
      $('.bar-higher').html('12%');
      $('.bar-highest').html('18%');
    } else if (spec == 'M-6') {
      $('.bar-lowest').html('-24%');
      $('.bar-lower').html('-16%');
      $('.bar-low').html('-8%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('8%');
      $('.bar-higher').html('16%');
      $('.bar-highest').html('24%');
    } else if (spec == 'Y-1') {
      $('.bar-lowest').html('-30%');
      $('.bar-lower').html('-20%');
      $('.bar-low').html('-10%');
      $('.bar-middle').html('0%');
      $('.bar-high').html('10%');
      $('.bar-higher').html('20%');
      $('.bar-highest').html('30%');
    }
  })
})