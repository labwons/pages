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
const srcTickers = {"251970":{"startDate":"2025-03-28","startBuy":49200,"date":"2025-04-04","close":53600,"marketCap":"6646\uc5b5","volume":63660,"amount":3419901500,"PBR":2.79,"dividendYield":0.71,"foreignRate":12.23,"D-1":-1.11,"W-1":8.94,"M-1":29.47,"M-3":23.08,"M-6":57.42,"Y-1":135.09,"beta":0.6781,"floatShares":39.33,"trailingRevenue":3374.84,"trailingEps":2637,"trailingProfitRate":14.34,"averageRevenueGrowth_A":14.56,"averageProfitGrowth_A":16.79,"averageEpsGrowth_A":15.2,"RevenueGrowth_A":18.63,"RevenueGrowth_Q":5.46,"ProfitGrowth_A":37.14,"ProfitGrowth_Q":4.63,"EpsGrowth_A":21.13,"EpsGrowth_Q":25.94,"fiscalDividendYield":0.97,"fiscalDebtRatio":27.12,"pct52wHigh":-0.74,"pct52wLow":136.12,"pctEstimated":-8.77,"estimatedPE":16.85,"trailingPS":1.97,"trailingPE":20.33,"turnoverRatio":0.51,"market":"kosdaq","name":"\ud38c\ud14d\ucf54\ub9ac\uc544*","industryCode":"WI200","industryName":"\ube44\ucca0\uae08\uc18d","sectorCode":"G15","sectorName":"\uc18c\uc7ac","stockSize":null,"timeDiff":"7 days","yield":8.94,"yieldColor":"#FA7272","profitColor":"#2FC558","peColor":"#396250","epeColor":"#337D4E","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/03\/28(7\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 8.94%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 14.34%<br>\uc139\ud130: \uc18c\uc7ac<br>\uc5c5\uc885: \ube44\ucca0\uae08\uc18d<br>\uc2dc\uac00\ucd1d\uc561: 6646\uc5b5\uc6d0<br>"},"102710":{"startDate":"2025-04-02","startBuy":26000,"date":"2025-04-04","close":25300,"marketCap":"3614\uc5b5","volume":187079,"amount":4631397800,"PBR":1.0,"dividendYield":0.2,"foreignRate":6.88,"D-1":-2.69,"W-1":-1.56,"M-1":10.24,"M-3":47.09,"M-6":20.48,"Y-1":-2.69,"beta":1.1093,"floatShares":64.36,"trailingRevenue":5824.34,"trailingEps":2177,"trailingProfitRate":10.19,"averageRevenueGrowth_A":6.33,"averageProfitGrowth_A":43.05,"averageEpsGrowth_A":-80.65,"RevenueGrowth_A":9.66,"RevenueGrowth_Q":-26.69,"ProfitGrowth_A":148.52,"ProfitGrowth_Q":-22.81,"EpsGrowth_A":-277.94,"EpsGrowth_Q":-70.71,"fiscalDividendYield":0.89,"fiscalDebtRatio":80.26,"pct52wHigh":-23.56,"pct52wLow":74.84,"pctEstimated":null,"estimatedPE":null,"trailingPS":0.62,"trailingPE":11.62,"turnoverRatio":1.28,"market":"kosdaq","name":"\uc774\uc5d4\uc5d0\ud504\ud14c\ud06c\ub180\ub85c\uc9c0*","industryCode":"WI620","industryName":"\ubc18\ub3c4\uccb4","sectorCode":"G45","sectorName":"IT","stockSize":null,"timeDiff":"2 days","yield":-2.69,"yieldColor":"#92AFC7","profitColor":"#2F9F4F","peColor":"#2FA04F","epeColor":"#414554","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/02(2\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: -2.69%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 10.19%<br>\uc139\ud130: IT<br>\uc5c5\uc885: \ubc18\ub3c4\uccb4<br>\uc2dc\uac00\ucd1d\uc561: 3614\uc5b5\uc6d0<br>"},"005180":{"startDate":"2025-04-03","startBuy":97000,"date":"2025-04-04","close":99000,"marketCap":"9723\uc5b5","volume":34628,"amount":3402878700,"PBR":1.36,"dividendYield":2.63,"foreignRate":21.45,"D-1":0.3,"W-1":5.77,"M-1":4.54,"M-3":21.62,"M-6":60.45,"Y-1":68.37,"beta":0.3554,"floatShares":48.86,"trailingRevenue":14630.42,"trailingEps":10479,"trailingProfitRate":8.97,"averageRevenueGrowth_A":11.26,"averageProfitGrowth_A":54.45,"averageEpsGrowth_A":-33.21,"RevenueGrowth_A":4.93,"RevenueGrowth_Q":-37.27,"ProfitGrowth_A":16.95,"ProfitGrowth_Q":-99.03,"EpsGrowth_A":19.73,"EpsGrowth_Q":-101.71,"fiscalDividendYield":4.05,"fiscalDebtRatio":38.96,"pct52wHigh":-11.69,"pct52wLow":73.08,"pctEstimated":-20.16,"estimatedPE":8.7,"trailingPS":0.66,"trailingPE":9.45,"turnoverRatio":0.35,"market":"kospi","name":"\ube59\uadf8\ub808","industryCode":"WI400","industryName":"\ud544\uc218\uc18c\ube44\uc7ac","sectorCode":"G30","sectorName":"\ud544\uc218\uc18c\ube44\uc7ac","stockSize":null,"timeDiff":"1 days","yield":2.06,"yieldColor":"#C09C9C","profitColor":"#30954E","peColor":"#2FB153","epeColor":"#2FB755","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/03(1\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 2.06%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 8.97%<br>\uc139\ud130: \ud544\uc218\uc18c\ube44\uc7ac<br>\uc5c5\uc885: \ud544\uc218\uc18c\ube44\uc7ac<br>\uc2dc\uac00\ucd1d\uc561: 9723\uc5b5\uc6d0<br>"},"097520":{"startDate":"2025-04-04","startBuy":24000,"date":"2025-04-04","close":24050,"marketCap":"4323\uc5b5","volume":24206,"amount":583493325,"PBR":1.31,"dividendYield":2.49,"foreignRate":9.53,"D-1":-0.62,"W-1":0.21,"M-1":3.44,"M-3":20.31,"M-6":33.39,"Y-1":-3.02,"beta":1.049,"floatShares":61.88,"trailingRevenue":10570.58,"trailingEps":3538,"trailingProfitRate":4.2,"averageRevenueGrowth_A":-3.93,"averageProfitGrowth_A":24.75,"averageEpsGrowth_A":27.44,"RevenueGrowth_A":13.36,"RevenueGrowth_Q":21.76,"ProfitGrowth_A":143.55,"ProfitGrowth_Q":499.68,"EpsGrowth_A":127.82,"EpsGrowth_Q":970.5,"fiscalDividendYield":4.17,"fiscalDebtRatio":54.24,"pct52wHigh":-9.76,"pct52wLow":43.5,"pctEstimated":-26.38,"estimatedPE":8.53,"trailingPS":0.41,"trailingPE":6.8,"turnoverRatio":0.13,"market":"kospi","name":"\uc5e0\uc528\ub125\uc2a4","industryCode":"WI610","industryName":"IT\ud558\ub4dc\uc6e8\uc5b4","sectorCode":"G45","sectorName":"IT","stockSize":null,"timeDiff":"0 days","yield":0.21,"yieldColor":"#A8A5A5","profitColor":"#366E4E","peColor":"#2FC558","epeColor":"#2FB855","meta1":"\ud22c\uc790 \uc2dc\uc791\uc77c: 2025\/04\/04(0\uc77c\ucc28)<br>\ud22c\uc790 \uc218\uc775\ub960: 0.21%<br>","meta2":"\uc601\uc5c5\uc774\uc775\ub960: 4.2%<br>\uc139\ud130: IT<br>\uc5c5\uc885: IT\ud558\ub4dc\uc6e8\uc5b4<br>\uc2dc\uac00\ucd1d\uc561: 4323\uc5b5\uc6d0<br>"}};


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
