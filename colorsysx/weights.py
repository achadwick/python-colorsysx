"""Luma/luminance/lightness weighting coefficients.

Each set of weights is a tuple of three floats that sum to exactly 1.
They are used for calculating lightness terms by this package's colour
conversion functions.

"""

# Imports::

import sys

if sys.version_info >= (3, 11):
    import enum

    class _EnumBase (tuple, enum.ReprEnum):
        pass

else:

    class _EnumBase (object):
        pass


# Const namespaces::

class RGBWeights (_EnumBase):
    """Weights for each RGB component, in typical red-green-blue order.

    These weighting tuples are appropriate for conversions which use a
    weighted sum of the individual colour components. The ones given
    here correspond to broadcast TV standards from different ages.

    * REC601: ITU-R Recommendation BT.601 (a.k.a. BT.470), as used in SDTV.

    * REC709: ITU-R Recommendation BT.709, as used in HDTV.

    * REC2020: ITU-R Recommendation BT.2020, as used in UHDTV.

    These weightings are appropriate for use with both the YUV and the
    GLHS pairs of conversion functions.

    ("ComponentWeights" is a deprecated alias for this class name. It
    will be removed in v2.0.)

    """
    # (R, G, B)
    REC601 = (0.299, 0.587, 0.114)
    REC709 = (0.2126, 0.7152, 0.0722)
    REC2020 = (0.2627, 0.678, 0.0593)


class SortedWeights (_EnumBase):
    """Weights for RGB components when sorted by ascending numeric value.

    These weighting tuples are appropriate for the GLHS conversion
    functions, where using different weights for the "weights_sorted"
    parameter makes the conversion operate like other well known
    cylindrical lighness/hue/saturation models.

    The weights are used to make a weighted sum of the three RGB
    components ordered by their numeric value, lowest first.

    * HSI: Weighting coefficients for the HSI model.

      For this model, the Intensity (or lightness) term is the
      arithmetic mean of all three R,G and B components. The GLHS paper
      calls this the "HSL Triangle" model.

    * HSV: Weighting coefficients for the HSV "hexcone" model.

      Here, the Value term is the maximum of all three R, G and B
      components.  Using these weights with the GLHS functions produces
      the same results as colorsys.rgb_to_hsv() and its inverse function

    * HLS: Weighting coefficients for the HLS "double hexcone" model.

      The HLS Lightness term is an average of the highest and lowest
      valued RGB component. This produces the same results as
      colorsys.rgb_to_hls() and its inverse.

    References:

    * https://doi.org/10.1006/cgip.1993.1019

    ("SortedComponentWeights" is a deprecated alias for this class name.
    It will be removed in v2.0.)

    """
    # (Min, Mid, Max)
    HSI = (1/3, 1/3, 1/3)
    HSV = (0, 0, 1)
    HLS = (1/2, 0, 1/2)


# Deprecated aliases, to be removed in version 2.0::

ComponentWeights = RGBWeights
SortedComponentWeights = SortedWeights
