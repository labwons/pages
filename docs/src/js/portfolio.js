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
		showline:true,
		zerolinecolor:"lightgrey",
		gridcolor:"lightgrey",
    },
};
var bubbleOption = {
    showTips:false,
    responsive:true,
    displayModeBar:true,
    displaylogo:false,
    modeBarButtonsToRemove: [
      // 'toImage','select2d','lasso2d','zoomOut2d','zoomIn2d','resetScale2d'
      'toImage','select2d','lasso2d','resetScale2d'
    ]    
};


/*--------------------------------------------------------------
# SOURCE DATA
--------------------------------------------------------------*/
const srcTickers = {"251970":{"startDate":"2025-03-28","today":"2025\/04\/03","timeDiff":"6 days","buyPrice":49200,"currentPrice":54200,"yield":10.16,"yieldColor":"#EE3D3D","pct52wHigh":0.0,"pct52wLow":138.77,"trailingProfitRate":14.34,"trailingPE":20.55,"estimatedPE":17.04,"name":"\ud38c\ud14d\ucf54\ub9ac\uc544*","marketCap":"6720\uc5b5","sectorName":"\uc18c\uc7ac","industryName":"\ube44\ucca0\uae08\uc18d"},"053580":{"startDate":"2025-04-02","today":"2025\/04\/03","timeDiff":"1 days","buyPrice":11000,"currentPrice":14080,"yield":28.0,"yieldColor":"#C92A2A","pct52wHigh":0.0,"pct52wLow":123.49,"trailingProfitRate":18.69,"trailingPE":23.04,"estimatedPE":null,"name":"\uc6f9\ucf00\uc2dc*","marketCap":"1914\uc5b5","sectorName":"IT","industryName":"IT\uc11c\ube44\uc2a4"},"102710":{"startDate":"2025-04-02","today":"2025\/04\/03","timeDiff":"1 days","buyPrice":26000,"currentPrice":26000,"yield":0.0,"yieldColor":"#A6A6A6","pct52wHigh":-21.45,"pct52wLow":79.68,"trailingProfitRate":10.19,"trailingPE":11.94,"estimatedPE":null,"name":"\uc774\uc5d4\uc5d0\ud504\ud14c\ud06c\ub180\ub85c\uc9c0*","marketCap":"3707\uc5b5","sectorName":"IT","industryName":"\ubc18\ub3c4\uccb4"}};


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
		hovertemplate: '%{x}<br><extra></extra>',
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
  
    Plotly.newPlot('portfolio-yield', [data], yieldLayout);
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
})
