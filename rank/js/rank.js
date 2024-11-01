const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');


let SRC = null;
var secOpt = 'ALL';
var comOpt = 'D-1';


function setTypeSelector() {
  $('bar-type').empty();
  Object.keys(SRC.Data).forEach(key => {
    $('.bar-type').append('<option value="' + key + '">' + SRC.Data[key]['label'] + '</option>');
  })
  secOpt = $('.bar-type').val();
}

function setOptionSelector() {
  $('.bar-option').empty();
  Object.entries(SRC.Meta).forEach(([key, val]) => {
    $('.bar-option').append('<option value="' + key + '">' + val['label'] + '</option>');
  })
  comOpt = $('.bar-option').val();
}

function setScale() {
  var tag = SRC.Meta[comOpt];
  $('.bar-legend span').each(function(n){
    if(tag.bound[n] == null){
      $(this).html('&nbsp; - &nbsp;');
    } else {
      $(this).html(String(tag.bound[n]) + tag.unit);
    }
    $(this).css('background-color', tag.scale[n]);
  })
}

function setLayout() {
  return {
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
    },
    yaxis:{
      showline: false,
      zeroline: false,
      showticklabels: false
    },
    barmode: 'relative',
    dragmode: false
  }
}

function setOption() {
  return {
    scrollZoom: false,
    displayModeBar:false, 
    responsive:true, 
    showTips:false, 
  }
}

function setRankDesktop() {
  var tag = SRC.Meta[comOpt];
  var data = SRC.Data[secOpt][comOpt];
  var font = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';
  var layout = setLayout();
  var option = setOption();
  var upperMax = Math.max(...data.upper.x);
  var lowerMin = Math.min(...data.lower.x);

  layout.xaxis.range = [1.1 * lowerMin, 1.1 * upperMax];
  Plotly.newPlot(
    'stock-rank', 
    [{
      type: 'bar',
      orientation: 'h',
      x: data.lower.x,
      y: data.lower.y,
      showlegend: false,
      text: data.lower.text,
      texttemplate: '%{text}' + tag.unit,
      textposition: 'outside',
      marker:{
        color: data.lower.color,
        opacity: 0.9
      },
      meta: data.lower.meta,
      hovertemplate:'%{meta}<extra></extra>',
    }, {
      type: 'scatter',
      orientation: 'h',
      x: data.lower.x,
      y: data.lower.y,
      showlegend: false,
      mode: 'text',
      text: data.lower.name.map(item => '&nbsp; ' + item),
      texttemplate: '%{text}',
      textposition: 'middle right',
      textfont: {
        family: font,
        color: 'white'
      },
      hoverinfo: 'skip'
    }, {
      type: 'bar',
      orientation: 'h',
      x: data.upper.x,
      y: data.upper.y,
      showlegend: false,
      text: data.upper.text,
      texttemplate: '%{text}' + tag.unit,
      textposition: 'outside',
      marker:{
        color: data.upper.color,
        opacity: 0.9
      },
      meta: data.upper.meta,
      hovertemplate:'%{meta}<extra></extra>',
    }, {
      type: 'scatter',
      orientation: 'h',
      x: data.upper.x,
      y: data.upper.y,
      showlegend: false,
      mode: 'text',
      text: data.upper.name.map(item => item + '&nbsp; '),
      texttemplate: '%{text}',
      textposition: 'middle left',
      textfont: {
        family: font,
        color: 'white'
      },
      hoverinfo: 'skip'
    }], 
    layout, 
    option
  )

  // indices.sort((i, j) => base[spec][i] - base[spec][j]);
  // for (var key in base) {
  //   sorted[key] = indices.map(index => base[key][index]);
  // }
  // if (isNarrow.matches) {
  //   maxRange = 1.35 * Math.max(...abs(sorted[spec]));
  // } else if (isMobile.matches) {
  //   maxRange = 1.3 * Math.max(...abs(sorted[spec]));
  // } else if (isTablet.matches) {
  //   maxRange = 1.2 * Math.max(...abs(sorted[spec]));
  // } else {
  //   maxRange = 1.1 * Math.max(...abs(sorted[spec]));
  // }
  // minbar = 0.45 * maxRange;

  // layout.xaxis.range = [0, maxRange + minbar];
  // layout.annotations = sorted.name.map(function(y, i) {
  //   return {
  //     x: 0,
  //     y: y,
  //     xref: 'x',
  //     yref: 'y',
  //     text: y,
  //     showarrow: false,
  //     font: {
  //       color: 'white',
  //       size: 13,
  //     },
  //     xanchor: 'left',
  //     yanchor: 'middle',
  //   };
  // });

  // data = [{
  //   type: 'bar',
  //   x: abs(sorted[spec]).map(function(x) {return x += minbar;}),
  //   y: sorted.name,
  //   orientation:'h',
  //   marker:{
  //     color:sorted[spec + '-C']
  //   },
  //   text:sorted[spec],
  //   texttemplate:'%{text}' + unit,
  //   textposition:'outside',
  //   meta:sorted.meta,
  //   hovertemplate:'%{meta}<br>' + spec + ': %{text}' + unit + '<extra></extra>',
  //   opacity:0.9
  // }];
  // Plotly.newPlot('stock-rank', data, layout, option);
}


$(document).ready(async function(){
  try {
    const response = await fetch('../../dev/json/service/rank.json');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    SRC = await response.json();
  } catch (error) {
      console.error('Fetch error:', error);
  }
  setTypeSelector();
  setOptionSelector();
  setRankDesktop();
  setScale();
})


$(document).ready(function() {

  $('.bar-type').on('change', function() {
    secOpt = $(this).val();
    setRankDesktop();
  })

  $('.bar-option').on('change', function() {    
    comOpt = $(this).val();
    setScale();
    setRankDesktop();
  })
})