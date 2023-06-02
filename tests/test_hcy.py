"""Tests for colorsysx.hcy"""

# Imports::

import colorsysx

from pytest import approx
import itertools


# Module vars::

WEIGHTS = (
    colorsysx.weights.RGBWeights.REC601,
    colorsysx.weights.RGBWeights.REC709,
    colorsysx.weights.RGBWeights.REC2020,
)


# Test funcs::

def test_grey_is_grey():
    """Neutral grey is always neutral grey."""
    for w in WEIGHTS:
        h, c, y = colorsysx.rgb_to_hcy(0.5, 0.5, 0.5, weights_rgb=w)
        assert y == approx(0.5)
        assert c == approx(0)
        assert h == approx(0)  # just a convention


def test_pure_components_match_weights():
    """Pure r, g, and b produce the corresponding weight value in y."""
    for w in WEIGHTS:
        wr, wg, wb = w
        h, c, y = colorsysx.rgb_to_hcy(1, 0, 0, weights_rgb=w)
        assert y == approx(wr)
        h, c, y = colorsysx.rgb_to_hcy(0, 1, 0, weights_rgb=w)
        assert y == approx(wg)
        h, c, y = colorsysx.rgb_to_hcy(0, 0, 1, weights_rgb=w)
        assert y == approx(wb)


def test_ranges():
    """Output should lie within the stated bounds, and cover that range"""
    n = 16
    min_h, max_h = [1, 0]
    min_c, max_c = [1, 0]
    min_y, max_y = [1, 0]
    for w in WEIGHTS:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            h, c, y = colorsysx.rgb_to_hcy(r0, g0, b0, weights_rgb=w)
            assert 0 <= h <= 1
            assert 0 <= c <= 1
            assert 0 <= y <= 1
            min_h, max_h = min(h, min_h), max(h, max_h)
            min_c, max_c = min(c, min_c), max(c, max_c)
            min_y, max_y = min(y, min_y), max(y, max_y)
    assert min_h <= 1/12
    assert max_h >= 1 - 1/12
    assert min_c == approx(0)
    assert max_c == approx(1)
    assert min_y == approx(0)
    assert max_y == approx(1)


def test_round_trips():
    """Should be able to convert to GHLS and back to RGB accurately."""
    n = 16
    for w in WEIGHTS:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            h, c, y = colorsysx.rgb_to_hcy(r0, g0, b0, weights_rgb=w)
            assert 0 <= y <= 1
            r1, g1, b1 = colorsysx.hcy_to_rgb(h, c, y, weights_rgb=w)
            assert 0 <= r1 <= 1
            assert 0 <= g1 <= 1
            assert 0 <= b1 <= 1

            assert (r1, g1, b1) == approx((r0, g0, b0))
