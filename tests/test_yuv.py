"""Tests for colorsysx.yuv"""

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
        y, u, v = colorsysx.rgb_to_yuv(0.5, 0.5, 0.5, weights_rgb=w)
        assert y == approx(0.5)
        assert u == approx(0)
        assert v == approx(0)


def test_pure_components_match_weights():
    """Pure r, g, and b produce the corresponding weight value in y."""
    for w in WEIGHTS:
        wr, wg, wb = w
        y, u, v = colorsysx.rgb_to_yuv(1, 0, 0, weights_rgb=w)
        assert y == approx(wr)
        y, u, v = colorsysx.rgb_to_yuv(0, 1, 0, weights_rgb=w)
        assert y == approx(wg)
        y, u, v = colorsysx.rgb_to_yuv(0, 0, 1, weights_rgb=w)
        assert y == approx(wb)


def test_round_trips():
    """Should be able to convert to GHLS and back to RGB accurately."""
    n = 16
    for w in WEIGHTS:
        for rn, gn, bn in itertools.product(range(n+1), repeat=3):
            r0, g0, b0 = (rn/n, gn/n, bn/n)
            y, u, v = colorsysx.rgb_to_yuv(r0, g0, b0, weights_rgb=w)
            assert 0 <= y <= 1
            r1, g1, b1 = colorsysx.yuv_to_rgb(y, u, v, weights_rgb=w)
            assert 0 <= r1 <= 1
            assert 0 <= g1 <= 1
            assert 0 <= b1 <= 1
            assert (r1, g1, b1) == approx((r0, g0, b0))


def test_unclamped():
    """Test that unclamped results can be returned and interpreted.

    Returning colours outside the RGB gamut isn't that helpful really,
    but it makes testing for this condition possible.

    """
    y, u, v = colorsysx.rgb_to_yuv(0, 0, 1)  # The bluest possible blue…
    assert y < 0.3                         # … has a very low luma.

    # Now try to make an extra-bright bluest blue that doesn't exist.
    y += 0.1

    # Now conversion back to rgb will go out of gamut,
    # if it's not clamped.
    rgb_clamped = colorsysx.yuv_to_rgb(y, u, v, clamp=True)
    rgb_unclamped = colorsysx.yuv_to_rgb(y, u, v, clamp=False)
    assert rgb_clamped != rgb_unclamped
    assert not all([0.0 <= c <= 1.0 for c in rgb_unclamped])
    assert max(rgb_unclamped) > 1.0
    assert all([0.0 <= c <= 1.0 for c in rgb_clamped])
