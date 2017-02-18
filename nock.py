import copy


def right_assoc(cell):
    if not isinstance(cell, list):
        return cell

    if len(cell) == 2:
        return [right_assoc(cell[0]), right_assoc(cell[1])]

    return [cell[0], right_assoc(cell[1:])]


def get_subtree_at_index(index, tree):
    L = object()
    R = object()

    reverse_steps = []

    while index > 1:
        if index % 2:
            reverse_steps.append(R)
        else:
            reverse_steps.append(L)

        index = index // 2

    steps = list(reversed(reverse_steps))

    tree = right_assoc(tree)
    for step in steps:
        if step is L:
            tree = tree[0]
        if step is R:
            tree = tree[1]

    return tree


def nock(expr):
    ret = right_assoc(expr)
    while isinstance(ret, list):
        for rule in rules:
            if rule.match(ret):
                old = copy.deepcopy(ret)
                ret = rule.eval(ret)

                break

        return ret

rules = []


class Rule:
    op = NotImplemented

    def match(self, expr):
        if not isinstance(expr, list):
            return False

        try:
            op_subtree = get_subtree_at_index(6, expr)
        except Exception:
             return False

        return isinstance(op_subtree, int) and op_subtree == self.op

    def eval(self, expr):
        raise NotImplementedError()


class FormulaPair(Rule):
    def match(self, expr):
        try:
            a, [[b, c], d] = expr
            return True
        except:
            return False

    def eval(self, expr):
        a, [[b, c], d] = expr
        return [nock([a, b, c]), nock([a, d])]

rules.append(FormulaPair())


class SubTree(Rule):
    op = 0

    def eval(self, expr):
        a, [_, b] = expr
        return get_subtree_at_index(b, a)

rules.append(SubTree())


class Constant(Rule):
    op = 1

    def eval(self, expr):
        a, [_, b] = expr
        return b

rules.append(Constant())


class Eval(Rule):
    op = 2

    def eval(self, expr):
        a, [_, [b, c]] = expr
        return nock([nock([a, b]), nock([a, c])])

rules.append(Eval())


class IsCell(Rule):
    op = 3

    def eval(self, expr):
        a, [_, b] = expr
        is_cell = isinstance(nock([a, b]), list)
        return 0 if is_cell else 1

rules.append(IsCell())


class Increment(Rule):
    op = 4

    def eval(self, expr):
        a, [_, b] = expr
        return 1 + nock([a, b])

rules.append(Increment())


class Equal(Rule):
    op = 5

    def eval(self, expr):
        a, [_, b] = expr
        result = nock([a, b])
        assert len(result) == 2, result
        return 0 if result[0] == result[1] else 1

rules.append(Equal())


class If(Rule):
    op = 6

    def eval(self, expr):
        a, [_, [b, [c, d]]] = expr
        return nock(
            [a, 2, [0, 1], 2, [1, c, d], [1, 0], 2, [1, 2, 3], [1, 0], 4, 4, b])

rules.append(If())


class ComposeFuncs(Rule):
    op = 7

    def eval(self, expr):
        a, [_, [b, c]] = expr
        return nock([a, 2, b, 1, c])

rules.append(ComposeFuncs())


class DeclareVar(Rule):
    op = 8

    def eval(self, expr):
        a, [_, [b, c]] = expr
        return nock([a, 7, [[7, [0, 1], b], 0, 1], c])

rules.append(DeclareVar())


class FireArm(Rule):
    op = 9

    def eval(self, expr):
        a, [_, [b, c]] = expr
        return nock([a, 7, c, [2, [0, 1], [0, b]]])

rules.append(FireArm())


class Hint(Rule):
    op = 10

    def eval(self, expr):
        a, [_, [b, c]] = expr

        if isinstance(b, list):
            a, [_, [b, c], d] = expr
            return nock([a, 8, c, 7, [0, 2], d])

        else:
            return nock([a, c])
