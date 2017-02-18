import nose.tools

import nock


def test_right_assoc():
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
        ([42, [[4, 0, 1], [3, 0, 1]]], [43, 1]),  # FunctionPair
        ([[541, 25, 99], 0, 1], [541, [25, 99]]),  # SubTree
        ([44, 1, [13, 27]], [13, 27]),  # Constant
        ([77, [2, [1, 42], [1, 1, 153, 218]]], [153, 218]),  # Eval
        ([1, 3, [1, 12]], 1),  # IsCell
        ([57, [4, 0, 1]], 58),  # Increment
        ([77, 5, 77], 0),  # Equal
        ([42, [6, [1, 0], [4, 0, 1], [1, 233]]], 43),  # If
        ([42, [7, [4, 0, 1], [4, 0, 1]]], 44),  # ComposeFuncs
        ([42, [8, [4, 0, 1], [0, 1]]], [43, 42]),  # DeclareVar
        ([42, [8, [1, 0], 8, [1, 6, [5, [0, 7], 4, 0, 6], [0, 6], 9, 2, [0, 2],
                              [4, 0, 6], 0, 7], 9, 2, 0, 1]], 41),
    )

    print()
    for expr, expected in cases:
        print(expr)
        actual = nock.nock(expr)
        nose.tools.assert_equals(actual, expected)
        print()
