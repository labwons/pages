import os


class PATH:
    try:
        ROOT = os.path.dirname(__file__)
        while not ROOT.endswith('pages'):
            ROOT = os.path.dirname(ROOT)
    except NameError:
        ROOT = 'https://raw.githubusercontent.com/labwons/pages/main/'

    GROUP  = os.path.join(ROOT, r'dev/json/group/group.json')
    STATE  = os.path.join(ROOT, r'dev/json/group/state.json')
    PRICE  = os.path.join(ROOT, r'dev/json/group/price.json')
    SPECS  = os.path.join(ROOT, r'dev/json/group/specs.json')
    INDEX  = os.path.join(ROOT, r'dev/json/macro/index.json')
    BUBBLE = os.path.join(ROOT, r'dev/json/service/bubble.json')
    TRMAP  = os.path.join(ROOT, r'dev/json/service/treemap.json')
    MACRO  = os.path.join(ROOT, r'dev/json/service/macro.json')

    DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    DOWNLOADS = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    


if __name__ == "__main__":
    print(PATH.ROOT)
    print(PATH.GROUP)
    print(PATH.STATE)
    print(PATH.PRICE)
    print(PATH.SPECS)
    print(PATH.INDEX)
    print(PATH.TRMAP)