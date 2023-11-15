from itertools import combinations
from copy import deepcopy

from .SimplexError import SimplexError
from .utils.matrix import Det


class BasicSimplex:
    def __init__(self, b, A, constrain, base_ind=None):
        """
        这是单纯形法的基础实现，满足Ax=constrain的标准型显示，目标函数为max bx
        """
        self.A = A
        self.b = b
        self.b_origin = b
        self.constrain = constrain
        self.variable_nums = len(A[0])
        self.constrain_nums = len(A)
        self.variable_names = [f'X{i+1}' for i in range(self.variable_nums)]
        self.cell_width = 7
        if base_ind:
            self.base_ind = base_ind
        else:
            self.base_ind = self.get_base_ind()

    def __str__(self):
        return self.create_table()

    def create_table(self, dimension=None):
        cell_width = self.cell_width

        header = f"{'CB':^{cell_width}}|{'XB':^{cell_width}}|{'b':^{cell_width}}|" + \
            "|".join(
                f"{name:^{cell_width}}" for name in self.variable_names) + "|\n"
        separator = "-" * len(header) + "\n"

        b_row = f"{(' '*cell_width+'|')*3}" + \
            "|".join(f"{val:^{cell_width}.3f}" for val in self.b_origin) + "|\n"
        table = b_row + separator
        table += header + separator

        k = 0
        for i in range(len(self.base_ind)):

            cb_value = self.b_origin[self.base_ind[i]]
            xb_value = self.variable_names[self.base_ind[i]]
            b_value = self.constrain[k]
            row = f"{str(cb_value):^{cell_width}}|{xb_value:^{cell_width}}|{b_value:^{cell_width}.3f}|"
            k += 1

            for j, val in enumerate(self.A[i]):
                formatted_val = f"{val:^{cell_width}.3f}"
                if dimension and (i, j) == dimension:
                    formatted_val = f"\033[91m{formatted_val}\033[0m"
                row += f"{formatted_val}|"
            table += row + "\n"

        cj_zj_row = f"{(' '*cell_width+'|')*3}" + \
            "|".join(f"{c:^{cell_width}.3f}" for c in self.b) + "|"
        table += separator + cj_zj_row + \
            "\n\n\033[93m" + separator + "\033[0m" + "\n"

        return table

    def get_base_ind(self):
        if self.constrain_nums > self.variable_nums:
            raise SimplexError('在基类中，约束方程数量不能大于决策变量数量！')

        base_index = list(combinations(
            range(self.variable_nums), self.constrain_nums))

        for index in base_index:
            base_matrix = [[self.A[i][j] for j in index]
                           for i in range(self.constrain_nums)]
            if Det(base_matrix) != 0:
                return index
        raise SimplexError('约束矩阵已退化！')

    def trans(self, outvar_dimension, invar_dimension, b=None):
        _b_copy = deepcopy(self.b)
        _A_copy = deepcopy(self.A)
        _constrain_copy = deepcopy(self.constrain)

        for i in range(self.constrain_nums):
            if i != outvar_dimension:
                self.constrain[i] = _constrain_copy[i]-_constrain_copy[outvar_dimension] * \
                    _A_copy[i][invar_dimension] / \
                    _A_copy[outvar_dimension][invar_dimension]
            else:
                self.constrain[i] /= _A_copy[outvar_dimension][invar_dimension]

        self.b = [_b_copy[j]-_A_copy[outvar_dimension][j]*_b_copy[invar_dimension] /
                  _A_copy[outvar_dimension][invar_dimension] for j in range(self.variable_nums)]

        for row_index in range(self.constrain_nums):
            if row_index != outvar_dimension:
                self.A[row_index] = [_A_copy[row_index][j]-_A_copy[outvar_dimension][j]*_A_copy[row_index]
                                     [invar_dimension]/_A_copy[outvar_dimension][invar_dimension] for j in range(self.variable_nums)]
            else:
                self.A[outvar_dimension] = [_A_copy[outvar_dimension][i] /
                                            _A_copy[outvar_dimension][invar_dimension] for i in range(self.variable_nums)]

        self.base_ind[outvar_dimension] = invar_dimension

        if b:
            _b_copy_2 = deepcopy(b)
            b = [_b_copy_2[j]-_A_copy[outvar_dimension][j]*_b_copy_2[invar_dimension] /
                 _A_copy[outvar_dimension][invar_dimension] for j in range(self.variable_nums)]
            return b
