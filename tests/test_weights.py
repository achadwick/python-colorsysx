"""Test colorsysx.weights"""

# Imports::

import colorsysx

from pytest import approx


# Test funcs::

def test_comp_weights():
    weights = (
        colorsysx.weights.RGBWeights.REC601,
        colorsysx.weights.RGBWeights.REC709,
        colorsysx.weights.RGBWeights.REC2020,
    )
    for w in weights:
        assert len(w) == 3
        assert sum(w) == approx(1)


def test_sorted_comp_weights():
    weights = (
        colorsysx.weights.SortedWeights.HSI,
        colorsysx.weights.SortedWeights.HSV,
        colorsysx.weights.SortedWeights.HLS,
    )
    for w in weights:
        assert len(w) == 3
        assert sum(w) == approx(1)
