import nose.tools

import nock


def test_right_assoc():
    nose.tools.assert_equals(nock.right_assoc([0, 1]), [0, 1])
    nose.tools.assert_equals(nock.right_assoc([0, 1, 2]), [0, [1, 2]])
    nose.tools.assert_equals(nock.right_assoc([0, [1, 2]]), [0, [1, 2]])
    nose.tools.assert_equals(nock.right_assoc([[0, 1], 2]), [[0, 1], 2])

    cases = (
        ([0, 1], [0, 1]),
        ([0, 1, 2], [0, [1, 2]]),
        ([0, [1, 2]], [0, [1, 2]]),
        ([[0, 1], 2], [[0, 1], 2]),
        ([1, 0, [541, 25, 99]], [1, [0, [541, [25, 99]]]]),
    )

    for expr, expected in cases:
        actual = nock.right_assoc(expr)
        nose.tools.assert_equals(actual, expected)


def test_nock_get_subtree_at_index():
    cases = (
        ((1, [1, 2]), [1, 2]),
        ((1, [541, 25, 99]), [541, [25, 99]]),
        ((2, [541, 25, 99]), 541),
        ((3, [541, 25, 99]), [25, 99]),
        ((6, [541, 25, 99]), 25),
        ((7, [541, 25, 99]), 99),
    )

    for (index, tree), expected in cases:
        actual = nock.get_subtree_at_index(index, tree)
        nose.tools.assert_equals(actual, expected)


def test_nock():
    cases = (
        ([[541, 25, 99], 0, 1], [541, [25, 99]]),
        ([44, 1, [13, 27]], [13, 27]),
        ([77, [2, [1, 42], [1, 1, 153, 218]]], [153, 218]),
        ([1, 3, [1, 12]], 1),
        ([57, [4, 0, 1]], 58),
        ([77, 5, 77], 0),
        ([42, [[4, 0, 1], [3, 0, 1]]], [43, 1]),
        ([42, [7, [4, 0, 1], [4, 0, 1]]], 44),
    )

    for expr, expected in cases:
        actual = nock.nock(expr)
        nose.tools.assert_equals(actual, expected)

