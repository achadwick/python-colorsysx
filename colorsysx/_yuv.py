"""YUV (YPbPr) colour model.

YUV defines colour in terms of a luma term (Y), and two absolute colour
difference terms (U and V). Coordinates are Cartesian.

This colour model is a counterpart to the YIQ colour space defined by
the Python standard library's colorsys module.  YIQ is used for NTSC
standard television, amongst other things. What this package calls YUV
is the family of analogue colour representations used in PAL, SDTV,
HDTV, and UHDTV. The YUV functions here use the analogue Y'PbPr
transformation, from which the corresponding digital transformations can
be derived.

Different weights can be provided for R, G, and B when converting to and
from YUV. The defaults make manipulating colours to meet WCAG
2.2 or draft 3.0 contrast criteria easier. You should use appropriately
gamma corrected R'G'B' values before converting to Y'UV, if you're doing
this.

YUV preserves absolute colourfulness when you manipulate Y alone, which
is nice, but it's quite easy to drift outside the RGB gamut envelope.
You may prefer HCY for this purpose.

References:

* https://en.wikipedia.org/wiki/YUV#Related_color_models
* https://en.wikipedia.org/wiki/YCbCr#R'G'B'_to_Y'PbPr

"""

# Imports::

from . import weights
from . import _helpers as helpers


# Default values::

DEFAULT_WEIGHTS = weights.RGBWeights.REC709


# Conversion functions::

def rgb_to_yuv(r, g, b, weights_rgb=None, w_rgb=None):
    """Convert RGB to YUV (YPbBr).

    The "r", "g", and "b" parameters are floats between 0 and 1
    inclusive.  If given, "weights_rgb" specifies the luma weighting
    coefficients for the R, G, and B components, in that order. It must
    be a tuple of 3 floats that sum to 1, but this is not enforced. The
    default is colorsysx.weights.RGBWeights.REC709.

    "w_rgb" is a deprecated override for "weights_rgb". It will be removed
    in colorsysx 2.0.

    Returns a tuple (y, u, v).

    """
    weights_rgb = w_rgb or weights_rgb  # FIXME: remove in 2.0
    if weights_rgb is None:
        weights_rgb = DEFAULT_WEIGHTS
    kr, kg, kb = weights_rgb
    color_matrix = [
        [kr,               kg,                kb],
        [-0.5 * kr/(1-kb), -0.5 * kg/(1-kb),  0.5],
        [0.5,              -0.5 * kg/(1-kr), -0.5 * kb/(1-kr)],
    ]
    [[y], [u], [v]] = helpers.matmul(color_matrix, [[r], [g], [b]])
    return (y, u, v)


def yuv_to_rgb(y, u, v, weights_rgb=DEFAULT_WEIGHTS, w_rgb=None,
               clamp=True):
    """Convert from YUV to RGB.

    The "y", "u", and "v" parameters are floats between 0 and 1
    inclusive.  "weights" has the same meaning and default value as it
    does in rgb_to_yuv().

    "w_rgb" is a deprecated override for "weights_rgb". It will be
    removed in colorsysx 2.0.

    By default, the returned (R, G, B) components are constrained to lie
    within the interval [0, 1]. Set "clamp" to False if you want to
    perform your own checking.

    """
    weights_rgb = w_rgb or weights_rgb  # FIXME: remove in 2.0
    if weights_rgb is None:
        weights_rgb = DEFAULT_WEIGHTS
    kr, kg, kb = weights_rgb
    inverse_color_matrix = [
        [1., 0.,                 2 - 2*kr],
        [1., -(kb/kg)*(2-2*kb), -(kr/kg)*(2-2*kr)],
        [1., 2-2*kb,             0.],
    ]
    [[r], [g], [b]] = helpers.matmul(inverse_color_matrix, [[y], [u], [v]])
    if clamp:
        return tuple(helpers.clamp(c, 0, 1) for c in (r, g, b))
    else:
        return (r, g, b)
