"""Conversions to and from GLHS.

GLHS is a family of cylindrical Lightness, Hue and Saturation colour
models, distinguished from each other by their weighting parameters
alone. It is a generalization of other colour models with the same
basic, arithmetic construction, specifically the HLS "double hexcone"
model, the HSV "hexcone" model, and the 1976 HSI model by John Kender.

The conversion algorithms presented here follow the 1993 paper by Haim
Levkowitz and Gabor Herman "GLHS: a generalized lightness, hue, and
saturation color model".  However, since HCY is a special case of this
general colour manipulation algorithm, this module adds the option of
describing weighting coefficients in RGB axis order.

Weight tuples can be given in one of two ways: in order of the RGB
components' contributions from lowest value to highest, or in the order
of the R, G and B axes themselves.

References:

* https://doi.org/10.1006/cgip.1993.1019

"""

# Imports::

from . import weights
from ._helpers import clamp
from . import _swizzle


# Default values::

DEFAULT_WEIGHTS_SORTED = weights.SortedWeights.HLS


# Conversion functions::

def rgb_to_glhs(r, g, b,
                weights_sorted=None, weights_rgb=None,
                w_min2max=None, w_rgb=None):
    """Convert a colour from RGB to a model covered by GLHS.

    The optional parameters select the converson model used. Only one of
    "weights_sorted" or "weights_rgb" may be defined. Weights are tuples
    of three floats that sum to 1.0. By default, if neither is provided,
    weights_sorted=colorsysx.SortedWeights.HLS is used, meaning that the
    return values will reflect the HLS "double hexcone" model.

    "w_rgb" is a deprecated override for "weights_rgb", and "w_min2max"
    is a deprecated override for "weights_sorted". These aliases will be
    removed in colorsysx 2.0.

    Returns a tuple of floats (h, l, s) where each term is between 0 and
    1 inclusive.

    """

    # FIXME: remove these two old aliases in 2.0
    weights_sorted = w_min2max or weights_sorted
    weights_rgb = w_rgb or weights_rgb

    # Check that the options make sense, and pick a default.
    if (weights_sorted is not None) and (weights_rgb is not None):
        raise TypeError(
            "weights_sorted and weights_rgb "
            "cannot both be defined"
        )
    elif (weights_sorted is None) and (weights_rgb is None):
        weights_sorted = DEFAULT_WEIGHTS_SORTED

    # GLHS operates with component weightings in the order of the
    # smallest, middle, and largest colour components. If the caller
    # passed a set of RGB-ordered weightings instead, extract them in
    # the right order now.
    if weights_rgb is not None:
        (c_min, w_min), (c_mid, w_mid), (c_max, w_max) \
            = sorted(zip([r, g, b], weights_rgb))
    else:
        w_min, w_mid, w_max = weights_sorted
        c_min, c_mid, c_max = sorted([r, g, b])

    # Handle the achromatic case first to avoid a division by zero later.
    if c_max == c_min:
        return (c_max, 0.0, 0.0)

    # Compute hue
    mid_minus_min = c_mid - c_min
    max_minus_min = c_max - c_min
    max_minus_mid = c_max - c_mid
    if r > g >= b:
        sector = 0
    elif g >= r > b:
        sector = 1
    elif g > b >= r:
        sector = 2
    elif b >= g > r:
        sector = 3
    elif b > r >= g:
        sector = 4
    else:  # r >= b > g
        sector = 5

    # Hue within sector
    if (sector % 2) == 0:
        f = mid_minus_min / max_minus_min
    else:
        f = max_minus_mid / max_minus_min

    h = (sector + f) / 6.0

    # Compute lightness
    l = w_max*c_max + w_mid*c_mid + w_min*c_min
    l_q = w_mid * mid_minus_min / max_minus_min + w_max
    if l <= l_q:
        s = (l - c_min) / l
    else:
        s = (c_max - l) / (1.0 - l)

    return (l, h, s)


def glhs_to_rgb(l, h, s,
                w_min2max=None, w_rgb=None,
                weights_sorted=None, weights_rgb=None,
                ):
    """Converts from HCY to RGB.

    The "l", "h", and "s" parameters are floats between 0 and 1
    inclusive. "weights_rgb and "weights_sorted" have the same meaning
    and default values as they do in "rgb_to_glhs()".

    Returns a tuple of floats in the form (r, g, b), where each
    component is between 0 and 1 inclusive.

    """
    # FIXME: remove these two old aliases in 2.0
    weights_sorted = w_min2max or weights_sorted
    weights_rgb = w_rgb or weights_rgb

    # Check that the options make sense, and pick a default.
    if (weights_sorted is not None) and (weights_rgb is not None):
        raise TypeError(
            "weights_sorted and weights_rgb "
            "cannot both be defined"
        )
    elif (weights_sorted is None) and (weights_rgb is None):
        weights_sorted = DEFAULT_WEIGHTS_SORTED

    # Achromatic
    if s == 0:
        return (clamp(c, 0.0, 1.0) for c in (l, l, l))

    # Pick a sector based on the hue angle.
    # This determines the order in which {r, g, b} are selected from
    # the {min, mid, max} components we're going to be calculating
    # later.
    sector = int((h % 1.0) * 6.0)
    f = ((h % 1.0) * 6.0) - sector
    if (sector % 2) == 0:
        ff = f
    else:
        ff = 1.0 - f

    # If the weights are in RGB order,
    # swizzle them back into min-to-max order now.
    if weights_rgb is not None:
        mapping_indices = _swizzle.FROM_RGB_TO_SORTED[sector]
        weights_sorted = tuple(weights_rgb[i] for i in mapping_indices)
    w_min, w_mid, w_max = weights_sorted

    # Calculate the RGB components in min-to-max order
    l_q = (w_mid * ff) + w_max
    if l <= l_q:
        c_min = (1 - s) * l
        c_mid = (
            ((ff * l) + (c_min * ((1-ff)*w_max - (ff*w_min)))) /
            (w_max + (ff * w_mid))
        )
        c_max = (l - (w_mid * c_mid) - (w_min * c_min)) / w_max
    else:
        c_max = s + ((1 - s) * l)
        c_mid = (
            (((1 - ff)*l) - (c_max * (((1-ff)*w_max) - (ff*w_min)))) /
            (((1-ff)*w_mid) + w_min)
        )
        if w_min > 0:
            c_min = (l - (w_max * c_max) - (w_mid * c_mid)) / w_min
        else:
            c_min = (c_mid - (ff * c_max)) / (1 - ff)

    # Back to RGB order
    mapping_indices = _swizzle.FROM_SORTED_TO_RGB[sector]
    c_sorted = (c_min, c_mid, c_max)
    c_rgb = tuple(c_sorted[i] for i in mapping_indices)
    return tuple(clamp(c, 0.0, 1.0) for c in c_rgb)
