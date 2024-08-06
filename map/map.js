const __URL__ = 'https://raw.githubusercontent.com/labwons/pages/main/app/barmap/archive/marketmap.json';


let __SRC__ = null;


var data = null;
var spec = null;

// var c_media = window.matchMedia('(max-width: 1023px)');
// var tdat_name = []; var tdat_scale = []; var tdat_caps = []; var tdat_price = []; var tdat_perf = []; var tdat_color = [];
// var map_type; var market_type; var option_type; var map_key;

// var map_layout = {
//     height: 690,
//     margin:{l:0,r:0,t:2,b:25}
// };
// var map_option = {
//     displayModeBar:false,
//     responsive:true,
//     showTips:false
// };

// function setSearch(key){
// 	$('.map-search').empty();
// 	$('.map-search').append('<option></option>');
// 	for (var n = 0; n < tdat_ids[key].length; n++){
// 		$('.map-search').append('<option>' + tdat_ids[key][n] + '</option>');
// 	}
// }

// function search_top(__group__){
//   var elems = $('.slicetext');
// 	var clicker = null;
// 	var name = '';
// 	for (var n = 0; n < elems.length; n++){
// 		name = $(elems[n]).text();
// 		if (name == __group__){
// 			clicker = $(elems[n]).parent().get(0);
// 			break;
// 		}
// 	}
// 	if (clicker == null) {return;}
// 	if (document.createEvent) {
// 			var event = document.createEvent('MouseEvents');
// 			event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
// 			!clicker.dispatchEvent(event);
// 	} else if (link.fireEvent) {
// 		!clicker.fireEvent('onclick');
// 	}
// }

// function search_asset(__asset_name){
// 	var elems = $('.slicetext');
// 	var clicker = null;
// 	for (var n = 0; n < elems.length; n++){
// 		var name = $(elems[n]).text();
//     if ((name.includes(__asset_name)) && (name.slice(0, __asset_name.length) == __asset_name)){
//       var leftover = name.slice(__asset_name.length, name.length)
//       var tail_cnt = 0;
//       var digits = leftover.match(/\d/g);
//       if (digits != null){
//   			tail_cnt += digits.length;
//   		}
//       if (leftover.includes('-')){ tail_cnt += 1 }
//       if (leftover.includes('.')){ tail_cnt += 1 }
//       if (leftover.includes('%')){ tail_cnt += 1 }
//       if ((leftover.length - tail_cnt) == 0){
//         clicker = $(elems[n]).parent().get(0);
//   		  break;
//       }
//     }
// 	}
// 	if (clicker == null){
// 		return
// 	}
// 	if (document.createEvent) {
// 			var event = document.createEvent('MouseEvents');
// 			event.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
// 			!clicker.dispatchEvent(event);
// 	} else if (link.fireEvent) {
// 		!clicker.fireEvent('onclick');
// 	}
// }

// function treemap(key){
//   var _t, _u, _treemap;
//   tdat_name = []; tdat_scale = []; tdat_caps = []; tdat_price = []; tdat_perf = []; tdat_color = [];

//   tdat_labels[key].forEach(function(code){
// 	  tdat_name.push(tdat_frm[code]['종목명']);
// 	  tdat_scale.push(tdat_frm[code]['크기']);
// 	  tdat_caps.push(tdat_frm[code]['시가총액']);
// 	  tdat_price.push(tdat_frm[code]['종가']);
// 	  tdat_perf.push(tdat_frm[code][option_type]);
// 	  tdat_color.push(tdat_frm[code]['C' + option_type]);
//   });
//   _t = (option_type == 'PER' || option_type == 'PBR') ? option_type : '수익률';
//   _u = (option_type == 'PER' || option_type == 'PBR') ? '' : '%';

//   _treemap={
//     type:'treemap',
//     branchvalues:'total',
//     labels:tdat_name,
//     parents:tdat_covers[key],
//     values:tdat_scale,
//     ids:tdat_name,
//     meta:tdat_caps,
//     customdata:tdat_price,
//     text:tdat_perf,
// 	  textposition:'middle center',
//     textfont:{
//       family:'NanumGothic, Nanum Gothic, monospace',
//       color:'#ffffff'
//     },
//     texttemplate: '%{label}<br>%{text}' + _u,
//     hovertemplate: '%{label}<br>시총: %{meta}<br>종가: %{customdata}<br>' + _t + ': %{text}' + _u + '<extra></extra>',
//     hoverlabel: {
//       font: {
//         family: 'NanumGothic, Nanum Gothic, monospace',
//         color: '#ffffff'
//       }
//     },
//     opacity: 0.9,
//     marker: {
//       colors: tdat_color,
//       visible: true
//     },
//     pathbar: {'visible': true}
//   }
//   Plotly.newPlot('myMap', [_treemap], map_layout, map_option);
// }

function update_map() {
  unit = (spec == 'PER' || spec == 'PBR') ? '' : '%';
  kwargs = {
    type:'treemap',
    branchvalues:'total',
    labels:data.name,
    parents:data.cover,
    values:data.size,
    meta:data.meta,
    text:data[spec],
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
      colors: data[spec + '-C'],
      visible: true
    },
    root_color:'lightgrey'
  }
  // Plotly.newPlot('myMap', [_treemap], map_layout, map_option);
  Plotly.newPlot(
    'market-map', 
    [kwargs],
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

  data = __SRC__[$('.map-type').val()];
  spec = $('.map-option').val();
  update_map();
})


$(document).ready(function() {
  
  $('.map-type').on('change', function() {
    data = __SRC__[$('.map-type').val()];
    update_map();
  })

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
    update_map();
  })

})

//   // MAP type selection
//   $('.map-select').on('change', function(){
//       $('.option-select option[value="PER"]').remove();
//       $('.option-select option[value="PBR"]').remove();
//       $('.option-select option[value="DIV"]').remove();
//       map_type = $('.map-select').val()

//       if (map_type != 'etfful'){
//       $('.option-select').append('<option value="PER">PER</option>');
//       $('.option-select').append('<option value="PBR">PBR</option>');
//       $('.option-select').append('<option value="DIV">배당수익률</option>');
//       }

//       map_key = map_type;
//       treemap(map_key);
//       setSearch(map_key);
//   })

//   // Option selection
//   $(".option-select").on('change', function(){
//       option_type = $(".option-select").val();
//       treemap(map_key);
//   if ((option_type == 'PER') || (option_type == 'PBR')){
//       $("#s_red").html('고평가');
//       $("#navy").html('평균');
//       $("#s_grn").html('저평가');
//   } else if (option_type == 'DIV'){
//       $("#s_red").html('저배당');
//       $("#navy").html('평균');
//       $("#s_grn").html('고배당');
//   } else {
//       $("#s_red").html('하락');
//       $("#navy").html('보합');
//       $("#s_grn").html('상승');
//   }
//   })

//   // MAP Search
//   $('.map-search').on('select2:select', function (e) {
//       var username = e.params.data.text;
//       if (username == "") { return }

//       var i_start = username.indexOf('[');
//       if (i_start != -1){
//       var group = username.slice(i_start + 1, username.length - 1);
//       username = username.slice(0, i_start);
//       } else if (group_data.includes(username)) {
//       var group = username;
//       } else{
//       var idx = tdat_name.indexOf(username);
//       var group = tdat_covers[map_key][idx];
//       }

//       search_top(group);
//       if (username == group){return}
//       setTimeout(function(){
//       search_asset(username);
//       }, 1000)
//   });

//   // MAP Reset
//   $('#map-reset').click(function(){
//       treemap(map_key);
//   })