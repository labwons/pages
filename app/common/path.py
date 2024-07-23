import os


DIRAPP = os.path.dirname(os.path.dirname(__file__))
DIRMAP = os.path.join(os.path.dirname(DIRAPP), "map")
JSONWICS = os.path.join(DIRMAP, r"src/json/wics.json")
JSONWI26 = os.path.join(DIRMAP, r"src/json/wi26.json")