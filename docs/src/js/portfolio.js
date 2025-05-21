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
const srcTickers = {"016590":{"startDate":"2025-04-09","startBuy":7170,"date":"2025\/05\/21","close":8870,"marketCap":"3554\uc5b5","volume":54930,"amount":484083845,"PBR":0.45,"dividendYield":2.25,"foreignRate":2.79,"D-1":2.31,"W-1":6.87,"M-1":15.95,"M-3":48.33,"M-6":53.46,"Y-1":43.3,"beta":0.4269,"floatShares":16.25,"trailingRevenue":6585.03,"trailingEps":871,"trailingProfitRate":4.45,"averageRevenueGrowth_A":2.14,"averageProfitGrowth_A":-14.3,"averageEpsGrowth_A":-2.63,"RevenueGrowth_A":2.04,"RevenueGrowth_Q":3.05,"ProfitGrowth_A":-49.95,"ProfitGrowth_Q":212.65,"EpsGrowth_A":-26.6,"EpsGrowth_Q":-841.18,"fiscalDividendYield":3.49,"fiscalDebtRatio":26.56,"pct52wHigh":0.0,"pct52wLow":80.47,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.54,"trailingPE":10.18,"turnoverRatio":0.14,"market":"kospi","name":"\uc2e0\ub300\uc591\uc81c\uc9c0","industryCode":"WI200","industryName":"\ube44\ucca0\uae08\uc18d","sectorCode":"G15","sectorName":"\uc18c\uc7ac","stockSize":null,"timeDiff":"42 days","yield":23.71,"yieldColor":"#C92A2A","profitColor":"#36704E","peColor":"#2FAB52","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/09(42\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 23.71%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 4.45%<br>\uc139\ud130: \uc18c\uc7ac<br>\uc5c5\uc885: \ube44\ucca0\uae08\uc18d<br>\uc2dc\uac00\ucd1d\uc561: 3554\uc5b5\uc6d0<br>"},"183300":{"startDate":"2025-04-21","startBuy":62000,"date":"2025\/05\/21","close":55800,"marketCap":"5837\uc5b5","volume":78332,"amount":4356728550,"PBR":2.12,"dividendYield":1.79,"foreignRate":20.03,"D-1":0.18,"W-1":-10.43,"M-1":-8.97,"M-3":15.53,"M-6":41.27,"Y-1":-39.81,"beta":1.0594,"floatShares":53.71,"trailingRevenue":5071.38,"trailingEps":5341,"trailingProfitRate":22.18,"averageRevenueGrowth_A":27.95,"averageProfitGrowth_A":64.91,"averageEpsGrowth_A":30.34,"RevenueGrowth_A":65.05,"RevenueGrowth_Q":0.13,"ProfitGrowth_A":240.51,"ProfitGrowth_Q":-35.05,"EpsGrowth_A":73.94,"EpsGrowth_Q":104.3,"fiscalDividendYield":2.73,"fiscalDebtRatio":113.02,"pct52wHigh":-41.63,"pct52wLow":70.9,"pctEstimated":-36.23,"estimatedPE":8.84,"trailingPS":1.15,"trailingPE":10.45,"turnoverRatio":0.75,"market":"kosdaq","name":"\ucf54\ubbf8\ucf54*","industryCode":"WI620","industryName":"\ubc18\ub3c4\uccb4","sectorCode":"G45","sectorName":"IT","stockSize":"large","timeDiff":"30 days","yield":-10.0,"yieldColor":"#50A9F2","profitColor":"#30CC5A","peColor":"#2FA951","epeColor":"#2FB654","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/21(30\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: -10.0%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 22.18%<br>\uc139\ud130: IT<br>\uc5c5\uc885: \ubc18\ub3c4\uccb4<br>\uc2dc\uac00\ucd1d\uc561: 5837\uc5b5\uc6d0<br>"}};


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
