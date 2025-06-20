/*--------------------------------------------------------------
# GLOBALS
--------------------------------------------------------------*/
const isLabTop = window.matchMedia('(max-width: 1443px)');
const isTablet = window.matchMedia('(max-width: 1023px)');
const isMobile = window.matchMedia('(max-width: 767px)');
const isNarrow = window.matchMedia('(max-width: 374px)');
const fontFamily = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

var Layout = {
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
		tickangle: 0,
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
	autosize: true,
	hoverlabel: {
		font: {
			family: fontFamily,
			color: '#fffff'
		}
	},
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
	var maxRange = 0;
	var minRange = 0;
	var layout = JSON.parse(JSON.stringify(Layout));
	var data = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		texttemplate:'%{y:.2f}%',
		textposition:'outside',
		hovertemplate: '%{meta}<extra></extra>',
		marker:{
			color:[]
		}
	};
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data.x.push(obj.name);
		data.y.push(obj['yield']);
		data.meta.push(obj.meta1);
		data.marker.color.push(obj.yieldColor);
		maxRange = obj['yield'] > maxRange ? obj['yield'] : maxRange;
		minRange = obj['yield'] < minRange ? obj['yield'] : minRange;
	});
	var space = 0.1 * (maxRange - minRange);
	maxRange = maxRange + space;
	if (minRange < 0) {
		minRange  = minRange - space;
	} 
	layout.yaxis.range = [minRange, maxRange];
    Plotly.newPlot('plotly-yield', [data], layout, Option);
}

function setPrice() {
	var maxRange = 0;
	var minRange = 0;
	var layout = JSON.parse(JSON.stringify(Layout));
	var data1 = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		hovertemplate: '매수가: %{y:,d}원<extra></extra>',
		marker:{
			color:[]
		}
	};
	
	var data2 = JSON.parse(JSON.stringify(data1));
	data2.hovertemplate = '현재가: %{y:,d}원<extra></extra>'
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data1.x.push(obj.name);
		data1.y.push(obj.startBuy);
		data1.marker.color.push('grey');
		maxRange = obj.startBuy > maxRange ? obj.startBuy : maxRange;
	});
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data2.x.push(obj.name);
		data2.y.push(obj.close);
		data2.marker.color.push(obj.startBuy > obj.close ? 'blue' : 'red');
		maxRange = obj.close > maxRange ? obj.close : maxRange;
	});
	layout.yaxis.range = [0, 1.1 * maxRange];
    Plotly.newPlot('plotly-price', [data1, data2], layout, Option);
}

function setProfit() {
	var maxRange = 0;
	var minRange = 0;
	var layout = JSON.parse(JSON.stringify(Layout));
	var data = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		hovertemplate: '%{meta}<extra></extra>',
		marker:{
			color:[]
		}
	};
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data.x.push(obj.name);
		data.y.push(obj.trailingProfitRate);
		data.meta.push(obj.meta2);
		data.marker.color.push(obj.profitColor);
		maxRange = obj.trailingProfitRate > maxRange ? obj.trailingProfitRate : maxRange;
		minRange = obj.trailingProfitRate < minRange ? obj.trailingProfitRate : minRange;
	});
	console.log(minRange);
	layout.yaxis.range = [1.1 * minRange, 1.1 * maxRange];
	
    Plotly.newPlot('plotly-profit', [data], layout, Option);
}

function setPe() {
	var maxRange = 0;
	var minRange = 0;
	var layout = JSON.parse(JSON.stringify(Layout));
	var data1 = {
		type:'bar',
		x:[],
		y:[],
		meta:[],
		hovertemplate: '4분기연속PE: %{y:.2f}<extra></extra>',
		marker:{
			color:[]
		}
	};
	
	var data2 = JSON.parse(JSON.stringify(data1));
	data2.hovertemplate = '12개월ForwardPE: %{y:.2f}<extra></extra>',
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data1.x.push(obj.name);
		data1.y.push(obj.trailingPE);
		data1.marker.color.push(obj.peColor);
		maxRange = obj.trailingPE > maxRange ? obj.trailingPE : maxRange;
	});
	
	Object.entries(srcTickers).forEach(([ticker, obj]) => {		
		data2.x.push(obj.name);
		data2.y.push(obj.estimatedPE);
		data2.marker.color.push(obj.epeColor);
		maxRange = obj.estimatedPE > maxRange ? obj.estimatedPE : maxRange;
	});
	layout.yaxis.range = [0, 1.1 * maxRange];
    Plotly.newPlot('plotly-pe', [data1, data2], layout, Option);
}



$(document).ready(function(){

	setYield();
	setPrice();
	setProfit();
	setPe();
})

