// const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
const __URL__ = '../../../src/json/treemap/treemap.json';
const abs = (array) => {
    return array.map(Math.abs);
}

let __SRC__ = null;

var base = null;
var data = null;
var spec = null;


function updateBar() {
    let sorted = {};
    let indices = base[spec].map((value, index) => index);
    var unit = '%';
    var layout = {
        margin:{
            l:115, 
            r:10, 
            t:10, 
            b:22
        }, 
        autorange:false,
        xaxis:{
            range:[0, 0], 
            linecolor:'black', 
            linewidth:1
        },
        yaxis:{
            linecolor:'black', 
            linewidth:1, 
            tickson:'boundaries', 
            ticklen:8
        }
    }
    var option = {
        displayModeBar:false, 
        responsive:true, 
        showTips:false, 
        staticPlot:true
    }

    if ((spec == 'PER') || (spec == 'PBR')) {
        unit = '';
    }

    indices.sort((i, j) => base[spec][i] - base[spec][j]);
    for (var key in base) {
        sorted[key] = indices.map(index => base[key][index]);
    }
    layout.xaxis.range = [0, 1.15 * sorted[spec][sorted[spec].length - 1]];

    data = [{
        type: 'bar',
        x: abs(sorted[spec]),
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
  var size = __SRC__.LargeCap.name.length;
  $('.trading-date').html(
    __SRC__.LargeCap.name[size - 1].replace('대형주(', '* ').replace(')', '')
  );
  updateBar();
})


$(document).ready(function() {
  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }
})