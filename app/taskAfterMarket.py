try:
    from .barmap.generic import MarketMap
except ImportError:
    from app.barmap.generic import MarketMap
import os


if __name__ == "__main__":
    WICS = MarketMap('WICS', update_index=False, update_market=True)
    WI26 = MarketMap('WI26', update_index=False, update_market=False)
    
    bo, bc = "{", "}"
    with open(os.path.join(os.path.dirname(__file__), r"barmap/archive/marketmap.json"), mode="w") as file:
        file.write(f"""{bo}
    "WICSL": {WICS.largeCap.drop(columns=["kind"]).to_dict(orient='list')},
    "WI26L": {WI26.largeCap.drop(columns=["kind"]).to_dict(orient='list')},
    "WICSM": {WICS.midCap.drop(columns=["kind"]).to_dict(orient='list')},
    "WI26M": {WI26.midCap.drop(columns=["kind"]).to_dict(orient='list')},
{bc}""".replace("'", '"').replace("nan", '""'))
    
    
    # print(wics.join(market, how='left'))
