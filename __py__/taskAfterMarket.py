try:
    from .treemap.generic import MarketMap
    from .market.generic import Market
except ImportError:
    from __py__.treemap.generic import MarketMap
    from __py__.market.generic import Market
import os


if __name__ == "__main__":
    DATA = Market(auto_update=True)
    WICS = MarketMap('WICS', DATA)
    WI26 = MarketMap('WI26', DATA)
    
    
    bo, bc = "{", "}"
    with open(os.path.join(os.path.dirname(__file__), r"../json/treemap/treemap.json"), mode="w") as file:
        file.write(f"""{bo}
    "WICSL": {
        WICS.largeCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "WI26L": {
        WI26.largeCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "WICSM": {
        WICS.midCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "WI26M": {
        WI26.midCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "SEC": {
        WICS.largeCap[WICS.largeCap["kind"] == "sector"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    },
    "IND": {
        WI26.largeCap[WI26.largeCap["kind"] == "industry"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    }
{bc}""".replace("'", '"').replace("nan", '""'))
    
    
    print("Success.")
