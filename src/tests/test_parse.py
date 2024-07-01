from djamago import *


def test_parse():
    try:
        Pattern()
    except Exception:
        pass
    else:
        raise Exception()
    RegEx("ama")
    Expression.register("ama", [(10, "ama")])
    Expression.parse('ama:3(name, "am", "am":3, "kd", ama("dkd"))')
