"""Test colorsysx.glhs"""

# Imports::

import colorsysx
import colorsys

from pytest import approx
import itertools


# Module vars::

WEIGHTS_SORTED = (
    colorsysx.weights.SortedWeights.HSI,
    colorsysx.weights.SortedWeights.HSV,
    colorsysx.weights.SortedWeights.HLS,
)
WEIGHTS_RGB = (
    colorsysx.weights.RGBWeights.REC601,
    colorsysx.weights.RGBWeights.REC709,
    colorsysx.weights.RGBWeights.REC2020,
)


# Test funcs::

def test_grey_is_grey_sorted():
    """Neutral grey is always neutral grey."""
    for w in WEIGHTS_SORTED:
        l, h, s = colorsysx.rgb_to_glhs(0.5, 0.5, 0.5, weights_sorted=w)
        assert l == approx(0.5)
        assert h == approx(0)
        assert s == approx(0)


def test_grey_is_grey_rgb():
    """Neutral grey is always neutral grey."""
    for w in WEIGHTS_RGB:
        l, h, s = colorsysx.rgb_to_glhs(0.5, 0.5, 0.5, weights_rgb=w)
        assert abs(l - 0.5) == approx(0)
        assert h == approx(0)
        assert s == approx(0)


def test_ranges_sorted():
    """Output should lie within the stated bounds, and cover that range"""
    n = 16
    min_l, max_l = [1, 0]
    min_h, max_h = [1, 0]
    min_s, max_s = [1, 0]
    for w in WEIGHTS_SORTED:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            l, h, s = colorsysx.rgb_to_glhs(r0, g0, b0, weights_sorted=w)
            assert 0 <= l <= 1
            assert 0 <= h <= 1
            assert 0 <= s <= 1
            min_l, max_l = min(l, min_l), max(l, max_l)
            min_h, max_h = min(h, min_h), max(h, max_h)
            min_s, max_s = min(s, min_s), max(s, max_s)
    assert min_l == approx(0)
    assert max_l >= 1
    assert min_h <= 1/12
    assert max_h >= 1 - 1/12
    assert min_s == approx(0)
    assert max_s >= 1


def test_ranges_rgb():
    """Output should lie within the stated bounds, and cover that range"""
    n = 16
    min_l, max_l = [1, 0]
    min_h, max_h = [1, 0]
    min_s, max_s = [1, 0]
    for w in WEIGHTS_RGB:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            l, h, s = colorsysx.rgb_to_glhs(r0, g0, b0, weights_rgb=w)
            assert 0 <= l <= 1
            assert 0 <= h <= 1
            assert 0 <= s <= 1
            min_l, max_l = min(l, min_l), max(l, max_l)
            min_h, max_h = min(h, min_h), max(h, max_h)
            min_s, max_s = min(s, min_s), max(s, max_s)
    assert min_l == approx(0)
    assert max_l >= 1
    assert min_h <= 1/12
    assert max_h >= 1 - 1/12
    assert min_s == approx(0)
    assert max_s >= 1


def test_round_trips_sorted():
    """Should be able to convert to GHLS and back to RGB accurately."""
    n = 16

    for w in WEIGHTS_SORTED:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            l, h, s = colorsysx.rgb_to_glhs(r0, g0, b0, weights_sorted=w)
            assert 0 <= l <= 1
            r1, g1, b1 = colorsysx.glhs_to_rgb(l, h, s, weights_sorted=w)
            assert 0 <= r1 <= 1
            assert 0 <= g1 <= 1
            assert 0 <= b1 <= 1

            assert (r1, g1, b1) == approx((r0, g0, b0))


def test_round_trips_rgb():
    """Should be able to convert to GHLS and back to RGB accurately."""
    n = 16

    for w in WEIGHTS_RGB:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            l, h, s = colorsysx.rgb_to_glhs(r0, g0, b0, weights_rgb=w)
            assert 0 <= l <= 1
            r1, g1, b1 = colorsysx.glhs_to_rgb(l, h, s, weights_rgb=w)
            assert 0 <= r1 <= 1
            assert 0 <= g1 <= 1
            assert 0 <= b1 <= 1

            assert (r1, g1, b1) == approx((r0, g0, b0))


def test_equivalences():
    """The GHLS funcs can reproduce other models with dedicated funcs."""
    n = 16
    for rn, gn, bn in itertools.product(range(n+1), repeat=3):
        r, g, b = (rn/n, gn/n, bn/n)

        # "HLS" double hexcone model
        (gl1, gh1, gs1) = colorsysx.rgb_to_glhs(
            r, g, b,
            weights_sorted=colorsysx.weights.SortedWeights.HLS,
        )
        (h1, l1, s1) = colorsys.rgb_to_hls(r, g, b)
        assert (gl1, gs1, gh1) == approx((l1, s1, h1))

        # "HSV" hexcone model
        (gl2, gh2, gs2) = colorsysx.rgb_to_glhs(
            r, g, b,
            weights_sorted=colorsysx.weights.SortedWeights.HSV,
        )
        (h2, s2, v2) = colorsys.rgb_to_hsv(r, g, b)
        assert (gl2, gs2, gh2) == approx((v2, s2, h2))

        # "HCY" luma-based model
        (gl3, gh3, gs3) = colorsysx.rgb_to_glhs(
            r, g, b,
            weights_rgb=colorsysx.weights.RGBWeights.REC709,
        )
        (h3, c3, y3) = colorsysx.rgb_to_hcy(
            r, g, b,
            weights_rgb=colorsysx.weights.RGBWeights.REC709,
        )
        assert (gl3, gs3, gh3) == approx((y3, c3, h3))
