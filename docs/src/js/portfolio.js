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
const srcTickers = {"016590":{"startDate":"2025-04-09","startBuy":7170,"date":"2025\/05\/02","close":8410,"marketCap":"3389\uc5b5","volume":54622,"amount":451553535,"PBR":0.43,"dividendYield":2.38,"foreignRate":2.86,"D-1":-1.52,"W-1":7.13,"M-1":19.97,"M-3":45.5,"M-6":42.54,"Y-1":39.7,"beta":0.4038,"floatShares":16.25,"trailingRevenue":6585.03,"trailingEps":871,"trailingProfitRate":4.45,"averageRevenueGrowth_A":2.14,"averageProfitGrowth_A":-14.3,"averageEpsGrowth_A":-2.63,"RevenueGrowth_A":2.04,"RevenueGrowth_Q":3.05,"ProfitGrowth_A":-49.95,"ProfitGrowth_Q":212.65,"EpsGrowth_A":-26.6,"EpsGrowth_Q":-841.18,"fiscalDividendYield":3.49,"fiscalDebtRatio":26.56,"pct52wHigh":-1.52,"pct52wLow":71.11,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.51,"trailingPE":9.66,"turnoverRatio":0.13,"market":"kospi","name":"\uc2e0\ub300\uc591\uc81c\uc9c0","industryCode":"WI200","industryName":"\ube44\ucca0\uae08\uc18d","sectorCode":"G15","sectorName":"\uc18c\uc7ac","stockSize":null,"timeDiff":"23 days","yield":17.29,"yieldColor":"#DD3434","profitColor":"#36704E","peColor":"#2FAF53","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/09(23\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 17.29%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 4.45%<br>\uc139\ud130: \uc18c\uc7ac<br>\uc5c5\uc885: \ube44\ucca0\uae08\uc18d<br>\uc2dc\uac00\ucd1d\uc561: 3389\uc5b5\uc6d0<br>"},"183300":{"startDate":"2025-04-21","startBuy":62000,"date":"2025\/05\/02","close":59200,"marketCap":"6171\uc5b5","volume":82977,"amount":4916485650,"PBR":2.24,"dividendYield":1.69,"foreignRate":19.28,"D-1":0.85,"W-1":-5.73,"M-1":3.5,"M-3":56.2,"M-6":21.81,"Y-1":-37.35,"beta":1.042,"floatShares":53.71,"trailingRevenue":5071.38,"trailingEps":5341,"trailingProfitRate":22.18,"averageRevenueGrowth_A":27.95,"averageProfitGrowth_A":64.91,"averageEpsGrowth_A":30.34,"RevenueGrowth_A":65.05,"RevenueGrowth_Q":0.13,"ProfitGrowth_A":240.51,"ProfitGrowth_Q":-35.05,"EpsGrowth_A":73.94,"EpsGrowth_Q":104.3,"fiscalDividendYield":2.73,"fiscalDebtRatio":113.02,"pct52wHigh":-38.97,"pct52wLow":81.32,"pctEstimated":-32.34,"estimatedPE":9.38,"trailingPS":1.22,"trailingPE":11.08,"turnoverRatio":0.8,"market":"kosdaq","name":"\ucf54\ubbf8\ucf54*","industryCode":"WI620","industryName":"\ubc18\ub3c4\uccb4","sectorCode":"G45","sectorName":"IT","stockSize":"large","timeDiff":"11 days","yield":-4.52,"yieldColor":"#85B6DD","profitColor":"#30CC5A","peColor":"#2FA550","epeColor":"#2FB253","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/21(11\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: -4.52%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 22.18%<br>\uc139\ud130: IT<br>\uc5c5\uc885: \ubc18\ub3c4\uccb4<br>\uc2dc\uac00\ucd1d\uc561: 6171\uc5b5\uc6d0<br>"}};


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
