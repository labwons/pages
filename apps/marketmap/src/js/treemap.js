const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/src/json/treemap/treemap.json';
// const __URL__ = '../../../../src/json/treemap/treemap.json';


let __SRC__ = null;

var base = null;
var data = null;
var spec = null;
var tops = null;


function setTops(){
  tops = [];
  for (var n = base.meta.length - 2; n > 0; n--) {
    tops.push(base.name[n]);
    if (base.meta[n].includes('종가')) { return tops; }
  }
  return [];
}

function searchReset(){
	$('.map-keyin').empty();
	$('.map-keyin').append('<option></option>');
	for (var n = 0; n < base.name.length; n++){
		$('.map-keyin').append('<option>' + base.name[n] + '</option>');
	}
}

// function searchObj(name) {
//   var objs = $('.slicetext');
//   for (var n = 0; n < objs.length; n++) {
//     if ($(objs[n]).text().includes(name)) {
//       return objs[n];
//     }
//   }
// }

function searchTop(top){
  var elems = $('.slicetext');
	var clicker = null;
	var name = '';
	for (var n = 0; n < elems.length; n++){
		name = $(elems[n]).text();
		if (name == top){
			clicker = $(elems[n]).parent().get(0);
			break;
		}
	}
	if (clicker == null) {return;}
	if (document.createEvent) {
			var event = document.createEvent('MouseEvents');
			event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
			!clicker.dispatchEvent(event);
	} else if (link.fireEvent) {
		!clicker.fireEvent('onclick');
	}
}

function searchAsset(asset){
	var elems = $('.slicetext');
	var clicker = null;
	for (var n = 0; n < elems.length; n++){
		var name = $(elems[n]).text();
    if ((name.includes(asset)) && (name.slice(0, asset.length) == asset)){
      var leftover = name.slice(asset.length, name.length)
      var tail_cnt = 0;
      var digits = leftover.match(/\d/g);
      if (digits != null){
  			tail_cnt += digits.length;
  		}
      if (leftover.includes('-')){ tail_cnt += 1 }
      if (leftover.includes('.')){ tail_cnt += 1 }
      if (leftover.includes('%')){ tail_cnt += 1 }
      if ((leftover.length - tail_cnt) == 0){
        clicker = $(elems[n]).parent().get(0);
  		  break;
      }
    }
	}
	if (clicker == null){
		return
	}
  console.log(clicker);
  $(clicker).css("border", "3px solid white");
	// if (document.createEvent) {
	// 		var event = document.createEvent('MouseEvents');
	// 		event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
	// 		!clicker.dispatchEvent(event);
	// } else if (link.fireEvent) {
	// 	!clicker.fireEvent('onclick');
	// }
}

function update_map() {
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
      family:'NanumGothic, Nanum Gothic, monospace',
      color:'#ffffff'
    },
    texttemplate: '%{label}<br>%{text:.2f}' + unit,
    hovertemplate: '%{meta}<br>' + spec + ': %{text}' + unit + '<extra></extra>',
    hoverlabel: {
      font: {
        family: 'NanumGothic, Nanum Gothic, monospace',
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
      height: 650,
      margin:{l:0,r:0,t:0,b:25}
    },
    {
      displayModeBar:false,
      responsive:true,
      showTips:false
    }
  );
}


$('.map-option').on('change', function() {
  spec = $('.map-option').val();
  if ((spec == 'PER') || (spec == 'PBR')) {
    $('.maps-lowest').html('고평가');
    $('.maps-lower').html('');
    $('.maps-low').html('');
    $('.maps-middle').html('평균');
    $('.maps-high').html('');
    $('.maps-higher').html('');
    $('.maps-highest').html('저평가');
  } else if (spec == 'DIV') {
    $('.maps-lowest').html('');
    $('.maps-lower').html('');
    $('.maps-low').html('');
    $('.maps-middle').html('0%');
    $('.maps-high').html('2%');
    $('.maps-higher').html('4%');
    $('.maps-highest').html('6%');
  } else if (spec == 'D-1') {
    $('.maps-lowest').html('-3%');
    $('.maps-lower').html('-2%');
    $('.maps-low').html('-1%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('1%');
    $('.maps-higher').html('2%');
    $('.maps-highest').html('3%');
  } else if (spec == 'W-1') {
    $('.maps-lowest').html('-6%');
    $('.maps-lower').html('-4%');
    $('.maps-low').html('-2%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('2%');
    $('.maps-higher').html('4%');
    $('.maps-highest').html('6%');
  } else if (spec == 'M-1') {
    $('.maps-lowest').html('-10%');
    $('.maps-lower').html('-6.7%');
    $('.maps-low').html('-3.3%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('3.3%');
    $('.maps-higher').html('6.7%');
    $('.maps-highest').html('10%');
  } else if (spec == 'M-3') {
    $('.maps-lowest').html('-18%');
    $('.maps-lower').html('-12%');
    $('.maps-low').html('-6%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('6%');
    $('.maps-higher').html('12%');
    $('.maps-highest').html('18%');
  } else if (spec == 'M-6') {
    $('.maps-lowest').html('-24%');
    $('.maps-lower').html('-16%');
    $('.maps-low').html('-8%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('8%');
    $('.maps-higher').html('16%');
    $('.maps-highest').html('24%');
  } else if (spec == 'Y-1') {
    $('.maps-lowest').html('-30%');
    $('.maps-lower').html('-20%');
    $('.maps-low').html('-10%');
    $('.maps-middle').html('0%');
    $('.maps-high').html('10%');
    $('.maps-higher').html('20%');
    $('.maps-highest').html('30%');
  }
  update_map(__ID__);
})

$('.map-keyin').on('select2:select', function (e) {
    var _select = e.params.data.text;
    if (_select == "") { return }

    if (tops.includes(_select)) {
      var group = _select;
    } else{
      var group = base.cover[base.name.indexOf(_select)];
    }
    searchTop(group);

    if (_select == group){ return }
    searchAsset(_select);
    // setTimeout(function(){
    //   searchAsset(username);
    //   $('.map-rewind').toggleClass('show');
    // }, 1000)
});

$('.map-reset').click(function(){
    update_map();
})

$('.map-rewind').click(function(){
  $(this).toggleClass('show');
})

// $('#market-map').on('plotly_click', function(e, d){
//   console.log(d);
// })

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
  tops = setTops();
  update_map();
  searchReset();
})


$(document).ready(function() {

  if ($('#header').attr("class").includes("header-fix")) {
    $('#header').removeClass('header-fix');
  }
  $('.map-keyin').select2({
    placeholder: "Testing"
  })
})

$('.map-type').on('change', function() {
  base = __SRC__[$('.map-type').val()];
  tops = setTops();
  update_map(__ID__);
  searchReset();
})