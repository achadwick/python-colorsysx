"""Reminder to remove deprecations at the promised version."""

from packaging.version import Version

import colorsysx


def test_v2_deprecation_aliases():
    # Test that the aliases are being respected
    # This is fairly pathological code, don't copy this!
    w_min2max_funcs = [
        # These should accept the old "w_min2max" parameter,
        # and convert it to "weights_sorted"
        colorsysx.rgb_to_glhs,
        colorsysx.glhs_to_rgb,
    ]
    w_rgb_funcs = [
        # These should accept the old "w_rgb" parameter,
        # and convert it to "weights_rgb"
        colorsysx.rgb_to_hcy,
        colorsysx.hcy_to_rgb,
        colorsysx.rgb_to_glhs,
        colorsysx.glhs_to_rgb,
        colorsysx.rgb_to_yuv,
        colorsysx.yuv_to_rgb,
    ]
    x, y, z = (0.5, 0.6, 0.7)
    weights = (0.3, 0.5, 0.7)
    for func in w_min2max_funcs:
        res_w_min2max = func(x, y, z, w_min2max=weights)
        res_weights_sorted = func(x, y, z, weights_sorted=weights)
        assert res_w_min2max == res_weights_sorted
    for func in w_rgb_funcs:
        res_w_rgb = func(x, y, z, w_rgb=weights)
        res_weights_rgb = func(x, y, z, weights_rgb=weights)
        assert res_w_rgb == res_weights_rgb


def test_v2_deprecations():
    assert Version(colorsysx.__version__) < Version("2.0"), (
        "v2.0+: remove w_rgb and w_min2max parameters, "
        "and the old aliases in colorsysx.weights"
    )
