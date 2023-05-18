"""Test colorsysx.weights"""

# Imports::

from .context import colorsysx

from sys import float_info


# Module vars::

EPSILON = float_info.epsilon


# Test funcs::

def test_comp_weights():
    weights = (
        colorsysx.weights.ComponentWeights.REC601,
        colorsysx.weights.ComponentWeights.REC709,
        colorsysx.weights.ComponentWeights.REC2020,
    )
    for w in weights:
        assert len(w) == 3
        assert abs(1.0 - sum(w)) <= EPSILON
        wr, rg, wb = w
        assert abs(1.0 - (1.0*wr + 1.0*rg + 1.0*wb)) <= EPSILON


def test_sorted_comp_weights():
    weights = (
        colorsysx.weights.SortedComponentWeights.HSI,
        colorsysx.weights.SortedComponentWeights.HSV,
        colorsysx.weights.SortedComponentWeights.HLS,
    )
    for w in weights:
        assert len(w) == 3
        assert abs(1.0 - sum(w)) <= EPSILON
