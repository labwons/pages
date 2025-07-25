/* ======================================================================
    COMMON EVENTS
====================================================================== */
$('.mobile-nav-toggle').on('click', function() {
  $('body').toggleClass('mobile-nav-active');
  $(this).toggleClass('bi-list bi-x');
});
$('#navmenu a').on('click', function() {
  if ($('.mobile-nav-active').length) {
    $('body').toggleClass('mobile-nav-active');
    $('.mobile-nav-toggle').toggleClass('bi-list bi-x');
  }
});
$('.navmenu .toggle-dropdown').on('click', function(e) {
  e.preventDefault();
  $(this).parent().next().toggleClass('dropdown-active');
  e.stopImmediatePropagation();
});
$('.scroll-top').on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({ scrollTop: 0 }, 'fast');
});
$('.faq-q').on('click', function() {
  $(this).parent().toggleClass('faq-active');
});
$(window).on('load scroll', function() {
  const $scrollTop = $('.scroll-top');
  if ($scrollTop.length) {
    if ($(window).scrollTop() > 100) {
      $scrollTop.addClass('active');
    } else {
      $scrollTop.removeClass('active');
    }
  }
});


const __media__ = {
  isMobile: window.matchMedia('(min-width: 0px) and (max-width: 767px)').matches,
  isTablet: window.matchMedia('(min-width: 768px) and (max-width: 1023px)').matches,
  isLabtop: window.matchMedia('(min-width: 1024px) and (max-width: 1439px)').matches,
  isDesktop: window.matchMedia('(min-width: 1440px)').matches,
  hasCursor: window.matchMedia('(pointer: fine)').matches
}
const __fonts__ = 'NanumGothic, Nanum Gothic, Open Sans, sans-serif';

function __mergeJson__(target, source) {
  for (const key in source) {
    if (
      source[key] &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key])
    ) {
      if (!target[key]) target[key] = {};
      __mergeJson__(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

/* -----------------------------------------------------------
 * MARKET MAP OPERATION 
----------------------------------------------------------- */
let updateCenteredSlide;
let getCurrentServiceState;
let setMainTypes;
let setMainOptions;
let setSearchBar;
let setScaleBar;
let setBar;
let setMap;
let eventClickTreemap;

if (SERVICE === "marketmap"){
  const mouseEvent   = document.createEvent('MouseEvent');
  const $mapToggle   = $('.map-switch i');
  const $mainTypes   = $('.map-select.types');
  const $mainOptions = $('.map-select.options');
  const $searchBar   = $('.map-select.map-searchbar');
  const $mapLegend   = $('.legends .legend');
  const $mapReset    = $('.map-reset');

  var currentMapViewer = 'all';
  var currentBarViewer = 'industry';
  var currentOption    = 'return1Day';
  
  mouseEvent.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);

  updateCenteredSlide = function(swiperInstance) {
    const slides = swiperInstance.slides;
    slides.forEach(slide => slide.classList.remove('centered'));

    const activeIndex = swiperInstance.activeIndex;
    const centeredIndex = activeIndex + 1;

    if (slides[centeredIndex]) {
      slides[centeredIndex].classList.add('centered');
    }
  };

  getCurrentServiceState = function() {
    return $mapToggle.hasClass('bi-bar-chart-line-fill') ? 'bar' : 'map';
  };

  setMainTypes = function(reset) {
    if ((getCurrentServiceState() == 'map') || reset) {
      $mainTypes.empty()
      .append(`<option value="all" selected>\ub300\ud615\uc8fc</option>`)
      .append(`<option value="woS">\ub300\ud615\uc8fc\u0028\uc0bc\uc131\uc804\uc790\u0020\uc81c\uc678\u0029</option>`)
      .find('option[value="' + currentMapViewer + '"]').prop('selected', true);
    } else {
      $mainTypes.empty()
      .append(`<option value="sector">\uc139\ud130\u0020\u0053\u0065\u0063\u0074\u006f\u0072</option>`)
      .append(`<option value="industry">\uc5c5\uc885\u0020\u0049\u006e\u0064\u0075\u0073\u0074\u0072\u0079</option>`)
      .find('option[value="' + currentBarViewer + '"]').prop('selected', true);
    }
  };

  setMainOptions = function(){
    $mainOptions.empty();
    Object.entries(srcIndicatorOpt).forEach(([key, obj]) => {
      $mainOptions.append(`<option value="${key}">${obj.label}</option>`);
    });
    $mainOptions.find('option[value="' + currentOption + '"]').prop('selected', true);
  };

  setSearchBar = function(){
    $searchBar.empty().append('<option></option>');
    Object.entries(srcTicker)
    .sort((a, b) => b[1].size - a[1].size)
    .forEach(([ticker, obj]) => {
      if (
          ticker.startsWith('N') ||
          ticker.startsWith('W') ||
          ( (currentMapViewer === 'woS') && (ticker === '005930') )
      ){
          return
      }
      $searchBar.append('<option value="' + ticker + '">' + obj.name + '</option>');
    });

    $searchBar.select2({
      placeholder: "\uc885\ubaa9\uba85\u0020\uac80\uc0c9",
      allowClear: true
    });
  };

  setScaleBar = function(){
    let indicator = srcIndicatorOpt[currentOption];
    $mapLegend.each(function(n) {
      if(indicator.scale[n] == null){
        $(this).html('&nbsp; - &nbsp;');
      } else {
        $(this).html(indicator.scale[n] + indicator.unit);
      }
      $(this).css('background-color', indicator.color[n]);
    });
  };
  
  eventClickTreemap = function(item){
    $('g.slicetext').each(function(){
      if ($(this).text().includes(item)) {
        !$(this).get(0).dispatchEvent(mouseEvent);
        return
      }
    })
  }

  setBar = function(key) {
    var layout = {
      margin:{
        l:10,
        r:0,
        t:10,
        b:22
      },
      xaxis:{
        autorange: false,
        showticklabels: false,
        showline: false,
        range:[0, 0],
      },
      yaxis:{
        showline: false,
        zeroline: false,
        showticklabels: false
      },
      dragmode: false
    };
    var option = {
      scrollZoom: false,
      displayModeBar:false,
      responsive:true,
      showTips:false,
    };    
    var data = {
      type:'bar',
      x:[],
      y:[],
      orientation:'h',
      marker: {
          color:[]
      },
      text:[],
      textposition: 'outside',
      meta:[],
      hovertemplate: '%{meta}<br>' + srcIndicatorOpt[key].label + ': %{text}<extra></extra>',
      opacity:0.9
    };

    var tickers = [];
    Object.entries(srcTicker).forEach(([ticker, obj]) => {
      if (
        ( (currentBarViewer === 'sector') && (ticker.startsWith('W') && ticker.includes('G')) ) ||
        ( (currentBarViewer === 'industry') && (ticker.startsWith('W') && (!ticker.includes('G'))) )
      ){
        if (ticker !== 'WS0000'){
          obj.ticker = ticker;
          tickers.push(obj);
        }
      }
    });
    tickers.forEach(obj => {
      if (typeof obj[key] === 'string'){
        obj[key] = parseFloat(obj[key].replace(srcIndicatorOpt[key].unit, ""));
      }      
    });
    
    tickers.sort((a, b) => a[key] - b[key]).forEach(item => {
      data.x.push(Math.abs(item[key]));
      data.y.push(item.name);
      data.marker.color.push(item[`${key}Color`]);
      data.text.push(`${item[key]}${srcIndicatorOpt[key].unit}`);
      data.meta.push(item.meta);
    });
    data.x = data.x.map(item => item + 0.3333 * Math.max(...data.x));
    layout.annotations = data.y.map(item => {
      return {
        x:0,
        y:item,
        xref:'x',
        yref:'y',
        text: item,
        showarrow:false,
        font: {
          family:__fonts__,
          color:'#ffffff',
          size:13,
        },
        xanchor:'left',
        yanchor:'middle'
      }
    })
    layout.xaxis.range = [0, 1.2 * Math.max(...data.x)];

//    if (isNarrow.matches) {
//        var xrange = 1.75 * maxX;
//    } else if (isMobile.matches) {
//        var xrange = 1.5 * maxX;
//    } else if (isTablet.matches) {
//        var xrange = 1.25 * maxX;
//    } else {
//        var xrange = 1.1 * maxX;
//    }

    Plotly.newPlot('plotly', [data], layout, option);
  }

  setMap = function(key) {
    var layout = {
      margin: {
        l:0,
        r:0,
        t:0,
        b:25
      },
      annotations: [{
        text: "©LAB￦ONS",
        xref: "paper",
        yref: "paper",
        x: 0,
        y: 1,
        xanchor: "left",
        yanchor: "top",
        showarrow: false,
        font: {
          size: 12,
          color: "white"
        }
      }],
    };
    var option = {
      displayModeBar:false,
      responsive:true,
      showTips:false
    };
    var data = {
      type:'treemap',
      branchvalues:'total',
      labels: [],
      parents: [],
      values: [],
      text: [],
      meta: [],
      textposition:'middle center',
      textfont:{
        family:__fonts__,
        color:'#ffffff'
      },
      texttemplate: '%{label}<br>%{text}',
      marker: {
        colors: [],
        visible: true,
      },
      hovertemplate: '%{meta}<br>' + srcIndicatorOpt[key].label + ': %{text}<extra></extra>',
      hoverlabel: {
        font: {
          family: __fonts__,
          color: '#ffffff'
        }
      },
      opacity: 0.9,
      pathbar:{
        visible: true,
      }
    };

    Object.entries(srcTicker).forEach(([ticker, obj]) => {
      if (currentMapViewer === 'woS') {
        if ( (ticker == '005930') || ticker.startsWith('W') ) {
          return
        }
      } else {
        if (ticker.startsWith('N')) {
          return
        }
      }
      data.labels.push(obj.name);
      data.parents.push(obj.ceiling);
      data.values.push(obj.size);
      data.text.push(obj[key]);
      data.meta.push(obj.meta);
      data.marker.colors.push(obj[`${key}Color`]);
    });
    Plotly.newPlot('plotly', [data], layout, option);
  }
  
  $mainTypes.on('change', function() {
    if (getCurrentServiceState() === 'map') {
      currentMapViewer = $(this).val();
      setMap(currentOption);
      setSearchBar();
    } else {
      currentBarViewer = $(this).val();
      setBar(currentOption)
    }
  });

  $mainOptions.on('change', function() {
    currentOption = $(this).val();
    if (getCurrentServiceState() === 'map') {
      setMap(currentOption);
    } else {
      setBar(currentOption)
    }
    setScaleBar();
  });

  $mapReset.on('click', function() {
    currentMapViewer = 'all';
    currentOption = 'return1Day';
    setMainTypes(true);
    setMainOptions();
    setScaleBar();
    setSearchBar();
    setMap(currentOption);
    $searchBar.prop('disabled', false);
    if (getCurrentServiceState() === 'bar') {
      $mapToggle
      .toggleClass("bi-geo-alt-fill bi-bar-chart-line-fill")
      .css('transform', 'none');
    }
  });

  $mapToggle.on('click', function() {
    $(this).toggleClass("bi-geo-alt-fill bi-bar-chart-line-fill");
    if ($(this).hasClass('bi-bar-chart-line-fill')) {
      setBar(currentOption);
      $(this).css('transform', 'scaleX(-1) rotate(-90deg)');
      $searchBar.prop('disabled', true);
    } else {
      setMap(currentOption);
      $(this).css('transform', 'none');
      $searchBar.prop('disabled', false);
    }
    setMainTypes(false);
  });

  $searchBar.on('select2:select', function(e){
    const ticker = srcTicker[e.params.data.id];
    eventClickTreemap(ticker.ceiling);
    setTimeout(function(){
        eventClickTreemap(ticker.name);
    }, 1000);
  });

  $searchBar.on('select2:clear', function(e){
    setMap(currentOption);
  });

  $('#plotly').dblclick(function(){
    if (getCurrentServiceState() === 'map') {
      setMap(currentOption);
    }
  });  

  $('.service-status-value').on('click', function() {
    window.open(`/stocks/${$(this).attr('data-ticker')}/`, '_blank');
  });

  new Swiper('.swiper', {
    loop: true,
    speed: 600,
    autoplay: {
      delay: 5000
    },
    slidesPerView: "auto",
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      "320": {
        "slidesPerView": 1,
        "spaceBetween": 40
      },
      "1200": {
        "slidesPerView": 3,
        "spaceBetween": 1
      }
    },
    on: {
      slideChange: function () {
        updateCenteredSlide(this);
      },
      init: function () {
        updateCenteredSlide(this);
      }
    }
  });

  setMainTypes(false);
  setMainOptions();
  setScaleBar();
  setSearchBar();
  setMap(currentOption);
}

/* -----------------------------------------------------------
 * MARKET BUBBLE OPERATION 
----------------------------------------------------------- */
let setOption, setAxisLabel, setBubbleSearchBar, setBubble;
let startDrag, onDrag, stopDrag;
let lineMap;

if (SERVICE === "bubble"){
  const root = document.querySelector(':root');
  const cssVY = parseInt(getComputedStyle(root).getPropertyValue('--slider-button-y'));
  const cssVX = parseInt(getComputedStyle(root).getPropertyValue('--slider-button-x'));
  const cssHX = cssVY;
  const cssHY = cssVX;
  const $x = $('.bubble-x');
  const $y = $('.bubble-y');
  const $sectors = $('.bubble-sector');
  const $bubbleSearchBar = $('.bubble-searchbar');
  const $ySlider = $('.slider-y-range');
  const $xSlider = $('.slider-x-range');

  var isDragging = false;
  var slider = '';
  var currentX = 'return1Day';
  var currentY = 'return3Month';
  var currentSector = 'ALL';
  var yValMin = 100;
  var yValMax = 0;
  var yValMinO = 100;
  var yValMaxO = 0;
  var xValMin = 100;
  var xValMax = 0;
  var xValMinO = 100;
  var xValMaxO = 0;

  setOption = function() {
    $x.empty();
    $y.empty();
    $sectors.empty();
    Object.entries(srcIndicatorOpt).forEach(([key, obj]) => {
      if (obj.dtype === "str") { return }
      if (key == currentX) {
        $x.append(`<option value="${key}" selected>${obj.label}</option>`);
      } else {
        $x.append(`<option value="${key}">${obj.label}</option>`);
      }
      if (key === currentY) {
        $y.append(`<option value="${key}" selected>${obj.label}</option>`);
      } else {
        $y.append(`<option value="${key}">${obj.label}</option>`);
      }      
    });

    Object.entries(srcSectors).forEach(([key, obj]) => {
      $sectors.append(`<option value="${key}">${obj.sectorName}</option>`);
    })
  };

  setBubbleSearchBar = function(){
    $bubbleSearchBar.empty().append('<option></option>');

    Object.entries(srcTickers)
    .sort((a, b) => b[1].size - a[1].size)
    .forEach(([ticker, obj]) => {
      if ((currentSector != 'ALL') && (currentSector != obj.sectorCode)){
        return
      }
      $bubbleSearchBar.append('<option value="' + ticker + '">' + obj.name + '</option>');
    });
    $bubbleSearchBar.select2({placeholder: "종목 찾기", allowClear: true});
  };

  setBubble = function(x, y, sector) {
    var xObj = srcIndicatorOpt[x];
    var yObj = srcIndicatorOpt[y];
    var bubbleLayout = {
      dragmode: false,
      doubleClick: false,
      margin:{
        l:20,
        r:0,
        t:0,
        b:35
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
      images: [{
        source: "/src/img/logo-footer.png",
        xref: "paper",
        yref: "paper",
        x: 0.97,
        y: 0.02,
        sizex: __media__.isMobile ? 0.2:0.1,
        sizey: __media__.isMobile ? 0.2:0.1,
        xanchor: "right",
        yanchor: "bottom",
        opacity: 0.3,
        layer: "above"
      }]    
    };
    var bubbleOption = {
      doubleClick: false,
      showTips:false,
      responsive:true,
      displayModeBar:true,
      // modeBarButtonsToRemove: ["select2d", "lasso2d", "zoomin", "zoomout", "resetScale", "toImage"],
      modeBarButtonsToRemove: ["select2d", "lasso2d", "resetScale", "toImage"],
      displaylogo:false,   
    };

    var labelX = xObj.label;
    if (labelX.includes("(")) {
      labelX = labelX.replace(/\([^)]*\)/g, '');
    }
    var hoverX = `%{x:.${xObj.digit}f}`;
    if (xObj.dtype === 'int') {
      hoverX = `%{x:,d}`;
    }
    if (xObj.text) {
      hoverX = '%{text}';
    }

    var labelY = yObj.label;
    if (labelY.includes("(")) {
      labelY = labelY.replace(/\([^)]*\)/g, '');
    }
    var hoverY = `%{y:.${yObj.digit}f}`;
    if (yObj.dtype === 'int') {
      hoverY = `%{y:,d}`;
    }
    if (yObj.text) {
      hoverY = '%{customdata}';
    }

    var hover = `%{meta}<br>${labelX}: ${hoverX}${xObj.unit}<br>${labelY}: ${hoverY}${yObj.unit}<extra></extra>`;
    var data = {
      type:'scatter',
      x:[],
      y:[],
      mode:'markers',
      meta:[],
      text:[],
      customdata:[],
      hovertemplate: hover,
      hoverlabel: {
        font: {
          family: __fonts__,
          color: '#fffff'
        }
      },
      marker: {
        size:[],
        color:[],
        line: {
          width:1.0,
        },
        opacity: 0.7,        
      },
    };
    
    Object.entries(srcTickers).forEach(([ticker, obj]) => {
      if ( (sector != 'ALL') && (sector != obj.sectorCode) ) {
        return;
      }
      data.x.push(obj[x]);
      data.y.push(obj[y]);
      data.meta.push(obj.meta);
      data.marker.size.push(obj.size);
      data.marker.color.push(srcSectors[obj.sectorCode].color);	
      if (xObj.text){
        data.text.push(obj[`${x}Text`]);
      }	
      if (yObj.text){
        data.customdata.push(obj[`${y}Text`]);
      }	
    });
    
    
    bubbleLayout.xaxis.title = xObj.label + (xObj.unit ? '[' + xObj.unit + ']' : '');
    bubbleLayout.yaxis.title = yObj.label + (yObj.unit ? '[' + yObj.unit + ']' : '');
    bubbleLayout.shapes = [{
      type:'line',
      xref:'paper',
      x0:0, x1:1,
      y0:yObj.mean,
      y1:yObj.mean,
      line:{
        color:'grey',
        width: 1,
        dash:'dot'
      }
    },{
      type:'line',
      yref:'paper',
      x0:xObj.mean, 
      x1:xObj.mean,
      y0:0,
      y1:1,
      line:{
        color:'grey',
        width: 1,
        dash:'dot'
      }
    }];
    
    Plotly.newPlot('plotly', [data], bubbleLayout, bubbleOption)
    .then(grid => {
      yValMinO = grid.layout.yaxis.range[0];
      yValMaxO = grid.layout.yaxis.range[1]; 
      yValMin = grid.layout.yaxis.range[0];
      yValMax = grid.layout.yaxis.range[1];
      xValMinO = grid.layout.xaxis.range[0];
      xValMaxO = grid.layout.xaxis.range[1]; 
      xValMin = grid.layout.xaxis.range[0];
      xValMax = grid.layout.xaxis.range[1];
      $('a[data-title="Zoom"]').attr("data-title", "확대");
      $('a[data-title="Pan"]').attr("data-title", "이동(패닝)");
      $('a[data-title="Autoscale"]').attr("data-title", "자동 조정");
      $('.modebar').prepend($('<div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="스크롤 모드" data-toggle="false" data-gravity="n"><i class="bi bi-arrow-down-up"></i></a></div>'));
      grid.on('plotly_doubleclick', function(e) {
        yValMin = yValMinO;
        yValMax = yValMaxO;
        xValMin = xValMinO;
        xValMax = xValMaxO;
      })
    });
  }

  lineMap = function(x1, y1, x2, y2, x) {
    return ((y2 - y1) / (x2 - x1)) * x + (y1 - ((y2 - y1) / (x2 - x1)) * x1);
  }

  startDrag = function(e) {
    $_class = $(e.target).attr('class');
    if ((typeof $_class === "string") && ($_class.includes('-slider-'))) {
      $('body').css({'user-select': 'none', 'overflow': 'hidden'});
      slider = $_class;
    } else {
      slider = "";
    }
  };

  onDrag = function(x, y) {
    if (slider.includes('y-slider')) {
      let posY = y - $ySlider.offset().top;

      if (slider.includes('top')) {
        let lowLim = $('.y-slider-bottom')[0].offsetTop - cssVY;
        posY = Math.max(0, Math.min(posY, lowLim));
      } else {
        let highLim = $('.y-slider-top')[0].offsetTop + cssVY;
        posY = Math.max(highLim, Math.min(posY, $ySlider.height() - cssVY));
      }
      if (!$('.service-app').find('.y-ranger').length){
        $('.service-app').append('<div class="y-ranger"></div>');
      }

      $(`.${slider}`).css('top', `${posY}px`);
      $('.y-ranger').css({
        'top': `${posY + (cssVY / 2)}px`,
        'left': `${cssVX}px`
      });
      
    } else if (slider.includes('x-slider')) {
      let posX = x - $xSlider.offset().left;

      if (slider.includes('left')) {
        let highLim = $('.x-slider-right')[0].offsetLeft - cssHX;
        posX = Math.max(0, Math.min(posX, highLim));
      } else {
        let lowLim = $('.x-slider-left')[0].offsetLeft + cssHX;
        posX = Math.min(Math.max(lowLim, posX), $xSlider.width() - cssHX);
      }
      if (!$('.service-app').find('.x-ranger').length){
        $('.service-app').append('<div class="x-ranger"></div>');
      }
      $(`.${slider}`).css('left', `${posX}px`);
      $('.x-ranger').css({
        'left': `${posX + 20 + cssVX + (cssHX / 2) + 2}px`,
        'bottom': `${cssHY}px`
      })

    } else {}

  };

  stopDrag = function() {
    if (slider.includes('-slider-')){
      $('body').css({'user-select': 'auto', 'overflow': ''});
      if ($('.service-app').find('.y-ranger').length){
        $('.service-app').find('.y-ranger').remove();
      }
      if ($('.service-app').find('.x-ranger').length){
        $('.service-app').find('.x-ranger').remove();
      }

      if (slider === 'y-slider-top') {
        yValMax = lineMap(0, yValMax, $ySlider.height() - cssVY, yValMin, parseFloat($(`.${slider}`).css('top')));
        $(`.${slider}`).css('top', '0');
      } else if (slider === 'y-slider-bottom') {
        yValMin = lineMap(0, yValMax, $ySlider.height() - cssVY, yValMin, parseFloat($(`.${slider}`).css('top')));
        $(`.${slider}`).css('top', `${$('.slider-vertical').height() - 35 - cssVY / 2}px`);
      } else if (slider === 'x-slider-left') {
        xValMin = lineMap(0, xValMin, $xSlider.width() - cssHX, xValMax, parseFloat($(`.${slider}`).css('left')));
        $(`.${slider}`).css('left', '0');
      } else if (slider === 'x-slider-right') {
        xValMax = lineMap(0, xValMin, $xSlider.width() - cssHX, xValMax, parseFloat($(`.${slider}`).css('left')));
        $(`.${slider}`).css({'left':'', 'right': '0'});
      } else { }
      Plotly.relayout('plotly', {
        'xaxis.range': [xValMin, xValMax],
        'yaxis.range': [yValMin, yValMax]
      });
    }
    slider = "";
  };

  $x.on('change', function() {
    currentX = $(this).val();
    setBubble(currentX, currentY, currentSector);
    $bubbleSearchBar.val(null).trigger('change');
  });

  $y.on('change', function() {
    currentY = $(this).val();
    setBubble(currentX, currentY, currentSector);
    $bubbleSearchBar.val(null).trigger('change');
  });
  
  $sectors.on('change', function() {
    currentSector = $(this).val();
    setBubble(currentX, currentY, currentSector);
  });

  $bubbleSearchBar.on('select2:select', function(e){
    let _ticker = srcTickers[e.params.data.id];
    const update = {
      annotations: [{
        x:_ticker[currentX],
        y:_ticker[currentY],
        xref:'x', yref:'y',
        text: '',
        showarrow: true,
      }]
    };
    Plotly.relayout('plotly', update);
  });

  $bubbleSearchBar.on('select2:clear', function(e){
    Plotly.relayout('plotly', {annotations:[]});
  });

  $(document)
  .on('mousedown', function(e) {
    startDrag(e);
  })
  .on('touchstart', function(e) {
    const _e = e.originalEvent.touches[0];
    startDrag(e);
  })
  .on('mousemove', function(e) {
    onDrag(e.pageX, e.pageY);
  })
  .on('touchmove', function(e) {
    const _e = e.originalEvent.touches[0];
    onDrag(_e.pageX, _e.pageY);
  })
  .on('mouseup', function() {
    stopDrag();
  })
  .on('touchend', function() {
    stopDrag();
  })
  .on('touchcancel', function() {
    stopDrag();
  })
  .on('click', '.bi-arrow-down-up', function() {
    Plotly.relayout('plotly', {dragmode: false});
    $(this).css('opacity', '0.8');
  })
  .on('click', '.modebar', function(e) {
    if (!$(e.target).is('i')){
      $('.bi-arrow-down-up').css('opacity', '0.3');
    }
  });

  $('.to-stock').on('click', function() {
    window.open(`/stocks/${$(this).attr('data-ticker')}/`, '_blank');
  });

  $ySlider.css('height', `${$('.slider-vertical').height() - 35}px`);
  $('.y-slider-bottom').css('top', `${$('.slider-vertical').height() - 35 - cssVY / 2}px`);
  if (!__media__.hasCursor) {
    $('.slider-vertical').remove();
    $('.service-layer-bottom').remove();
  }

  setOption();
  setBubbleSearchBar();
  setBubble(currentX, currentY, currentSector);
}

/* -----------------------------------------------------------
 * MACRO OPERATION 
----------------------------------------------------------- */
let setYaxisOption;
let plotMacro;
if (SERVICE === "macro"){
  new PureCounter();
  const $y1 = $('.y1');
  const $y2 = $('.y2');
  
  var y1_selection = [];
  var y2_selection = [];
  
  setYaxisOption = function() {
    let _groups = [];

    $y1.empty().append('<option></option>');
    $y2.empty().append('<option></option>');
    Object.entries(srcIndicatorOpt)
    .forEach(([symbol, meta]) => {
      if (!_groups.includes(meta.group)){
        $y1.append(`<optgroup label="${meta.group}"></optgroup>`);
        $y2.append(`<optgroup label="${meta.group}"></optgroup>`);
        _groups.push(meta.group);
      }
      let $_group = $(`optgroup[label="${meta.group}"]`);

      $_group.append(`<option value="${symbol}">${meta.name}</option>`);
    });
    $y1.val(['1001']).trigger('change');
    y1_selection.push('1001');
    $y1.select2({
      maximumSelectionLength: 3,
      minimumResultsForSearch: Infinity
    });
    $y2.select2({
      maximumSelectionLength: 3,
      minimumResultsForSearch: Infinity
    });
  };

  plotMacro = function() {
    let layout = {
      clickmode:'event',
      dragmode: __media__.isMobile ? false : 'pan',
      margin:{
        l:20, 
        r:20, 
        t:10, 
        b:20
      }, 
      hovermode: 'x unified',
      doubleClick: false,
      legend: {
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'right',
        x:1.0,
        yanchor:'top',
        y:1.0
      },
      images: [{
        source: "/src/img/logo-footer.png",
        xref: "paper",
        yref: "paper",
        x: 0.97,
        y: 0.02,
        sizex: __media__.isMobile ? 0.2:0.1,
        sizey: __media__.isMobile ? 0.2:0.1,
        xanchor: "right",
        yanchor: "bottom",
        opacity: 0.3,
        layer: "above"
      }],
      xaxis:{
        autorange: false,
        fixedrange: true,
        tickformat: "%Y/%m/%d",
        showticklabels: true,
        showline: true,
        rangeselector: {
          buttons: [
            { step: 'all', label: 'All' },
            { count: 6, label: '6M', step:'month', stepmode: 'backward'},
            { count: 1, label: 'YTD', step:'year', stepmode: 'todate'},
            { count: 1, label: '1Y', step: 'year', stepmode: 'backward' },
            { count: 3, label: '3Y', step: 'year', stepmode: 'backward' },
            { count: 5, label: '5Y', step: 'year', stepmode: 'backward' }        
          ],
          xanchor: 'left',
          x: 0,
          yanchor: 'top',
          y:1.025
        },
      },
      yaxis:{
        side: 'left',
        showline: true,
        zeroline:true,
        zerolinecolor:'grey',
        zerolinewidth: '1.5px',
        showticklabels: true,
        tickangle: -90,
      },
      yaxis2: {
        overlaying:'y',
        side:'right',
        zeroline:false,
        showline:true,
        showgrid:false,
        showticklabels: true,
        tickangle: -90,
      },
    };
    let option = {
      showTips:false,
      responsive:true,
      displayModeBar:true,
      // modeBarButtonsToRemove: ["select2d", "lasso2d", "zoomin", "zoomout", "resetScale", "toImage"],
      modeBarButtonsToRemove: ["select2d", "lasso2d", "resetScale", "toImage"],
      displaylogo:false
    }

    var data = [];
    var y1data = Object.fromEntries(y1_selection.map(key => [key, srcIndicator[key]]));
    var y2data = Object.fromEntries(y2_selection.map(key => [key, srcIndicator[key]]));
    var fromdate = 0;
    var enddate = 0;

    for(var n = 0; n < y1_selection.length; n++){
      fromdate = Math.max(...[fromdate, parseInt(y1data[y1_selection[n]].date[0].replaceAll('-', ''))]);
      enddate = Math.max(...[enddate, parseInt(y1data[y1_selection[n]].date.at(-1).replaceAll('-', ''))]);
    }
    for(var n = 0; n < y2_selection.length; n++){
      fromdate = Math.max(...[fromdate, parseInt(y2data[y2_selection[n]].date[0].replaceAll('-', ''))]);
      enddate = Math.max(...[enddate, parseInt(y2data[y2_selection[n]].date.at(-1).replaceAll('-', ''))]);
    }
    fromdate = ('' + fromdate).replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
    enddate = ('' + enddate).replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
    layout.xaxis.range = [fromdate, enddate];

    for (const [key, _data] of Object.entries(y1data)) {
      let meta = srcIndicatorOpt[key];
      let obj = {
        x: _data.date,
        y: _data.data,
        type: 'scatter',
        mode: 'lines',
        name: meta.name,
        showlegend: true,
        hovertemplate: `${meta.name}${meta.hover}`,
        yaxis: 'y1',
      }
      if (`${key}Text` in srcIndicator) {
        obj.text = srcIndicator[`${key}Text`].data;
      }
      data.push(obj);
    };

    for (const [key, _data] of Object.entries(y2data)) {
      let meta = srcIndicatorOpt[key];
      let obj = {
        x: _data.date,
        y: _data.data,
        type: 'scatter',
        mode: 'lines',
        name: meta.name,
        showlegend: true,
        hovertemplate: `${meta.name}${meta.hover}`,
        yaxis: 'y2',
      }
      if (`${key}Text` in srcIndicator) {
        obj.text = srcIndicator[`${key}Text`].data;
      }
      if (srcIndicatorOpt[key].unit === '%') {
        layout.yaxis.zeroline = false;
        layout.yaxis2.zeroline = true;
        layout.yaxis2.zerolinecolor = 'grey';
        layout.yaxis2.zerolinewidth = '1.5px';
      }
      data.push(obj);
    };


    Plotly.newPlot('plotly', data, layout, option)
    .then(grid => {
      $('a[data-title="Zoom"]').attr("data-title", "확대");
      $('a[data-title="Pan"]').attr("data-title", "이동(패닝)");
      $('a[data-title="Autoscale"]').attr("data-title", "자동 조정");
      $('.modebar').prepend($('<div class="modebar-group"><a rel="tooltip" class="modebar-btn" data-title="스크롤 모드" data-toggle="false" data-gravity="n"><i class="bi bi-arrow-down-up"></i></a></div>'));
    });
  };

  $y1.on('select2:select', async function(e){
    if (y1_selection.length) {
      let metaN = srcIndicatorOpt[e.params.data.id];
      let metaO = srcIndicatorOpt[y1_selection[0]];
      if (metaN.unit != metaO.unit) {
        const result = await Swal.fire({
          title: "먼저 추가한 지표와 단위가 다릅니다. 계속하시겠습니까?",
          icon: "question",
          showCancelButton: true,
          confirmButtonText: "추가하기",
        });
        
        if (result.isConfirmed) {
          y1_selection.push(e.params.data.id);
          plotMacro();
          return;
        } else {
          const newValues = ($(this).val() || []).filter(val => val !== e.params.data.id);
          $(this).val(newValues).trigger('change');
          return;
        }
      }
    }
    y1_selection.push(e.params.data.id);
    plotMacro();
    $('.notice').click();
  });
  $y1.on('select2:unselect', function(e){
    y1_selection = y1_selection.filter(item => item != e.params.data.id);
    plotMacro();
    $('.notice').click();
  });
  $y2.on('select2:select', async function(e){
    if (y2_selection.length) {
      let metaN = srcIndicatorOpt[e.params.data.id];
      let metaO = srcIndicatorOpt[y2_selection[0]];
      if (metaN.unit != metaO.unit) {
        const result = await Swal.fire({
          title: "먼저 추가한 지표와 단위가 다릅니다. 계속하시겠습니까?",
          icon: "question",
          showCancelButton: true,
          confirmButtonText: "추가하기",
        });
        
        if (result.isConfirmed) {
          y2_selection.push(e.params.data.id);
          plotMacro();
          return;
        } else {
          const newValues = ($(this).val() || []).filter(val => val !== e.params.data.id);
          $(this).val(newValues).trigger('change');
          return;
        }
      }
    }
    y2_selection.push(e.params.data.id);
    plotMacro();
    $('.notice').click();
  });
  $y2.on('select2:unselect', function(e){
    y2_selection = y2_selection.filter(item => item != e.params.data.id);
    plotMacro();
    $('.notice').click();
  });

  $(document)
  .on('click', '.bi-arrow-down-up', function() {
    Plotly.relayout('plotly', {
      'dragmode': false,
      'xaxis.fixedrange': true,
      'yaxis.fixedrange': true
    });
    $(this).css('opacity', '0.8');
  })
  .on('click', '.modebar', function(e) {
    if (!$(e.target).is('i')){
      $('.bi-arrow-down-up').css('opacity', '0.3');
      Plotly.relayout('plotly', {
        'xaxis.fixedrange': false,
        'yaxis.fixedrange': false
      });
    }
  });
  $('.content-number').on('click', function(){
    var item = $(this).attr('data-symbol');
    y1_selection = [item];
    y2_selection = [];
    $y1.val([]).trigger('change');
    $y2.val([]).trigger('change');
    $y1.val(item).trigger('change');
    plotMacro();
    $('html, body').animate({
      scrollTop: $('#main').offset().top
    }, 1000);
  });

  setYaxisOption();
  plotMacro();

}

/* -----------------------------------------------------------
 * STOCK OPERATION 
----------------------------------------------------------- */
let setTechnicalOption;
let setTechnicalChart;
let setDeviationChart;
let setSalesChart;
let setAssetChart;
let setGrowthChart;
let setProductChart;
let setDivChart;
let setPbrChart;
let setPerChart;
let setPerBandChart;
let setPegChart;
let setForienRateChart;
let calcXrange;
let calcYrange;

if (SERVICE === "stock"){
  const $techOpt = $('.indicators');
  const defaultLayout = {
    font: {
      size: __media__.isMobile ? 9 : 12,
      color: 'black',
      family: __fonts__
    }
  };

  var chartSelected = {
    techMain:['ohlcv'],
    techSupp:[],
    standalone:[],
  };

  setTechnicalOption = function() {
    if (__media__.isMobile){
      $('optgroup[label="보조 지표"]').remove();
      // $('option[data-class="main"]').not('[value="ohlcv"]').remove();
    }
    if (srcProduct === null) {
      $('option[value="product"]').remove();
    }
    $techOpt.select2({
      maximumSelectionLength: 5,
      minimumResultsForSearch: Infinity,
    });
  };

  calcYrange = function(data, layout) {
    var yrange = {'y': [], 'y2': [], 'y3': [], 'y4': []};
    var yname = {'y': '', 'y2': 2, 'y3': 3, 'y4': 4};
    data.forEach(trace => {
      var n = yname[trace.yaxis];
      if (trace.type === "candlestick") {
        yrange[trace.yaxis] = [...yrange[trace.yaxis], ...trace.low.slice(xRangeN[0], xRangeN[1]), ...trace.high.slice(xRangeN[0], xRangeN[1])];
      } else {
        yrange[trace.yaxis] = [...yrange[trace.yaxis], ...trace.y.slice(xRangeN[0], xRangeN[1])];
      }

      var rng = [Math.min(...yrange[trace.yaxis]), Math.max(...yrange[trace.yaxis])];
      if (rng[0] < 0){
        rng = [1.1 * rng[0], 1.1 * rng[1]];
      } else {
        rng = [0.9 * rng[0], 1.1 * rng[1]];
      }
      
      layout[`yaxis${n}`]['range'] = rng;
    });
  }

  setTechnicalChart = function() {
    /* THIS FUNCTION IS TO PLOT PRICE AND RELATED INDICATORS */
    $('#plotly').empty();
    
    if (!__media__.isMobile) {
      const option = {
        showTips:false,
        responsive:true,
        displayModeBar:true,
        // modeBarButtonsToRemove: ["select2d", "lasso2d", "zoomin", "zoomout", "resetScale", "toImage"],
        modeBarButtonsToRemove: ["select2d", "lasso2d", "resetScale", "toImage"],
        displaylogo:false,
        doubleClick: false
      };
        
      let layout = {
        autosize: true,
        dragmode: 'pan',
        margin:{
          l:__media__.isMobile ? 30:60, 
          r:20, 
          t:10, 
          b:20
        }, 
        hovermode: 'x unified',
        legend: {
          font: defaultLayout.font,
          bgcolor:'rgba(0,0,0,0)',
          borderwidth:0,
          itemclick:'toggle',
          itemdoubleclick:'toggleothers',
          orientation:'h',
          valign:'middle',
          xanchor:'left',
          x:0.0,
          yanchor:'top',
          y:1.0
        },
        xaxis:{
          autorange: false,
          range: [xRangeN[0], xRangeN[1]],
          type:'category',
          categorygap: __media__.isMobile ? 0.2 : 0.1,
          showline: true,
          showticklabels: true,
          rangeslider: {
            visible: false,
          },
          hoverformat: '%Y/%m/%d',
          tickfont: defaultLayout.font,
          tickformat: "%Y/%m/%d",     
          tickangle:0,   
          nticks: __media__.isMobile ? 4 : 6,
          anchor: 'y',
        },
        yaxis:{
          autorange: false,
          fixedrange: true,
          range: [srcOhlcv.low[xRangeN[0]], srcOhlcv.high[xRangeN[1]]],
          showline: true,
          showticklabels: true,
          tickformat: ',d',
          tickfont: defaultLayout.font,
          domain:[0, 1],
          anchor: 'x',
        },
      };

      let data = [{
        name: "",
        x: srcDate,
        open: srcOhlcv.open,
        high: srcOhlcv.high,
        low: srcOhlcv.low,
        close: srcOhlcv.close,
        type: 'candlestick',
        showlegend: false,
        increasing: {
          line: { color: '#C92A2A' },
          fillcolor: '#C92A2A'
        },
        decreasing: {
          line: { color: '#1861A8' },
          fillcolor: '#1861A8'
        },
        xaxis: 'x',
        yaxis: 'y'
      }];

      if (chartSelected.techMain.includes('bollingerx2')) {
        data.push({
          name:'상단선',
          x:srcDate,
          y:srcBollinger.upper,
          type: 'scatter',
          mode: 'lines',
          showlegend: false,
          line: {
            color: 'grey',
            dash:'dot'
          },
          hovertemplate: 'x2상단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
        data.push({
          name:'하단선',
          x:srcDate,
          y:srcBollinger.lower,
          type: 'scatter',
          mode: 'lines',
          showlegend: false,
          line: {
            color: 'grey',
            dash:'dot'
          },
          hovertemplate: 'x2하단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
        data.push({
          name: '중간선',
          x:srcDate,
          y:srcBollinger.middle,
          type: 'scatter',
          mode: 'lines',
          showlegend: false,
          line: {
            color: 'brown',
          },
          hovertemplate: '중간: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
      }

      if (chartSelected.techMain.includes('bollingerx1')) {
        data.push({
          name:'상단선x1',
          x:srcDate,
          y:srcBollinger.upperTrend,
          type: 'scatter',
          mode: 'lines',
          showlegend: false,
          line: {
            color: 'green',
            dash:'dash'
          },
          hovertemplate: 'x1상단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
        data.push({
          name:'하단선x1',
          x:srcDate,
          y:srcBollinger.lowerTrend,
          type: 'scatter',
          mode: 'lines',
          showlegend: false,
          line: {
            color: 'green',
            dash:'dash'
          },
          hovertemplate: 'x1하단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
        var _ismiddle=false;
        for (var _n=0; _n<data.length; _n++){
          if (data[_n].name === '중간선') {_ismiddle = true;}
        }
        if (!_ismiddle){
          data.push({
            name: '중간선',
            x:srcDate,
            y:srcBollinger.middle,
            type: 'scatter',
            mode: 'lines',
            showlegend: false,
            line: {
              color: 'brown',
            },
            hovertemplate: '중간: %{y}원<extra></extra>',
            xaxis: 'x',
            yaxis: 'y'
          })
        }
      }

      if (chartSelected.techMain.includes('sma')) {
        Object.entries(srcSma).forEach(([key, _data]) => {
          var _name = key.replace("sma", "") + '일';
          data.push({
            name:_name,
            x:srcDate,
            y:_data,
            type: 'scatter',
            mode: 'lines',
            line: {
              dash:'dash',
              width: 1,
            },
            showlegend: true,
            hovertemplate: `${_name}: %{y}원<extra></extra>`,
            xaxis: 'x',
            yaxis: 'y'
          })
        });
      }

      if (chartSelected.techMain.includes('envelope')) {
        data.push({
          name:'앤밸로프(20,6)',
          x:srcDate,
          y:srcEnvelope.upper,
          type: 'scatter',
          mode: 'lines',
          legendgroup:'envelope',
          showlegend: true,
          line: {
            color: 'grey',
            dash:'dash'
          },
          hovertemplate: '상단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
        data.push({
          name:'',
          x:srcDate,
          y:srcEnvelope.lower,
          type: 'scatter',
          mode: 'lines',
          legendgroup:'envelope',
          showlegend: false,
          line: {
            color: 'grey',
            dash:'dash'
          },
          hovertemplate: '하단: %{y}원<extra></extra>',
          xaxis: 'x',
          yaxis: 'y'
        });
      }

      if (chartSelected.techMain.includes('trend')) {
        Object.entries(srcTrend).forEach(([key, _data]) => {
          var _name = `${key} 추세`;
          data.push({
            name:_name,
            x:_data.x,
            y:_data.y,
            type: 'scatter',
            mode: 'lines',
            line: {
              color:'black',
              dash:'dashdot',
              width: 1,
            },
            showlegend: true,
            visible: (key === '6개월') ? true: 'legendonly',
            hovertemplate: `${_name}: %{y}원<extra></extra>`,
            xaxis: 'x',
            yaxis: 'y'
          })
        });
      }

      if (chartSelected.techSupp.includes('volume')) {
        data.push({
          name:"거래량",
          x: srcDate,
          y: srcOhlcv.volume,
          type: 'bar',
          showlegend: false,
          marker: {color:'lightgrey'},
          xaxis: 'x2',
          yaxis: 'y2'
        });
      }

      if (chartSelected.techSupp.includes('macd')) {
        var axisN = 2;
        if (chartSelected.techSupp.includes('volume')) {
          axisN = 3;
        }

        data.push({
          name:"MACD",
          x: srcDate,
          y: srcMacd.macd,
          showlegend: false,
          type: 'scatter',
          mode: 'lines',
          line: {
            color:'royalblue',
            dash:'solid',
            width: 1,
          },
          hovertemplate: 'MACD: %{y}<extra></extra>',
          xaxis: `x${axisN}`,
          yaxis: `y${axisN}`
        });
        data.push({
          name:"Signal",
          x: srcDate,
          y: srcMacd.signal,
          showlegend: false,
          type: 'scatter',
          mode: 'lines',
          line: {
            color:'red',
            dash:'dash',
            width: 1,
          },
          hovertemplate: 'Signal: %{y}<extra></extra>',
          xaxis: `x${axisN}`,
          yaxis: `y${axisN}`
        });
        data.push({
          name:"Diff",
          x: srcDate,
          y: srcMacd.diff,
          type: 'bar',
          showlegend: false,
          marker: {color:srcMacd.diff.map(v => v < 0 ? '#1861A8':'#C92A2A' )},
          hovertemplate: 'Signal: %{y}<extra></extra>',
          xaxis: `x${axisN}`,
          yaxis: `y${axisN}`
        });
      }

      if (chartSelected.techSupp.includes('rsi')) {
        var axisN = 2;
        if (chartSelected.techSupp.includes('volume')) {
          axisN = 3;
          if (chartSelected.techSupp.includes('macd')) {
            axisN = 4;
          }
        } else {
          if (chartSelected.techSupp.includes('macd')) {
            axisN = 3;
          }
        }
        
        data.push({
          name:"RSI",
          x: srcDate,
          y: srcRsi.rsi,
          showlegend: false,
          type: 'scatter',
          mode: 'lines',
          line: {
            color:'royalblue',
            dash:'solid',
            width: 1,
          },
          hovertemplate: 'RSI: %{y}%<extra></extra>',
          xaxis: `x${axisN}`,
          yaxis: `y${axisN}`
        });
      }
      
      if (chartSelected.techSupp.length) {
        layout.xaxis.showticklabels = false;
        for (var n=1; n<=chartSelected.techSupp.length; n++){
          layout[`xaxis${n+1}`] = {
            type:'category',
            categorygap: 0.1,
            matches: 'x',
            showline: true,
            showticklabels: n === chartSelected.techSupp.length,
            tickfont: defaultLayout.font,
            tickformat: "%Y/%m/%d",
            tickangle:0,
            nticks: __media__.isMobile ? 4 : 6,
            anchor: `y${n+1}`,
          };
          layout[`yaxis${n+1}`] = {
            autorange: false,
            range: [0, 1],
            anchor: `x${n+1}`,
            showticklabels: ((n==1) && chartSelected.techSupp.includes('volume')) ? false : true,
            tickfont: defaultLayout.font,
          }
        }

        if (chartSelected.techSupp.length === 1) {
          if (chartSelected.techSupp.includes('volume')) {
            layout.yaxis.domain = [0.12, 1];
            layout.yaxis2.domain = [0, 0.1];
          } else {
            layout.yaxis.domain = [0.27, 1];
            layout.yaxis2.domain = [0, 0.25];
          }
        } else if (chartSelected.techSupp.length === 2) {
          if (chartSelected.techSupp.includes('volume')) {
            layout.yaxis.domain = [0.39, 1];
            layout.yaxis2.domain = [0.27, 0.37];
            layout.yaxis3.domain = [0, 0.25];
          } else {
            layout.yaxis.domain = [0.44, 1];
            layout.yaxis2.domain = [0.22, 0.42];
            layout.yaxis3.domain = [0, 0.2];
          }
        } else if (chartSelected.techSupp.length === 3) {
          if (chartSelected.techSupp.includes('volume')) {
            layout.yaxis.domain = [0.43, 1];
            layout.yaxis2.domain = [0.32, 0.42];
            layout.yaxis3.domain = [0.16, 0.31];
            layout.yaxis4.domain = [0, 0.15];
          } else {
            layout.yaxis.domain = [0.51, 1];
            layout.yaxis2.domain = [0.34, 0.5];
            layout.yaxis3.domain = [0.17, 0.33];
            layout.yaxis4.domain = [0, 0.16];
          }
        }    
      }

      calcYrange(data, layout);
      Plotly.newPlot('plotly', data, layout, option);
    } else {
      const $chart = $('#plotly');
      const chart = LightweightCharts.createChart($chart[0], {
        width: $chart.width(),
        height: $chart.height(),
        layout: {
          background: {color: '#fff'},
          textColor: '#000',
        },
        rightPriceScale: {
          mode: LightweightCharts.PriceScaleMode.Normal,
          autoScale: true,
          autoScaleOnScroll: true,
          entireTextOnly: true,
        },
        handleScale: {
          axisPressedMouseMove: false,
          mouseWheel: true,
          pinch: true
        },
        localization: {
          priceFormatter: price => Math.round(price).toString(),
          timeFormatter: businessDay => {
            if (typeof businessDay === 'string') {
              return businessDay;
            }
            if (typeof businessDay === 'object' && businessDay !== null) {
              const y = businessDay.year;
              const m = String(businessDay.month).padStart(2, '0');
              const d = String(businessDay.day).padStart(2, '0');
              return `${y}-${m}-${d}`;
            }
            return '';
          },
        },
        grid: {
          vertLines: { color: '#eee' },
          horzLines: { color: '#eee' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        }
      });
      const candleSeries = chart.addCandlestickSeries({
        upColor: '#C92A2A',
        downColor: '#1861A8',
        borderUpColor: '#C92A2A',
        borderDownColor: '#1861A8',
        wickUpColor: '#C92A2A',
        wickDownColor: '#1861A8',
      });
      candleSeries.setData(srcDate.map((date, n) => ({time:date, open:srcOhlcv.open[n], high:srcOhlcv.high[n], low:srcOhlcv.low[n], close:srcOhlcv.close[n]})));

      if (chartSelected.techMain.includes('sma')) {
        Object.entries(srcSma).forEach(([key, obj]) => {
          const sma = chart.addLineSeries({
            color: {
              'sma5': '#FF6B6B',
              'sma20': '#FFD43B',
              'sma60': '#4DABF7',
              'sma120': '#69DB7C',
              'sma200': '#845EF7'}[key],
            lineWidth: 1.0,
            lastValueVisible: false,
          });
          sma.setData(srcDate.map((date, n) => ({time:date, value:obj[n]})));
        });
      }

      if (chartSelected.techMain.includes('bollingerx2')) {
        const b2upper = chart.addLineSeries({
          color: 'brown',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        const b2lower = chart.addLineSeries({
          color: 'brown',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        b2upper.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.upper[n]})));
        b2lower.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.lower[n]})));

        if (!chartSelected.techMain.includes('bollingerx1')) {
          const bmiddle = chart.addLineSeries({
            color: 'black',
            lineWidth: 1.0,
            lastValueVisible: false,
          });
          bmiddle.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.middle[n]})));
        }
      }

      if (chartSelected.techMain.includes('bollingerx1')) {
        const b1upper = chart.addLineSeries({
          color: 'brown',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        const b1lower = chart.addLineSeries({
          color: 'brown',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        b1upper.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.upperTrend[n]})));
        b1lower.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.lowerTrend[n]})));

        if (!chartSelected.techMain.includes('bollingerx2')) {
          const bmiddle = chart.addLineSeries({
            color: 'black',
            lineWidth: 1.0,
            lastValueVisible: false,
          });
          bmiddle.setData(srcDate.map((date, n) => ({time:date, value:srcBollinger.middle[n]})));
        }
      }

      if (chartSelected.techMain.includes('envelope')) {
        const e_upper = chart.addLineSeries({
          color: '#808080',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        const e_lower = chart.addLineSeries({
          color: '#808080',
          lineWidth: 1.2,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible: false,
        });
        e_upper.setData(srcDate.map((date, n) => ({time:date, value:srcEnvelope.upper[n]})));
        e_lower.setData(srcDate.map((date, n) => ({time:date, value:srcEnvelope.lower[n]})));
      }

      if (chartSelected.techMain.includes('trend')) {
          const trend = chart.addLineSeries({
            color: 'black',
            lineWidth: 1.0,
            lineStyle: LightweightCharts.LineStyle.Dashed,
            lastValueVisible: false,
          });
          trend.setData(srcTrend['6개월'].x.map((x, n) => ({time:x, value:srcTrend['6개월'].y[n]})));
        // Object.entries(srcTrend).forEach(([key, obj]) => {
        //   const trend = chart.addLineSeries({
        //     color: 'black',
        //     lineWidth: 1.0,
        //     lineStyle: LightweightCharts.LineStyle.Dashed,
        //     lastValueVisible: false,
        //   });
        //   trend.setData(obj.x.map((x, n) => ({time:x, value:obj.y[n]})));
        // });
      }

      
    }
  };

  setDeviationChart = function() {
    let layout = {
      margin:{
        l:__media__.isMobile ? 20:40, 
        r:10, 
        t:10, 
        b:20
      }, 
      grid: { 
        rows: __media__.isMobile ? 3:2, 
        columns: __media__.isMobile ? 2:3, 
        pattern: 'independent',
      },
      dragmode: 'zoom',
      hovermode: 'x unified'
    }
    const option = {
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false
    };

    var data = [];
    Object.entries(srcDeviation).forEach(([label, obj], n) => {
      if (obj.isempty){
        return
      }
      
      data.push({
        type:'bar',
        name:label,
        x:obj.date,
        y:obj.data,
        showlegend:false,
        visible:true,
        marker: {color:obj.data.map(v => v < 0 ? '#1861A8':'#C92A2A' )},
        xaxis:`x${n === 0 ? '' : n + 1}`,
        yaxis:`y${n === 0 ? '' : n + 1}`,
        hovertemplate: `%{y:.2f}%<extra>${label}</extra>`
      })
      layout[`xaxis${n === 0 ? '' : n + 1}`] = {
        anchor: `y${n === 0 ? '' : n + 1}`,
        fixedrange: true,
        tickfont: defaultLayout.font,
        tickformat:'%Y/%m/%d',
        tickangle:0,
        nticks: __media__.isMobile? 3 : 4,
        showline: true,
      }
      layout[`yaxis${n === 0 ? '' : n + 1}`] = {
        anchor: `x${n === 0 ? '' : n + 1}`,
        tickfont: defaultLayout.font,
        fixedrange:true,
        domain: n < 3 ? [0.52, 1] : [0, 0.48],
        showline: true,
      }
      if (__media__.isMobile) {
        if (n <= 1) {
          layout[`yaxis${n === 0 ? '' : n + 1}`].domain = [0.7, 1.0];
        } else if (n <= 3){
          layout[`yaxis${n === 0 ? '' : n + 1}`].domain = [0.35, 0.65];
        } else {
          layout[`yaxis${n === 0 ? '' : n + 1}`].domain = [0, 0.30];
        }
        
      }
    });

    Plotly.newPlot('plotly', data, layout, option)
  };

  setSalesChart = function(period) {
    let src = (period === 'sales-q') ? srcSalesQ : srcSalesY;
    const layout = {
      margin:{
        l:__media__.isMobile ? 50:70, 
        r:__media__.isMobile ? 30:50, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      doubleClick: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      barmode: 'group',
      xaxis: {
        tickangle: 0,
        tickfont: defaultLayout.font,
      },
      yaxis: {
        autorange: true,
        title: {
          text: '[억원]',
          font: defaultLayout.font
        },
        tickformat: ',',
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
      yaxis2: {
        autorange: true,
        title: {
          text: '영업이익률[%]',
          font: defaultLayout.font
        },
        overlaying: 'y',
        side: 'right',
        tickfont: defaultLayout.font,
        showgrid: false,
        zeroline: false,
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const revenue = {
      x: src.index,
      y: src.sales,
      name: src.salesLabel,
      text: src.salesText,
      type: 'bar',
      marker: { color: '#2ca02c', opacity:0.8 },
      hovertemplate: `${src.salesLabel}: %{text}원<extra></extra>`
    };

    const opIncome = {
      x: src.index,
      y: src.profit,
      name: src.profitLabel,
      text: src.profitText,
      type: 'bar',
      marker: { color: '#ff7f0e', opacity:0.8 },
      hovertemplate: `${src.profitLabel}: %{text}원<extra></extra>`
    };

    const netIncome = {
      x: src.index,
      y: src.netProfit,
      name: src.netProfitLabel,
      text: src.netProfitText,
      type: 'bar',
      marker: { color: '#d62728', opacity:0.8 },
      hovertemplate: `${src.netProfitLabel}: %{text}원<extra></extra>`
    };

    const opMargin = {
      x: src.index,
      y: src.profitRate,
      name: '영업이익률(%)',
      yaxis: 'y2',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#d62728', width: 3 },
      marker: { size: 8, opacity:0.7 },
      hovertemplate: '영업이익율(%): %{y}%<extra></extra>'
    };

    let data = [revenue, opIncome, netIncome, opMargin];
    if ("marketcap" in src){
      const cap = {
        x: src.index,
        y: src.marketcap,
        name: src.marketcapLabel,
        text: src.marketcapText,
        visible: (period === 'sales-q') ? 'legendonly' : true,
        type: 'bar',
        marker: { color: '#1f77b4', opacity:0.8 },
        hovertemplate: `${src.marketcapLabel}: %{text}원<extra></extra>`
      };
      data.unshift(cap);
    }
    Plotly.newPlot('plotly', data, layout, option)
  };


  setAssetChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 50:70, 
        r:__media__.isMobile ? 30:50, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      barmode: 'stack',
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: false,
        range:[0, 1.2 * Math.max(...srcAsset.asset)],
        title: {
          text: '[억원]',
          font: defaultLayout.font
        },
        tickformat: ',',
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
      yaxis2: {
        title: {
          text: '부채율[%]',
          font: defaultLayout.font
        },
        autorange: false,
        range:[0.8 * Math.min(...srcAsset.debtRatio), 1.2 * Math.max(...srcAsset.debtRatio)],
        overlaying: 'y',
        side: 'right',
        showgrid: false,
        zeroline: false,
        tickfont: defaultLayout.font,
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const asset = {
      x: srcAsset.index,
      y: srcAsset.asset,
      name: "자산총액",
      text: srcAsset.assetText,
      textposition: 'top center',
      texttemplate: '%{text}원',
      textfont: defaultLayout.font,
      showlegend: false,
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        opacity:0.0
      },
      hovertemplate: '자산총액: %{text}원<extra></extra>'
    };

    const capital = {
      x: srcAsset.index,
      y: srcAsset.capital,
      name: '자본총액',
      text: srcAsset.capitalText,
      textfont: defaultLayout.font,
      type: 'bar',
      marker: { color: '#2ca02c', opacity:0.8 },
      hovertemplate: '자본총액: %{text}원<extra></extra>'
    };

    const debt = {
      x: srcAsset.index,
      y: srcAsset.debt,
      name: '부채총액',
      text: srcAsset.debtText,
      textfont: defaultLayout.font,
      type: 'bar',
      marker: { color: '#d62728', opacity:0.8 },
      hovertemplate: '부채총액: %{text}원<extra></extra>'
    };

    const debtRatio = {
      x: srcAsset.index,
      y: srcAsset.debtRatio,
      name: '부채율(%)',
      yaxis: 'y2',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#d62728', width: 3},
      marker: { size: 8, opacity:0.7 },
      hovertemplate: '부채율(%): %{y}%<extra></extra>'
    };

    let data = [asset, capital, debt, debtRatio];
    Plotly.newPlot('plotly', data, layout, option);
  };

  setGrowthChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 30:50, 
        r:10, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: true,
        title: {
          text: '[%]',
          font: defaultLayout.font
        },
        tickformat: ',',
        tickfont: defaultLayout.font,
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const revenue = {
      x: srcGrowth.date,
      y: srcGrowth.revenue,
      name: `${srcSalesY.salesLabel}성장률`,
      textposition: 'top center',
      texttemplate: '%{y:.2f}%',
      textfont: defaultLayout.font,
      showlegend: true,
      mode: 'lines+markers+text',
      type: 'scatter',
      hovertemplate: `${srcSalesY.salesLabel}성장률: %{y:.2f}%<extra></extra>`
    };

    const profit = {
      x: srcGrowth.date,
      y: srcGrowth.profit,
      name: '영업이익성장률',
      textposition: 'top center',
      texttemplate: '%{y:.2f}%',
      textfont: defaultLayout.font,
      showlegend: true,
      mode: 'lines+markers+text',
      type: 'scatter',
      hovertemplate: '영업이익성장률: %{y:.2f}%<extra></extra>'
    };

    const eps = {
      x: srcGrowth.date,
      y: srcGrowth.eps,
      name: 'EPS성장률',
      textposition: 'top center',
      texttemplate: '%{y:.2f}%',
      textfont: defaultLayout.font,
      showlegend: true,
      mode: 'lines+markers+text',
      type: 'scatter',
      hovertemplate: 'EPS성장률: %{y:.2f}%<extra></extra>'
    };

    let data = [revenue, profit, eps];
    Plotly.newPlot('plotly', data, layout, option);
  };

  setProductChart = function() {
    const layout = {
      margin: {
        t:10,
        r:40,
        l:40,
        b:10
      },
      dragmode: false,    
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
    }
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    const data = [{
      type: 'pie',
      labels: srcProduct.label,
      values: srcProduct.value,
      textinfo: 'label+percent',
      textfont: defaultLayout.font,
      insidetextorientation: 'radial',
      marker: {
        opacity: 0.8
      },
      hoverinfo:'skip'
    }];
    Plotly.newPlot('plotly', data, layout, option);
  };

  setDivChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 30:50, 
        r:__media__.isMobile ? 40:60, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: false,
        range:[0, 1.2 * Math.max(...srcDiv.div)],
        title: {
          text: '배당수익률[%]',
          font: defaultLayout.font
        },
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
      yaxis2: {
        title: {
          text: 'DPS[원]',
          font: defaultLayout.font
        },
        autorange: false,
        range:[0, 1.2 * Math.max(...srcDiv.dps)],
        overlaying: 'y',
        side: 'right',
        showgrid: false,
        zeroline: false,
        showticklabels: true,
        tickformat: ',',
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const div = {
      x: srcDiv.x,
      y: srcDiv.div,
      name: '배당수익률',
      textposition: 'inside',
      texttemplate: '%{y}%',
      textfont: defaultLayout.font,
      showlegend: true,
      meta:srcDiv.meta,
      type: 'bar',
      yaxis: 'y1',
      marker: { color:'lightgreen', opacity:0.8 },
      hovertemplate: '%{meta}<extra></extra>'
    };

    const dps = {
      x: srcDiv.x,
      y: srcDiv.dps,
      name: 'DPS(원)',
      yaxis: 'y2',
      textposition: 'top center',
      texttemplate: '%{y:,d}원',
      textfont: defaultLayout.font,
      showlegend: true,
      mode: 'lines+markers+text',
      type: 'scatter',
      marker: {opacity: 0.7},
      hovertemplate: 'DPS: %{y:,d}원<extra></extra>'
    };

    Plotly.newPlot('plotly', [div, dps], layout, option)
  };

  setPbrChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 30:50, 
        r:__media__.isMobile ? 40:60, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: false,
        range:[0, 1.2 * Math.max(...srcPb.pbr)],
        title: {
          text: 'PBR[-]',
          font: defaultLayout.font
        },
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
      yaxis2: {
        title: {
          text: 'BPS[원]',
          font: defaultLayout.font
        },
        autorange: false,
        range:[0, 1.2 * Math.max(...srcPb.bps)],
        overlaying: 'y',
        side: 'right',
        showgrid: false,
        zeroline: false,
        showticklabels: true,
        tickformat: ',',
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const pbr = {
      x: srcPb.x,
      y: srcPb.pbr,
      name: 'PBR',
      textposition: 'inside',
      texttemplate: '%{y:.2f}',
      textfont: defaultLayout.font,
      showlegend: true,
      type: 'bar',
      yaxis: 'y1',
      marker: { color:'lightpink', opacity:0.8 },
      hovertemplate: 'PBR: %{y:.2f}<extra></extra>'
    };

    const bps = {
      x: srcPb.x,
      y: srcPb.bps,
      name: 'BPS(원)',
      yaxis: 'y2',
      textposition: 'top center',
      texttemplate: '%{y:,d}원',
      textfont: defaultLayout.font,
      showlegend: true,
      mode: 'lines+markers+text',
      type: 'scatter',
      marker: {opacity: 0.7},
      hovertemplate: 'BPS: %{y:,d}원<extra></extra>'
    };

    Plotly.newPlot('plotly', [bps, pbr], layout, option)
  };

  setPerChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 20:30, 
        r:20, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: false,
        range:[0, 1.1 * Math.max(...srcPe.y)],
        title: {
          font: defaultLayout.font
        },
        tickformat: ',',
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const pe = {
      x: srcPe.x,
      y: srcPe.y,
      name: '',
      text: srcPe.text,
      textposition: 'outside',
      texttemplate: '%{text}',
      textfont: defaultLayout.font,
      meta: srcPe.meta,
      showlegend: false,
      type: 'bar',
      marker: { color:'skyblue', opacity:0.8 },
      hovertemplate: '%{meta}<extra></extra>'
    };

    Plotly.newPlot('plotly', [pe], layout, option)
  };

  setPerBandChart = function() {
    $('#plotly').empty();
    if (!__media__.isMobile) {
      const layout = {
        margin:{
          l:__media__.isMobile ? 30:50, 
          r:10, 
          t:10, 
          b:20
        }, 
        dragmode: false,
        hovermode: 'x unified',      
        legend: {
          font: defaultLayout.font,
          bgcolor:'rgba(0,0,0,0)',
          borderwidth:0,
          itemclick:'toggle',
          itemdoubleclick:'toggleothers',
          orientation:'h',
          valign:'middle',
          xanchor:'left',
          x:0.0,
          yanchor:'top',
          y:1.02
        },
        xaxis: {
          tickfont: defaultLayout.font,
          tickangle: 0,
          hoverformat: '%Y-%m-%d'
        },
        yaxis: {
          autorange: true,
          title: {
            font: defaultLayout.font
          },
          tickformat: ',',
          tickfont: defaultLayout.font,
        },
      };
      const option = {
        doubleClick: false,
        doubleTap: false,
        showTips:false,
        responsive:true,
        displayModeBar:false,
        displaylogo:false,
        scrollZoom: false
      };
      let data = [];
      Object.entries(srcPerBand).forEach(([col, obj]) => {
        if (col === 'x'){
          return
        }
        data.push({
          name:col,
          x:srcPerBand.x,
          y:obj,
          visible:true,
          showlegend:false,
          type:'scatter',
          mode: 'lines',
          line:{
            dash: col === "종가" ? 'solid': 'dash'
          },
          hovertemplate: '%{y:.1f}원<extra></extra>'
        });
        if (col === "종가"){
          data.at(-1).line['color'] = 'black';
          data.at(-1).hovertemplate = '%{y:,d}원<extra></extra>';
        }
      });

      Plotly.newPlot('plotly', data, layout, option);
    } else {
      const $chart = $('#plotly');
      const chart = LightweightCharts.createChart($chart[0], {
        width: $chart.width(),
        height: $chart.height(),
        layout: {
          background: {color: '#fff'},
          textColor: '#000',
        },
        rightPriceScale: {
          mode: LightweightCharts.PriceScaleMode.Normal,
          autoScale: true,
          autoScaleOnScroll: true,
          entireTextOnly: true,
        },
        handleScale: {
          axisPressedMouseMove: false,
          mouseWheel: true,
          pinch: true
        },
        localization: {
          priceFormatter: price => Math.round(price).toString()
        },
        grid: {
          vertLines: { color: '#eee' },
          horzLines: { color: '#eee' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        }
      });

      const price = chart.addLineSeries({
        color:'black',
        lineWidth:1.2,
        lastValueVisible:true,
      });
      price.setData(
        srcPerBand.x
        .map((date, n) => ({time:date, value:srcPerBand['종가'][n]}))
        .filter(d => d.value !== null && d.value !== undefined)
      );
      
      Object.entries(srcPerBand).forEach(([col, obj]) => {
        if ((col === 'x') || (col === '종가')){
          return
        }
        const band = chart.addLineSeries({
          lineWidth:0.8,
          lineStyle: LightweightCharts.LineStyle.Dashed,
          lastValueVisible:false,
          priceLineVisible: false,
        })
        band.setData(srcPerBand.x.map((date, n) => ({time:date, value:srcPerBand[col][n]})));
      });

      chart.timeScale().setVisibleRange({
        from: srcPerBand.x[0],
        to: srcPerBand.x.at(-1)
      })
    }
  };

  setPegChart = function() {
    const layout = {
      margin:{
        l:__media__.isMobile ? 30:50, 
        r:__media__.isMobile ? 50:70, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: defaultLayout.font,
        tickangle: 0,
      },
      yaxis: {
        autorange: false,
        range:[0, 1.2 * Math.max(...srcPeg.peg)],
        title: {
          text: 'PEG[-]',
          font: defaultLayout.font
        },
        tickfont: defaultLayout.font,
        rangemode: 'tozero'
      },
      yaxis2: {
        autorange: false,
        range:[0.8 * Math.min(...srcPeg.close), 1.2 * Math.max(...srcPeg.close)],
        title: {
          text: '종가[원]',
          font: {
            family: __fonts__,
            size: __media__.isMobile ? 9: 12,
            color: 'royalblue'
          }
        },
        tickfont: {
          family: __fonts__,
          size: __media__.isMobile ? 9:12,
          color:'royalblue'
        },
        overlaying: 'y',
        side: 'right',
        showgrid: false,
        zeroline: false,
        showticklabels: true,
        tickformat: ',',
      },
      
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    const peg = {
      x: srcPeg.x,
      y: srcPeg.peg,
      name: 'PEG',
      text: srcPeg.text,
      textposition: 'outside',
      texttemplate: '%{text}',
      textfont: defaultLayout.font,
      showlegend: true,
      type: 'bar',
      yaxis: 'y1',
      marker: { color:'lightblue', opacity:0.8 },
      hoverinfo: 'skip'
      // hovertemplate: 'PBR: %{y:.2f}<extra></extra>'
    };

    const price = {
      x: srcPeg.x,
      y:srcPeg.close,
      name: '종가',
      textposition: 'bottom center',
      texttemplate: '%{y:,d}원',
      textfont: defaultLayout.font,
      type:'scatter',
      mode:'lines+markers+text',
      yaxis: 'y2',
      line: {
        color:'royalblue'
      },
      marker: {
        color:'royalblue'
      }
    }

    Plotly.newPlot('plotly', [peg, price], layout, option)
  };

  setForienRateChart = function() {
    $('#plotly').empty();
    const layout = {
      margin:{
        l:__media__.isMobile ? 30:50, 
        r:__media__.isMobile ? 20:40, 
        t:10, 
        b:20
      }, 
      dragmode: false,
      hovermode: 'x unified',      
      legend: {
        font: defaultLayout.font,
        bgcolor:'rgba(0,0,0,0)',
        borderwidth:0,
        itemclick:'toggle',
        itemdoubleclick:'toggleothers',
        orientation:'h',
        valign:'middle',
        xanchor:'left',
        x:0.0,
        yanchor:'top',
        y:1.02
      },
      xaxis: {
        tickfont: {
          size: __media__.isMobile ? 9 : 12,
          color: 'black',
          family: __fonts__
        },
        tickangle: 0,
        tickformat: '%Y-%m-%d',
      },
      yaxis: {
        title: {
          font: defaultLayout.font
        },
        autorange: true,
        tickformat: ',',
        tickfont: {
          size: __media__.isMobile ? 9 : 12,
          color: 'black',
          family: __fonts__
        },
      },
      yaxis2: {
        title: {
          font: defaultLayout.font
        },
        showgrid: false,
        overlaying: 'y',
        side: 'right',
        tickfont: {
          size: __media__.isMobile ? 9 : 12,
          color: 'royalblue',
          family: __fonts__
        },
      },
    };
    const option = {
      doubleClick: false,
      doubleTap: false,
      showTips:false,
      responsive:true,
      displayModeBar:false,
      displaylogo:false,
      scrollZoom: false
    };
    
    let data = [];
    Object.entries(srcForeignRate).forEach(([col, obj]) => {
      data.push({
        name:col,
        x:obj.x,
        y:obj['종가'],
        visible:col === '3M' ? true: 'legendonly',
        legendgroup: col,
        showlegend:true,
        type:'scatter',
        mode: 'lines',
        line:{
          color:'black',
          dash: 'solid'
        },
        yaxis: 'y1',
        hovertemplate: '종가: %{y:,d}원<extra></extra>'
      });
      data.push({
        name:'비중',
        x:obj.x,
        y:obj['비중'],
        visible:col === '3M' ? true: 'legendonly',
        legendgroup: col,
        showlegend:false,
        type:'scatter',
        mode: 'lines',
        line:{
          color:'royalblue',
          dash: 'solid'
        },
        yaxis: 'y2',
        hovertemplate: '비중: %{y:.2f}%<extra></extra>'
      });
    });
    layout.xaxis.tickfont.color = 'black';
    layout.yaxis.tickfont.color = 'black';    
    layout.yaxis2.tickfont.color = 'royalblue';
    Plotly.newPlot('plotly', data, layout, option);
  };


  $techOpt.on('select2:select', function(e){
    $('#plotly').empty();
    let _val = e.params.data.id;
    let _cls = e.params.data.element.dataset.class;
    if (_cls === "standalone"){
      $(this).val([_val]).trigger('change');
      if ((_val === "sales-y") || (_val === "sales-q")){
        setSalesChart(_val);
      } else if (_val === "asset") {
        setAssetChart();
      } else if (_val === "deviation") {
        setDeviationChart();
      } else if (_val === "pbrs") {
        setPbrChart();
      } else if (_val === "pers") {
        setPerChart();
      } else if (_val === "perband") {
        setPerBandChart();
      } else if (_val === "foreigners") {
        setForienRateChart();
      } else if (_val === "growth") {
        setGrowthChart();
      } else if (_val === "product") {
        setProductChart();
      } else if (_val === "div") {
        setDivChart();
      } else if (_val === "peg") {
        setPegChart();
      }

      chartSelected.standalone = [_val];
      chartSelected.techMain = [];
      chartSelected.techSupp = [];
      $(this).blur();
      $('.notice').click();
      return
    } 

    if (chartSelected.standalone.length) {
      $(this).val([_val]).trigger('change');
      chartSelected.standalone = [];
    }
    if (_cls === "main") {
      chartSelected.techMain.push(_val);
    } else if (_cls == "support") {
      chartSelected.techSupp.push(_val);
    }
    setTechnicalChart();
    $(this).blur();
    $('.notice').click();
    
  });

  $techOpt.on('select2:unselect', function(e){
    let _val = e.params.data.id;
    $('#plotly').empty();
    if (chartSelected.standalone.includes(_val)) {
      chartSelected.standalone = [];
      return;
    }
    if (chartSelected.techMain.includes(_val)){
      chartSelected.techMain = chartSelected.techMain.filter(item => item !== _val);
    }
    if (chartSelected.techSupp.includes(_val)) {
      chartSelected.techSupp = chartSelected.techSupp.filter(item => item !== _val);
    }
    setTechnicalChart();
    $(this).blur();
    $('.notice').click();
  });


  $('#plotly').on('plotly_relayout', function(e, ed){
    if (chartSelected.standalone.length) {
      return
    }
    
    if (ed['xaxis.range[0]'] && ed['xaxis.range[1]']) {
      xRangeN = [
        Math.round(Math.max(...[0, ed['xaxis.range[0]']])), 
        Math.round(Math.min(...[ed['xaxis.range[1]'], srcDate.length - 1]))
      ];

      calcYrange(e.currentTarget.data, e.currentTarget.layout);
      Object.entries(e.currentTarget.layout).forEach(([key, obj]) => {
        if (key.startsWith('yaxis')) {
          Plotly.relayout("plotly", {[`${key}.range`]: obj.range });
        }
      });
      
    }

  });

  setTechnicalOption();
  setTechnicalChart();
}
