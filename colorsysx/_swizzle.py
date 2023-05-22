"""Map weight lists in R-G-B order to sorted-component order.

These are maping tables that remap triples of weighting coefficients in
in the same order as the R, G, and B component _axes_ to the equivalent
triple in the order you get after sorting the _values_ of the current
colour's R, G, and B components, lowest first. The remapping is
different for each hue sector, and the two tables are not symmetrical.

These are an implementation detail of GLHS-family models, which use the
value-sorted order internally. Each mapping contains indexes into the
"from" list that turn it into the "to" list, like this:

    ord1 = [ord2[i] for i in FROM_ORD2_TO_ORD1[sector]]

The mapping lists are keyed by the hue sector number (0 to 5).

See: colorsysx.weights

"""

# Sectoral swizzles::

FROM_SORTED_TO_RGB = [
    (2, 1, 0),  # red->yellow
    (1, 2, 0),  # yellow->green
    (0, 2, 1),  # green->cyan
    (0, 1, 2),  # cyan->blue
    (1, 0, 2),  # blue->magenta
    (2, 0, 1),  # magenta->red
]

FROM_RGB_TO_SORTED = [
    (2, 1, 0),
    (2, 0, 1),
    (0, 2, 1),
    (0, 1, 2),
    (1, 0, 2),
    (1, 2, 0),
]

# Hint: calcuate one from the other like so:
#
# FROM_A_TO_B = [
#   tuple(s.index(i) for i in (0, 1, 2))
#   for s in FROM_B_TO_A
# ]
