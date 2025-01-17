import torch

from pfhedge.instruments import BrownianStock
from pfhedge.instruments import EuropeanOption
from pfhedge.instruments import LookbackOption
from pfhedge.nn import WhalleyWilmott


class TestWhalleyWilmott:
    def test_repr(self):
        liability = EuropeanOption(BrownianStock())
        m = WhalleyWilmott(liability)
        assert repr(m) == (
            "WhalleyWilmott(\n"
            "  (bs): BSEuropeanOption()\n"
            "  (clamp): Clamp()\n"
            ")"
        )

        liability = EuropeanOption(BrownianStock())
        m = WhalleyWilmott(liability, a=2)
        assert repr(m) == (
            "WhalleyWilmott(\n"
            "  a=2\n"
            "  (bs): BSEuropeanOption()\n"
            "  (clamp): Clamp()\n"
            ")"
        )

        liability = LookbackOption(BrownianStock())
        m = WhalleyWilmott(liability)
        assert repr(m) == (
            "WhalleyWilmott(\n"
            "  (bs): BSLookbackOption()\n"
            "  (clamp): Clamp()\n"
            ")"
        )

    def test_shape(self):
        torch.distributions.Distribution.set_default_validate_args(False)

        deriv = EuropeanOption(BrownianStock())
        m = WhalleyWilmott(deriv)

        N = 10
        H_in = len(m.features())
        M_1 = 11
        M_2 = 12

        x = torch.empty((N, H_in))
        assert m(x).size() == torch.Size((N, 1))

        x = torch.empty((N, M_1, H_in))
        assert m(x).size() == torch.Size((N, M_1, 1))

        x = torch.empty((N, M_1, M_2, H_in))
        assert m(x).size() == torch.Size((N, M_1, M_2, 1))
