"""Colorsys's YIQ colour model, but clamping is now optional."""

# This *could* be derived from the YUV transform, since it's just that
# plus a rotation+axis swap, times a pair of I and Q scaling factors.
# The basis is
#
#   # 33° rotation and (important!) a chromaticity-axis flip
#   YUV_YIQ_SPINFLIP = [
#       [1, 0, 0],
#       [0, -SIN_33, COS_33],
#       [0, COS_33, SIN_33],
#   ]
#   # then
#   yiq = yuv @ YUV_YIQ_SPINFLIP
#   yuv = yiq @ YUV_YIQ_SPINFLIP
#
# Which would be pretty cool, since you could plug in different
# weights to the YUV/YPbPr bit.
#
# However, I don't know what the special SMPTE C / FCC NTSC scaling
# factors are, and I want to remain compatible with colorsys's original
# YUV implementation, which does apply the scaling factor.

from . import _helpers as helpers


def rgb_to_yiq(r, g, b):
    """Convert RGB to YIQ.

    The "r", "g", and "b" parameters are floats between 0 and 1
    inclusive.

    Returns a tuple (y, u, v).

    """
    # SMPTE-C (FCC NTSC) constants, hardcoded
    y = 0.30*r + 0.59*g + 0.11*b
    i = 0.74*(r-y) - 0.27*(b-y)
    q = 0.48*(r-y) + 0.41*(b-y)
    return (y, i, q)


def yiq_to_rgb(y, i, q, clamp=True):
    """Convert from YIQ to RGB.

    The "y" parameter is a float in the interval [0, 1].
    The range for "i" is approximately [-0.6, 0.6].
    The range for "q" is approximately [-0.213, 0.213].

    By default, the returned (r, g, b) components are constrained to lie
    within the interval [0, 1]. Set "clamp" to False if you want to
    perform your own checking and/or clamping.

    """
    # $ qalc
    # > multisolve([\y = 0.30\r + 0.59\g + 0.11\b,
    #               \i = 0.74(\r−\y) − 0.27(\b−\y),
    #               \q = 0.48(\r−\y) + 0.41(\b−\y)];
    #              [\r, \g, \b])
    r = y + (410*i + 270*q) / 433
    g = y - (7020*i + 16240*q) / 25547
    b = y + (740*q - 480*i) / 433
    if clamp:
        r = helpers.clamp(r, 0.0, 1.0)
        g = helpers.clamp(g, 0.0, 1.0)
        b = helpers.clamp(b, 0.0, 1.0)
    return (r, g, b)
