try:
    from .barmap.generic import MarketMap
except ImportError:
    from app.barmap.generic import MarketMap


if __name__ == "__main__":
    WICS = MarketMap('WICS', update_index=False, update_market=True)
    WI26 = MarketMap('WI26', update_index=False, update_market=False)
    bo, bc = "{", "}"
    with open(r"./barmap/archive/marketmap.json", mode="w") as file:
        file.write(f"""

""")
    
    
    # print(wics.join(market, how='left'))