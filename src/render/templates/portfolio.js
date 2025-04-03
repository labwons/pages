/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const fontFamily = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

var TOOLBOX = false; // 0: NO TOOLBOX, 1: USE TOOLBOX
var VIEW_MODE = false; // 0: TREEMAP, 1: BAR
var SAMSUNG = true; // 0: WITHOUT SAMSUNG, 1: WITH SAMSUNG
var BARMODE = false; // 0: INDUSTRY, 1: SECTOR
var yieldLayout = {
	barmode:'group',
	showlegend: false,
	dragmode: false,
    margin:{
        l:20,
        r:0,
        t:0,
        b:20
    },
	xaxis:{
		showline:true,
		zerolinecolor:"lightgrey",
		gridcolor:"lightgrey",
    },
    yaxis:{
		ticklabelposition: 'inside',
		tickformat: 'd',
		showline:true,
		zerolinecolor:"lightgrey",
		gridcolor:"lightgrey",
    },
	autosize: true
};
var Option = {
    showTips:false,
    responsive:true,
    displayModeBar:false,
    displaylogo:false,
    modeBarButtonsToRemove: [
      // 'toImage','select2d','lasso2d','zoomOut2d','zoomIn2d','resetScale2d'
      'toImage','select2d','lasso2d','resetScale2d'
    ]    
};


/*--------------------------------------------------------------
# SOURCE DATA
--------------------------------------------------------------*/
const srcTickers = {{ srcTickers }};


/*--------------------------------------------------------------
# Functions
--------------------------------------------------------------*/
function setYield() {
	var data = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		texttemplate:'%{y}%',
		textposition:'outside',
		hovertemplate: '%{x}<br>%{y}%<extra></extra>',
		hoverlabel: {
			font: {
				family: fontFamily,
				color: '#fffff'
			}
		},
		marker:{
			color:[]
		}
	};
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data.x.push(obj.name);
		data.y.push(obj['yield']);
		data.marker.color.push(obj.yieldColor);
		
	});
  
    Plotly.newPlot('plotly-yield', [data], yieldLayout, Option);
}

function setPrice() {
	var data1 = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		hovertemplate: '%{y}원<br><extra></extra>',
		hoverlabel: {
			font: {
				family: fontFamily,
				color: '#fffff'
			}
		},
		marker:{
			color:[]
		}
	};
	
	var data2 = JSON.parse(JSON.stringify(data1));
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data1.x.push(obj.name);
		data1.y.push(obj.buyPrice);
		data1.marker.color.push('grey');
	});
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data2.x.push(obj.name);
		data2.y.push(obj.currentPrice);
		data2.marker.color.push('red');
	});
  
    Plotly.newPlot('plotly-price', [data1, data2], yieldLayout, Option);
}

function setOption(cssSelector, jsonObj, initKey){
    /*
    [USAGE]
    - setOption('.bubble-x', srcIndicatorOpt, 'D-1');
    - setOption('.bubble-y', srcIndicatorOpt, 'Y-1);
    */
    $(cssSelector).empty();
    Object.entries(jsonObj).forEach(([key, obj]) => {
        var label = (typeof obj === "object" && obj !== null) ? obj.label : obj;
		if (key == initKey) {
			$(cssSelector).append(`<option value="${key}" selected>${label}</option>`)
		} else {
			$(cssSelector).append(`<option value="${key}">${label}</option>`)
		}
    });
}

function setAxisLabel(cssSelector, axis){
	var selected = $(cssSelector).find('option:selected');
	selected.text(axis + ': ' + selected.text());
}

$(document).ready(function(){

	setYield();
	setPrice();
})

