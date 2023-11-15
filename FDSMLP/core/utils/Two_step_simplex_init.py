from copy import deepcopy
from collections import Counter

from .Normailze_simplex import convert_to_standard_form


def initialize_two_phase_simplex(b, A, c, constraints):
    """
    Initialize the simplex table for the two-phase method by adding artificial variables,
    and return the modified b, A, c, along with the base variable indices.
    :param b: Coefficients of the objective function.
    :param A: Coefficients of the constraints.
    :param c: Constants of the constraints.
    :param constraints: List of strings representing constraints, each string is '='.
    :return: Modified b, A, c after constructing the simplex table for two-phase method and base variable indices.
    """
    modified_b, modified_A, c = convert_to_standard_form(b, A, c, constraints)

    start = len(modified_b)

    b_normalized = deepcopy(modified_b)
    A_normalized = deepcopy(modified_A)

    num_constraints = len(modified_A)
    num_vars = len(modified_A[0])

    base_ind = []
    used_rows = []

    for j in range(num_vars):
        if modified_b[j] == 0:
            vec = [modified_A[i][j] for i in range(num_constraints)]
            if Counter(vec)[1] == 1 and Counter(vec)[0] == num_constraints-1 and vec.index(max(vec)) not in used_rows:
                base_ind.append(j)
                used_rows.append(vec.index(max(vec)))
                continue

    base_ind_nature = deepcopy(base_ind)

    artificial_nums = 0

    for i in range(num_constraints):
        if i not in used_rows:
            artificial_nums += 1

    j = 0
    for row_index in range(num_constraints):
        if row_index in used_rows:
            modified_A[row_index] += [0]*artificial_nums
        else:
            artificial = [0]*artificial_nums
            if len(artificial) > 0:
                artificial[j] = 1
            modified_A[row_index] += artificial
            j += 1

    modified_b += [0]*artificial_nums

    base_ind += [start+i for i in range(artificial_nums)]

    base_ind_return = [0 for _ in range(len(base_ind))]

    for ind in base_ind:
        x_vec = [row[ind] for row in modified_A]
        base_ind_return[x_vec.index(1)] = ind

    artificial_lst = list(set(base_ind)-set(base_ind_nature))

    return modified_b, modified_A, c, base_ind_return, b_normalized, A_normalized, artificial_lst, base_ind_nature
