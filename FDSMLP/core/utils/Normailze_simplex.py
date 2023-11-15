import warnings

from .InitializationError import InitializationError


def convert_to_standard_form(b, A, c, constraints):
    """
    Convert the linear program to standard form by adding slack, surplus, and artificial variables.
    :param b: Coefficients of the objective function.
    :param A: Coefficients of the constraints.
    :param c: Constants of the constraints.
    :param constraints: List of strings representing constraints, each string is '<=', '>=', or '='.
    :return: Modified b, A, c, and additional variables information.
    """
    num_constraints = len(A)
    num_vars = len(A[0])

    if num_constraints != len(c):
        raise InitializationError('约束条件右侧变量与约束方程数量不符！')

    if len(b) > num_vars:
        raise InitializationError('目标函数系数大于约束条件中变量！')

    if len(b) < num_vars:
        warnings.warn('目标函数变量小于约束条件变量，自动填充为0！')
        b += [0]*(num_vars-len(b))

    num_slack = constraints.count('<=')
    num_surplus = constraints.count('>=')

    modified_A = [row[:] + [0] * (num_slack + num_surplus) for row in A]
    modified_b = b[:] + [0] * (num_slack + num_surplus)

    slack_surplus_col = num_vars
    for i, constraint in enumerate(constraints):
        if constraint == '<=':
            modified_A[i][slack_surplus_col] = 1
            slack_surplus_col += 1
        elif constraint == '>=':
            modified_A[i][slack_surplus_col] = -1
            slack_surplus_col += 1

    return modified_b, modified_A, c
