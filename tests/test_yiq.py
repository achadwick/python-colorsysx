"""Tests for colorsysx.yiq"""

# Imports::

from .context import colorsysx

import colorsys
import itertools
from pytest import approx


# Test funcs::

def test_grey_is_grey():
    """Neutral grey is 0.5 grey."""
    y, i, q = colorsysx.rgb_to_yiq(0.5, 0.5, 0.5)
    assert abs(y - 0.5) == approx(0)
    assert i == approx(0)
    assert q == approx(0)


def test_equivalence():
    """Test that our YIQ does what colorsys's does."""
    n = 16
    for rn, gn, bn in itertools.product(range(n+1), repeat=3):
        r, g, b = (rn/n, gn/n, bn/n)
        y0, i0, q0 = colorsysx.rgb_to_yiq(r, g, b)
        y1, i1, q1 = colorsys.rgb_to_yiq(r, g, b)
        assert y0 == approx(y1)
        assert i0 == approx(i1)
        assert q0 == approx(q1)


def test_round_trips():
    n = 16
    for rn, gn, bn in itertools.product(range(n+1), repeat=3):
        rgb0 = (rn/n, gn/n, bn/n)
        yiq = colorsysx.rgb_to_yiq(*rgb0)
        assert 0 <= yiq[0] <= 1
        rgb1 = colorsysx.yiq_to_rgb(*yiq)
        assert all((0 <= c <= 1) for c in rgb1)
        assert rgb0 == approx(rgb1)


def test_unclamped():
    """Test that unclamped results can be returned and interpreted.

    Returning colours outside the RGB gamut isn't that helpful really,
    but it makes testing for this condition possible.

    """
    y, i, q = colorsysx.rgb_to_yiq(0, 0, 1)  # The bluest possible blue…
    assert y < 0.3                         # … has a very low luma.

    # Now try to make an extra-bright bluest blue that doesn't exist.
    y += 0.1

    # Now conversion back to rgb will go out of gamut,
    # if it's not clamped.
    rgb_clamped = colorsysx.yiq_to_rgb(y, i, q, clamp=True)
    rgb_unclamped = colorsysx.yiq_to_rgb(y, i, q, clamp=False)
    assert rgb_clamped != rgb_unclamped
    assert not all([0.0 <= c <= 1.0 for c in rgb_unclamped])
    assert max(rgb_unclamped) > 1.0
    assert all([0.0 <= c <= 1.0 for c in rgb_clamped])
