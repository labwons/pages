try:
    from ..technical.wrapper import TechnicalReporter
except ImportError:
    from dev.portfolio.technical.wrapper import TechnicalReporter
import pandas as pd
import json


class Report:
    ticker:str = ''

    @classmethod
    def dump(cls, data:dict) -> str:
        return json.dumps(data).replace("NaN", "null")

    def __init__(self, ticker:str, **kwargs):
        # data = krx(ticker=ticker, period=period).ohlcv
        data = pd.read_csv("https://raw.githubusercontent.com/kairess/stock_crypto_price_prediction/master/dataset/005930.KS_5y.csv") \
                 .set_index(keys="Date") \
                 .drop(columns=["Adj Close"])
        data.index = pd.to_datetime(data.index)
        self.tech = TechnicalReporter(data, to="js")
        self.ticker = ticker
        return
    
    def write(self):
        with open(r"C:\Users\Administrator\Desktop\report_copy.html", mode='w', encoding='utf-8') as file:
            file.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>LAB￦ONS :: 이름({self.ticker})</title>
	
	<!-- <script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script> --> 
    <script src="https://cdn.jsdelivr.net/gh/labwons/pages/src/js/plotly-0.1.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.1.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
        .dropdown {{
            position: relative;
            font-size: 14px;
            color: #333;
            
            .dropdown-list {{
                padding: 12px;
                background: #fff;
                position: absolute;
                top: 30px;
                left: 2px;
                right: 2px;
                box-shadow: 0 1px 2px 1px rgba(0, 0, 0, .15);
                transform-origin: 50% 0;
                transform: scale(1, 0);
                transition: transform .15s ease-in-out .15s;
                max-height: 66vh;
                overflow-y: scroll;
                z-index: 999;
            }}
            
            .dropdown-option {{
                display: block;
                padding: 8px 12px;
                opacity: 0;
                transition: opacity .15s ease-in-out;
            }}
            
            .dropdown-label {{
                display: block;
                height: 30px;
                background: #fff;
                border: 1px solid #ccc;
                padding: 6px 12px;
                line-height: 1;
                cursor: pointer;
                
                &:before {{
                    content: '▼';
                    float: right;
                }}
            }}
            
            &.on {{
                .dropdown-list {{
                    transform: scale(1, 1);
                    transition-delay: 0s;
                    
                    .dropdown-option {{
                        opacity: 1;
                        transition-delay: .2s;
                    }}
                }}
                    
                .dropdown-label:before {{
                    content: '▲';
                }}
            }}
            
            [type="checkbox"] {{
                position: relative;
                top: -1px;
                margin-right: 4px;
            }}
        }}
    </style>
</head>
<body>
    <header>

    </header>
    <main>
        <div class="service-app">
            <div class="service-nav">
                <div class="service-options">
                    <div class="dropdown" data-control="checkbox-dropdown">
                        <label class="dropdown-label">지표 선택</label>
                        <div class="dropdown-list">
                            <label><strong>상단 지표</strong></label>
                            <label class="dropdown-option">
                                <input type="checkbox" name="dropdown-group" value="sma" />
                                MA
                            </label>
                            <label class="dropdown-option">
                                <input type="checkbox" name="dropdown-group" value="bb" />
                                BB
                            </label>
                            <label class="dropdown-option">
                                <input type="checkbox" name="dropdown-group" value="trend" />
                                TREND
                            </label>
                            <label><strong>하단 지표</strong></label>
                            <label class="dropdown-option">
                                <input type="checkbox" name="dropdown-group" value="volume" checked/>
                                Volume
                            </label>
                            <label class="dropdown-option">
                                <input type="checkbox" name="dropdown-group" value="macd" />
                                CD
                            </label>   
                        </div>
                    </div>
                </div>
            </div>
            <div class="plotly" id="plotly"></div>
        </div>
        <div style="clear:both;"></div>
    </main>
    <footer>
        <!-- 하단 정보 -->
    </footer>
    <script>
{self.tech.const}
{self.tech.predef}        
        var option = {{
            displayModeBar:false,
            responsive:true,
            showTips:false
        }}
    </script>
    <script>
        (function($) {{
            var CheckboxDropdown = function(el) {{
                var _this = this;
                this.isOpen = false;
                this.$el = $(el);
                this.$label = this.$el.find('.dropdown-label');
                this.$inputs = this.$el.find('[type="checkbox"]');

                this.onCheckBox();

                this.$label.on('click', function(e) {{
                    e.preventDefault();
                    _this.toggleOpen();
                }});

                this.$inputs.on('change', function(e) {{
                    _this.onCheckBox();
                }});
            }};

            CheckboxDropdown.prototype.onCheckBox = function() {{
                this.updateStatus();
            }};

            CheckboxDropdown.prototype.updateStatus = function() {{
                var checked = this.$el.find(':checked');   
                var data = [ohlc];
                var grid = [['ohlc']];
                var currentY = 1;
                var layout = {{
                    margin: {{t:10, r:80, l:20, b:20}},
                    grid: {{
                        rows:1,
                        columns:1,
                        xaxes:['x'],
                    }},
                    hovermode: "x unified",
                    legend:{{
                        bgcolor: "white",
                        bordercolor: "#444",
                        borderwidth: 0,
                        groupclick: "togglegroup",
                        itemclick: "toggle",
                        itemdoubleclick: "toggleothers",
                        itemsizing: "trace",
                        itemwidth: 30,
                        orientation: "h",
                        tracegroupgap: 10,
                        traceorder: "normal",
                        valign: "middle",
                        xanchor: "right",
                        x: 1.0,
                        yanchor: "bottom",
                        y: 1.0,
                    }},
                    xaxis: {self.tech.xaxis()},
                    yaxis: {self.tech.yaxis()},
                }}
                
                for(var i = 0; i < checked.length; i++) {{
                    if (BELOW_INDICATORS.includes(checked[i].value)) {{
                        grid.push(checked[i].value);
                        if (grid.length > 4) {{
                            grid.pop();
                            alert("하단(보조) 지표는 최대 3개까지 가능합니다.");
                            return;
                        }}
                        layout[`yaxis${{grid.length}}`] = {self.tech.yaxis()};
                        if (checked[i].value == "volume") {{
                            layout[`yaxis${{grid.length}}`].tickformat = "";
                        }}
                    }} else {{
                        grid[0].push(checked[i].value);
                    }}
                    data.push(...VARIABLE_MAPPING[checked[i].value]);
                }}
                layout.grid.rows = grid.length;
                
                GRID_RATIO[layout.grid.rows].map((height, n) => {{
                    const start = currentY - height;
                    if (n == 0) {{
                        layout.yaxis.domain = [start, currentY];                
                    }} else {{
                        layout[`yaxis${{n + 1}}`].domain = [start, currentY];         
                    }}
                    currentY = start;
                }});
                Plotly.newPlot('plotly', data, layout, option);
                
            }};

            CheckboxDropdown.prototype.toggleOpen = function(forceOpen) {{
                var _this = this;

                if(!this.isOpen || forceOpen) {{
                    this.isOpen = true;
                    this.$el.addClass('on');
                    $(document).on('click', function(e) {{
                        if(!$(e.target).closest('[data-control]').length) {{
                            _this.toggleOpen();
                        }}
                    }});
                }} else {{
                    this.isOpen = false;
                    this.$el.removeClass('on');
                    $(document).off('click');
                }}
            }};

            var checkboxesDropdowns = document.querySelectorAll('[data-control="checkbox-dropdown"]');
            for(var i = 0, length = checkboxesDropdowns.length; i < length; i++) {{
                new CheckboxDropdown(checkboxesDropdowns[i]);
            }}
        }})(jQuery);
    </script>
</body>
</html>""")
        return
    
if __name__ == "__main__":
    rep = Report('005930')

    rep.write()