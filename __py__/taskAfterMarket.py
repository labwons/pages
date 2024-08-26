try:
    from .treemap.generic import MarketMap
except ImportError:
    from __py__.treemap.generic import MarketMap
import os


if __name__ == "__main__":
    
    MMAP = MarketMap(auto_update=True)    
    
    bo, bc = "{", "}"
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/treemap/treemap.json"), mode="w") as file:
        file.write(f"""{bo}
    "LargeCap": {
        MMAP.largeCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "LargeCapWithoutSamsung" : {
        MMAP.largeCapSamsungExcluded.drop(columns=["kind"]).to_dict(orient='list')
    },
    "MidCap": {
        MMAP.midCap.drop(columns=["kind"]).to_dict(orient='list')
    },
    "Sectors": {
        MMAP.largeCap[MMAP.largeCap["kind"] == "sector"].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    },
    "Industries": {
        MMAP.largeCap[(MMAP.largeCap["kind"] == "industry") | (MMAP.largeCap["name"].isin(['에너지', '유틸리티']))].drop(columns=["cover", "kind", "size"]).to_dict(orient='list')
    }
{bc}""".replace("'", '"').replace("nan", '""'))
    
    
    print("Success.")
