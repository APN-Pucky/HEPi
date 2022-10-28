from enum import IntEnum
class Order(IntEnum):
    """
    Computation orders.
    """
    LO = 0
    """Leading Order"""
    NLO = 1
    """Next-to-Leading Order"""
    NLO_PLUS_NLL = 2
    """Next-to-Leading Order plus Next-to-Leading Logarithms"""
    aNNLO_PLUS_NNLL = 3
    """Approximate Next-to-next-to-Leading Order plus Next-to-next-to-Leading Logarithms"""



def replace_macros(s: str) -> str:
    return s.replace("_PLUS_", "+").replace(" ", "\\ ")



def xsec_to_order(s: str):
    if s == "NNLOapprox+NNLL":
        return Order.aNNLO_PLUS_NNLL
    elif s == "NLO+NLL":
        return Order.NLO_PLUS_NLL
    elif s == "NLO":
        return Order.NLO
    elif s == "LO":
        return Order.LO
    else:
        raise ValueError("Unknown Order '" + s + "', not supported by HEPi.")

def order_to_string(o: Order, json_style=False, no_macros=False) -> str:
    ret = ""
    if o == Order.LO:
        ret = "LO"
    elif o == Order.NLO:
        ret = "NLO"
    elif o == Order.NLO_PLUS_NLL:
        ret = "NLO_PLUS_NLL"
    elif o == Order.aNNLO_PLUS_NNLL:
        if json_style:
            ret = "NNLOapprox+NNLL"
        else:
            ret = "aNNLO_PLUS_NNLL"
    else:
        raise ValueError("Order '" + o + "' not supported by HEPi.")
    if no_macros:
        return replace_macros(ret)
    return ret