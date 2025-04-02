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
const srcTickers = {"251970":{"startDate":"2025-03-28","today":"2025-04-02","timeDiff":"5 days","buyPrice":49200,"currentPrice":54000,"yield":9.76,"yieldColor":"#F04141","pct52wHigh":0.0,"pct52wLow":137.89,"trailingProfitRate":14.34,"trailingPE":20.48,"estimatedPE":16.98,"name":"\ud38c\ud14d\ucf54\ub9ac\uc544*","marketCap":"6634\uc5b5","sectorName":"\uc18c\uc7ac","industryName":"\ube44\ucca0\uae08\uc18d"},"053580":{"startDate":"2025-04-02","today":"2025-04-02","timeDiff":"0 days","buyPrice":11000,"currentPrice":11090,"yield":0.82,"yieldColor":"#B4A0A0","pct52wHigh":-1.86,"pct52wLow":76.03,"trailingProfitRate":18.69,"trailingPE":18.15,"estimatedPE":null,"name":"\uc6f9\ucf00\uc2dc*","marketCap":"1519\uc5b5","sectorName":"IT","industryName":"IT\uc11c\ube44\uc2a4"},"102710":{"startDate":"2025-04-02","today":"2025-04-02","timeDiff":"0 days","buyPrice":26000,"currentPrice":26050,"yield":0.19,"yieldColor":"#A9A4A4","pct52wHigh":-21.3,"pct52wLow":80.03,"trailingProfitRate":10.19,"trailingPE":11.97,"estimatedPE":null,"name":"\uc774\uc5d4\uc5d0\ud504\ud14c\ud06c\ub180\ub85c\uc9c0*","marketCap":"3743\uc5b5","sectorName":"IT","industryName":"\ubc18\ub3c4\uccb4"}};


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
