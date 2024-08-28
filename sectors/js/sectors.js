const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
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
            // linecolor:'black', 
            // linewidth:1, 
            // tickson:'boundaries', 
            // ticklen:8
        },

    }
    var option = {
        scrollZoom: false,
        displayModeBar:false, 
        responsive:true, 
        showTips:false, 
        // modeBarButtonsToRemove: ['zoom2d', 'pan2d', 'select2d', 'lasso2d'], // 기본 확대/축소 도구 제거
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
    }]
    Plotly.newPlot('sector-bar', data, layout, option);
}

$('.bar-type').on('change', function() {
    base = __SRC__[$('.bar-type').val()];
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

  base = __SRC__[$('.bar-type').val()];
  spec = $('.bar-option').val();
//   var size = __SRC__.LargeCap.name.length;
//   $('.trading-date').html(
//     __SRC__.LargeCap.name[size - 1].replace('대형주(', '* ').replace(')', '')
//   );
  updateBar();
})


$(document).ready(function() {
  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }
})