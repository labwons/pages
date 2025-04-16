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
const srcTickers = {"102710":{"startDate":"2025-04-02","startBuy":26000,"date":"2025\/04\/16","close":26850,"marketCap":"3872\uc5b5","volume":65438,"amount":1774713525,"PBR":1.07,"dividendYield":0.19,"foreignRate":6.1,"D-1":-3.07,"W-1":9.59,"M-1":8.7,"M-3":36.29,"M-6":40.5,"Y-1":1.9,"beta":1.0732,"floatShares":64.36,"trailingRevenue":5824.34,"trailingEps":2177,"trailingProfitRate":10.19,"averageRevenueGrowth_A":6.33,"averageProfitGrowth_A":43.05,"averageEpsGrowth_A":-80.65,"RevenueGrowth_A":9.66,"RevenueGrowth_Q":-26.69,"ProfitGrowth_A":148.52,"ProfitGrowth_Q":-22.81,"EpsGrowth_A":-277.94,"EpsGrowth_Q":-70.71,"fiscalDividendYield":0.89,"fiscalDebtRatio":80.26,"pct52wHigh":-18.88,"pct52wLow":85.56,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.66,"trailingPE":12.33,"turnoverRatio":0.46,"market":"kosdaq","name":"\uc774\uc5d4\uc5d0\ud504\ud14c\ud06c\ub180\ub85c\uc9c0*","industryCode":"WI620","industryName":"\ubc18\ub3c4\uccb4","sectorCode":"G45","sectorName":"IT","stockSize":null,"timeDiff":"14 days","yield":3.27,"yieldColor":"#CF9797","profitColor":"#2F9F4F","peColor":"#2F9B4E","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/02(14\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 3.27%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 10.19%<br>\uc139\ud130: IT<br>\uc5c5\uc885: \ubc18\ub3c4\uccb4<br>\uc2dc\uac00\ucd1d\uc561: 3872\uc5b5\uc6d0<br>"},"017960":{"startDate":"2025-04-09","startBuy":17400,"date":"2025\/04\/16","close":18810,"marketCap":"9810\uc5b5","volume":898086,"amount":16911927230,"PBR":2.04,"dividendYield":0.58,"foreignRate":7.82,"D-1":-3.64,"W-1":7.86,"M-1":21.12,"M-3":48.11,"M-6":71.78,"Y-1":84.96,"beta":0.9231,"floatShares":62.75,"trailingRevenue":7417.41,"trailingEps":391,"trailingProfitRate":6.13,"averageRevenueGrowth_A":18.87,"averageProfitGrowth_A":15.35,"averageEpsGrowth_A":-107.65,"RevenueGrowth_A":24.78,"RevenueGrowth_Q":13.79,"ProfitGrowth_A":176.0,"ProfitGrowth_Q":126.12,"EpsGrowth_A":-233.45,"EpsGrowth_Q":-105.08,"fiscalDividendYield":1.11,"fiscalDebtRatio":85.32,"pct52wHigh":-2.13,"pct52wLow":99.89,"pctEstimated":-12.51,"estimatedPE":15.02,"trailingPS":1.32,"trailingPE":48.11,"turnoverRatio":1.72,"market":"kospi","name":"\ud55c\uad6d\uce74\ubcf8","industryCode":"WI240","industryName":"\uc870\uc120","sectorCode":"G20","sectorName":"\uc0b0\uc5c5\uc7ac","stockSize":null,"timeDiff":"7 days","yield":8.1,"yieldColor":"#FC7B7B","profitColor":"#337F4E","peColor":"#F63538","epeColor":"#32894E","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/09(7\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 8.1%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 6.13%<br>\uc139\ud130: \uc0b0\uc5c5\uc7ac<br>\uc5c5\uc885: \uc870\uc120<br>\uc2dc\uac00\ucd1d\uc561: 9810\uc5b5\uc6d0<br>"},"016590":{"startDate":"2025-04-09","startBuy":7170,"date":"2025\/04\/16","close":7460,"marketCap":"3006\uc5b5","volume":57925,"amount":442555280,"PBR":0.43,"dividendYield":2.01,"foreignRate":2.85,"D-1":-4.24,"W-1":6.12,"M-1":13.37,"M-3":29.97,"M-6":31.57,"Y-1":32.98,"beta":0.3715,"floatShares":16.25,"trailingRevenue":6585.03,"trailingEps":871,"trailingProfitRate":4.45,"averageRevenueGrowth_A":2.14,"averageProfitGrowth_A":-14.3,"averageEpsGrowth_A":-2.63,"RevenueGrowth_A":2.04,"RevenueGrowth_Q":3.05,"ProfitGrowth_A":-49.95,"ProfitGrowth_Q":212.65,"EpsGrowth_A":-26.6,"EpsGrowth_Q":-841.18,"fiscalDividendYield":3.49,"fiscalDebtRatio":26.56,"pct52wHigh":0.0,"pct52wLow":51.78,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.46,"trailingPE":8.56,"turnoverRatio":0.15,"market":"kospi","name":"\uc2e0\ub300\uc591\uc81c\uc9c0","industryCode":"WI200","industryName":"\ube44\ucca0\uae08\uc18d","sectorCode":"G15","sectorName":"\uc18c\uc7ac","stockSize":null,"timeDiff":"7 days","yield":4.04,"yieldColor":"#D99494","profitColor":"#36704E","peColor":"#2FB855","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/09(7\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 4.04%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 4.45%<br>\uc139\ud130: \uc18c\uc7ac<br>\uc5c5\uc885: \ube44\ucca0\uae08\uc18d<br>\uc2dc\uac00\ucd1d\uc561: 3006\uc5b5\uc6d0<br>"}};


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
