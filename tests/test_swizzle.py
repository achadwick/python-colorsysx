"""Test colorsysx._swizzle"""

from colorsysx import _swizzle


def test_swizzle_pairs_are_inverses():
    """The sectoral swizzles must be reverse mappings of each other"""

    from_sorted_to_rgb_generated = [
        tuple(s.index(i) for i in (0, 1, 2))
        for s in _swizzle.FROM_RGB_TO_SORTED
    ]
    assert _swizzle.FROM_SORTED_TO_RGB == from_sorted_to_rgb_generated

    from_rgb_to_sorted_generated = [
        tuple(s.index(i) for i in (0, 1, 2))
        for s in _swizzle.FROM_SORTED_TO_RGB
    ]
    assert _swizzle.FROM_RGB_TO_SORTED == from_rgb_to_sorted_generated
