"""
TITLE   : BUILD CACHE
AUTHOR  : SNOB
CONTACT : snob.labwons@gmail.com
ROUTINE : 21:00+09:00UTC on weekday
"""
if __name__ == "__main__":
    try:
        from ..common.path import PATH
        from ..common.report import eMail
        from ..fetch.market.group import MarketGroup
        from ..fetch.market.index import MarketIndex
        from ..fetch.market.spec import MarketSpec
        from .service.macro import Macro
    except ImportError:
        from src.common.path import PATH
        from src.common.report import eMail
        from src.fetch.market.group import MarketGroup
        from src.fetch.market.index import MarketIndex
        from src.fetch.market.spec import MarketSpec
        from src.build.service.macro import Macro
    from datetime import datetime
    import os

    LOCAL_HOST = os.getenv('LOCAL_HOST') is None
    ACTION_MODE = os.environ.get("GITHUB_EVENT_NAME", "local")

    context = ['DETAILS']
    prefix = []

    # try:
    #     group = MarketGroup(update=True)
    #     if not PATH.GROUP.startswith('http'):
    #         with open(PATH.GROUP, 'w') as f:
    #             f.write(group.to_json(orient='index').replace("nan", ""))
    #     prefix_group = "PARTIALLY FAILED" if "FAIL" in group.log else "SUCCESS"
    #     context += [f"- [{prefix_group}] MARKET GROUP: ", group.log, ""]
    # except Exception as report:
    #     prefix_group = 'FAILED'
    #     context += [f"- [{prefix_group}] MARKET GROUP: ", f'{report}', ""]
    # prefix.append(prefix_group)

    # try:
    #     index = MarketIndex(update=True)
    #     if not PATH.INDEX.startswith('http'):
    #         with open(PATH.INDEX, 'w') as f:
    #             f.write(index.to_json(orient='index').replace("nan", ""))
    #     prefix_index = "PARTIALLY FAILED" if "FAIL" in index.log else "SUCCESS"
    #     context += [f"- [{prefix_index}] MARKET INDEX: ", index.log, ""]
    # except Exception as report:
    #     prefix_index = "FAILED"
    #     context += [f"- [{prefix_index}] MARKET INDEX: ", f'{report}', ""]
    # prefix.append(prefix_index)


    try:
        macro = Macro(update=ACTION_MODE in ["schedule", "workflow_dispatch"])
        if not PATH.MACRO.startswith('http'):
            with open(PATH.MACRO, 'w') as f:
                f.write(macro.to_json(orient='index').replace('nan', ''))
        prefix_macro = 'SUCCESS'
        context += [f"- [{prefix_macro}] MACRO DATA: ", macro.log, ""]
    except Exception as report:
        prefix_macro = 'FAILED'
        context += [f"- [{prefix_macro}] MACRO DATA: ", f'{report}', ""]
    prefix.append(prefix_macro)

    try:
        spec = MarketSpec(update=ACTION_MODE == "schedule")
        if not PATH.SPEC.startswith('http'):
            with open(PATH.SPEC, 'w') as f:
                f.write(spec.to_json(orient='index').replace("nan", ""))
        prefix.append("PARTIALLY FAILED" if "FAIL" in spec.log else "SUCCESS")
        context += [f"- [{prefix[-1]}] MARKET SPECIFICATION: ", spec.log, ""]
    except Exception as report:
        prefix.append('FAILED')
        context += [f"- [{prefix[-1]}] MARKET SPECIFICATION: ", f'{report}', ""]

    if "PARTIALLY FAILED" in prefix:
        prefix = "PARTIALLY FAILED"
    elif "FAILED" in prefix:
        prefix = "FAILED"
    else:
        prefix = "SUCCESS"


    mail = eMail()
    mail.subject = f'[{prefix}] UPDATE BASELINE CACHE on {datetime.today().strftime("%Y/%m/%d")}'
    mail.context = "\n".join(context)
    if ACTION_MODE == "local":
        print(f'{mail.subject}\n{mail.context}\n')
    else:
        mail.send()
