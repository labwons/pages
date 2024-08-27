try:
    from .deploy.sitemap import updateSitemap, updateRSS
    from .treemap.generic import MarketMap    
    from .rank.generic import Rank
except ImportError:
    from __py__.deploy.sitemap import updateSitemap, updateRSS
    from __py__.treemap.generic import MarketMap    
    from __py__.rank.generic import Rank
import os


if __name__ == "__main__":
    
    
    bo, bc = "{", "}"
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/treemap/treemap.json"), mode="w") as file:
        file.write(f"""{bo}
{MarketMap(auto_update=True)    }
{bc}""")
        
    RANK = Rank()
    with open(os.path.join(os.path.dirname(__file__), r"../src/json/rank/rank.json"), mode="w") as file:
        file.write(f"""{bo}
{RANK}
{bc}""")
    updateSitemap()
    updateRSS()
    print("Success.")
