try:
    from .deploy.sitemap import updateSitemap, updateRSS
    from .treemap.generic import MarketMap    
    from .rank.generic import Rank
except ImportError:
    from __py__.deploy.sitemap import updateSitemap, updateRSS
    from __py__.treemap.generic import MarketMap    
    from __py__.rank.generic import Rank
import os, json


if __name__ == "__main__":
    
    treemap = json.dumps(json.loads("{" + str(MarketMap(True)) + "}"), separators=(',', ':'))
    ranking = json.dumps(json.loads("{" + str(Rank()) + "}"), separators=(',', ':'))
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/treemap/treemap.json"), mode="w") as file:
        file.write(treemap)
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/rank/rank.json"), mode="w") as file:
        file.write(ranking)
    
#     bo, bc = "{", "}"
#     with open(os.path.join(os.path.dirname(__file__), r"../src/json/treemap/treemap.json"), mode="w") as file:
#         file.write(f"""{bo}
# {MarketMap(auto_update=True)}
# {bc}""")
        
#     with open(os.path.join(os.path.dirname(__file__), r"../src/json/rank/rank.json"), mode="w") as file:
#         file.write(f"""{bo}
# {Rank()}
# {bc}""")


    updateSitemap()
    updateRSS()
    print("Success.")
