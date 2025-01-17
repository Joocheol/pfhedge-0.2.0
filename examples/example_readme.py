import sys

sys.path.append("..")


def print_as_comment(obj):
    print("\n".join(f"# {line}" for line in str(obj).splitlines()))


if __name__ == "__main__":
    import torch

    torch.manual_seed(42)

    # --- Prepare instruments

    from pfhedge.instruments import BrownianStock
    from pfhedge.instruments import EuropeanOption

    stock = BrownianStock(cost=1e-4)
    deriv = EuropeanOption(stock)

    print(">>> stock")
    print_as_comment(stock)
    print(">>> deriv")
    print_as_comment(deriv)

    # --- Fit and price

    from pfhedge import Hedger
    from pfhedge.nn import MultiLayerPerceptron

    model = MultiLayerPerceptron()
    hedger = Hedger(model, ["log_moneyness", "expiry_time", "volatility", "prev_hedge"])
    hedger

    print(">>> hedger")
    print_as_comment(hedger)

    hedger.fit(deriv)
    price = hedger.price(deriv)

    print(">>> price")
    print_as_comment(price)

    # --- Black-Scholes and Whalley-Wilmott

    from pfhedge.nn import BlackScholes
    from pfhedge.nn import WhalleyWilmott

    deriv = EuropeanOption(BrownianStock(cost=1e-4))

    model = BlackScholes(deriv)
    hedger_bs = Hedger(model, model.features())
    hedger_bs
    print(">>> hedger_bs")
    print_as_comment(hedger_bs)

    model = WhalleyWilmott(deriv)
    hedger_ww = Hedger(model, model.features())
    hedger_ww
    print(">>> hedger_ww")
    print_as_comment(hedger_ww)

    price_bs = hedger_bs.price(deriv)
    price_ww = hedger_ww.price(deriv)

    print(">>> price_bs")
    print_as_comment(price_bs)
    print(">>> price_ww")
    print_as_comment(price_ww)
