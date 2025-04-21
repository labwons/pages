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
const srcTickers = {"016590":{"startDate":"2025-04-09","startBuy":7170,"date":"2025-04-21","close":7650,"marketCap":"3074\uc5b5","volume":11558,"amount":88002540,"PBR":0.44,"dividendYield":1.96,"foreignRate":2.86,"D-1":0.0,"W-1":5.08,"M-1":11.68,"M-3":32.81,"M-6":33.04,"Y-1":34.92,"beta":0.3936,"floatShares":16.25,"trailingRevenue":6585.03,"trailingEps":871,"trailingProfitRate":4.45,"averageRevenueGrowth_A":2.14,"averageProfitGrowth_A":-14.3,"averageEpsGrowth_A":-2.63,"RevenueGrowth_A":2.04,"RevenueGrowth_Q":3.05,"ProfitGrowth_A":-49.95,"ProfitGrowth_Q":212.65,"EpsGrowth_A":-26.6,"EpsGrowth_Q":-841.18,"fiscalDividendYield":3.49,"fiscalDebtRatio":26.56,"pct52wHigh":-1.8,"pct52wLow":55.65,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.47,"trailingPE":8.78,"turnoverRatio":0.03,"market":"kospi","name":"\uc2e0\ub300\uc591\uc81c\uc9c0","industryCode":"WI200","industryName":"\ube44\ucca0\uae08\uc18d","sectorCode":"G15","sectorName":"\uc18c\uc7ac","stockSize":null,"timeDiff":"12 days","yield":6.69,"yieldColor":"#FB8888","profitColor":"#36704E","peColor":"#2FB654","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/09(12\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 6.69%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 4.45%<br>\uc139\ud130: \uc18c\uc7ac<br>\uc5c5\uc885: \ube44\ucca0\uae08\uc18d<br>\uc2dc\uac00\ucd1d\uc561: 3074\uc5b5\uc6d0<br>"},"052400":{"startDate":"2025-04-21","startBuy":35050,"date":"2025-04-21","close":35800,"marketCap":"5213\uc5b5","volume":815394,"amount":28852606900,"PBR":2.74,"dividendYield":1.4,"foreignRate":1.61,"D-1":5.45,"W-1":-16.65,"M-1":39.84,"M-3":58.76,"M-6":164.6,"Y-1":106.7,"beta":0.1034,"floatShares":59.35,"trailingRevenue":2363.08,"trailingEps":2028,"trailingProfitRate":14.14,"averageRevenueGrowth_A":16.43,"averageProfitGrowth_A":30.7,"averageEpsGrowth_A":33.5,"RevenueGrowth_A":-15.67,"RevenueGrowth_Q":8.04,"ProfitGrowth_A":-0.8,"ProfitGrowth_Q":-40.03,"EpsGrowth_A":4.32,"EpsGrowth_Q":-8.0,"fiscalDividendYield":2.46,"fiscalDebtRatio":108.85,"pct52wHigh":-22.68,"pct52wLow":168.37,"pctEstimated":null,"estimatedPE":null,"trailingPS":2.21,"trailingPE":17.65,"turnoverRatio":5.53,"market":"kosdaq","name":"\ucf54\ub098\uc544\uc774*","industryCode":"WI602","industryName":"IT\uc11c\ube44\uc2a4","sectorCode":"G45","sectorName":"IT","stockSize":null,"timeDiff":"0 days","yield":2.14,"yieldColor":"#C19C9C","profitColor":"#2FC458","peColor":"#34784E","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/21(0\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 2.14%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 14.14%<br>\uc139\ud130: IT<br>\uc5c5\uc885: IT\uc11c\ube44\uc2a4<br>\uc2dc\uac00\ucd1d\uc561: 5213\uc5b5\uc6d0<br>"},"183300":{"startDate":"2025-04-21","startBuy":62000,"date":"2025-04-21","close":61300,"marketCap":"6433\uc5b5","volume":118559,"amount":7372776100,"PBR":3.03,"dividendYield":0.65,"foreignRate":19.95,"D-1":-1.13,"W-1":16.54,"M-1":7.17,"M-3":48.97,"M-6":18.34,"Y-1":-26.67,"beta":1.0634,"floatShares":53.71,"trailingRevenue":5071.38,"trailingEps":5341,"trailingProfitRate":22.18,"averageRevenueGrowth_A":27.95,"averageProfitGrowth_A":64.91,"averageEpsGrowth_A":30.34,"RevenueGrowth_A":65.05,"RevenueGrowth_Q":0.13,"ProfitGrowth_A":240.51,"ProfitGrowth_Q":-35.05,"EpsGrowth_A":73.94,"EpsGrowth_Q":104.3,"fiscalDividendYield":2.73,"fiscalDebtRatio":113.02,"pct52wHigh":-36.8,"pct52wLow":87.75,"pctEstimated":-27.88,"estimatedPE":10.51,"trailingPS":1.27,"trailingPE":11.48,"turnoverRatio":1.15,"market":"kosdaq","name":"\ucf54\ubbf8\ucf54*","industryCode":"WI620","industryName":"\ubc18\ub3c4\uccb4","sectorCode":"G45","sectorName":"IT","stockSize":"large","timeDiff":"0 days","yield":-1.13,"yieldColor":"#9DAAB3","profitColor":"#30CC5A","peColor":"#2FA14F","epeColor":"#2FA951","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/21(0\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: -1.13%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 22.18%<br>\uc139\ud130: IT<br>\uc5c5\uc885: \ubc18\ub3c4\uccb4<br>\uc2dc\uac00\ucd1d\uc561: 6433\uc5b5\uc6d0<br>"}};


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
