try:
    from .treemap.generic import MarketMap
    from .market.generic import Market
except ImportError:
    from __py__.treemap.generic import MarketMap
    from __py__.market.generic import Market
import os


if __name__ == "__main__":
    DATA = Market(auto_update=True)
    MMAP = MarketMap('WI26', DATA)
    
    
    bo, bc = "{", "}"
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/treemap/treemap.json"), mode="w") as file:
        file.write(f"""{bo}
    "LargeCap": {
        MMAP.largeCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "MidCap": {
        MMAP.midCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "Sectors": {
        MMAP.largeCap[MMAP.largeCap["kind"] == "sector"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    },
    "Industries": {
        MMAP.largeCap[MMAP.largeCap["kind"] == "industry"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    }
{bc}""".replace("'", '"').replace("nan", '""'))
    
    
    print("Success.")
