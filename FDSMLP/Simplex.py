from copy import deepcopy

from .core.BasicSimplex import BasicSimplex
from .core.utils.Two_step_simplex_init import initialize_two_phase_simplex
from .core.utils.Normailze_simplex import convert_to_standard_form


class Two_step_simplex(BasicSimplex):
    def __init__(self, b, A, constrain, constraints):
        self.b_origin_two = b
        self.A_origin_two = A
        self.constraints = constraints
        b, A, constrain, base_ind, self.b_normal, self.A_normal, self.base_ind_artificial, self.base_ind_nature = initialize_two_phase_simplex(
            b, A, constrain, constraints)
        super().__init__(b, A, constrain, base_ind)
        self.b_step_one = []
        for col in range(self.variable_nums-len(self.base_ind_artificial)):
            self.b_step_one.append(
                sum([self.A[i][col] for i in range(self.constrain_nums)]))

        self.b_step_one += [0 for _ in range(len(self.base_ind_artificial))]
        self.b_copy = deepcopy(self.b)
        self.b = self.b_step_one

    def set_cell_width(self, cell_width):
        self.cell_width = cell_width

    def solve(self):
        print('开始执行两步法进行线性规划求解：')
        print(f'原始目标函数为：\n{self.__get_objective_func(self.b_origin_two)}')
        print(
            f'原始约束条件为：\n{self.__get_constrain_func(self.A_origin_two,self.constrain,self.constraints)}')
        print(f'进行标准化后的目标函数为：\n{self.__get_objective_func(self.b_normal)}')
        print(
            f'标准化后得约束条件为：\n{self.__get_constrain_func(self.A_normal,self.constrain,["=" for _ in range(len(self.constrain))])}')
        print(f'使用两步法修改目标函数为：\n{self.__get_objective_func(self.b)}')
        print(
            f'使用两步法修改约束条件为：\n{self.__get_constrain_func(self.A,self.constrain,["=" for _ in range(len(self.constrain))])}')

        print('初始化单纯形表后结果如下：')
        print(self.create_table())
        print('开始进行第一阶段运算：')
        status = self._solve_step_one()
        print(self.create_table())
        print(f'第一阶段算法执行完毕，得到如上结果，此时的检验数结果为：{self.b_copy}\n')
        self._solve_step_two()

    def __get_objective_func(self, b):
        self.__get_objective = 'max y ='
        for coffient_index in range(len(b)):
            if coffient_index == 0:
                self.__get_objective += f' {b[coffient_index]} * X{coffient_index+1}' if b[
                    coffient_index] > 0 else f' - {-b[coffient_index]} * X{coffient_index+1}'
            else:
                self.__get_objective += f' + {b[coffient_index]} * X{coffient_index+1}' if b[
                    coffient_index] > 0 else f' - {-b[coffient_index]} * X{coffient_index+1}'

        return self.__get_objective

    def __get_constrain_func(self, A, constrain, constraints):
        self.__get_constrain = ''
        for row_index in range(len(A)):
            row = A[row_index]
            for coffient_index in range(len(row)):
                if coffient_index == 0:
                    self.__get_constrain += f' {row[coffient_index]} * X{coffient_index+1}' if row[
                        coffient_index] >= 0 else f' - {-row[coffient_index]} * X{coffient_index+1}'
                else:
                    self.__get_constrain += f' + {row[coffient_index]} * X{coffient_index+1}' if row[
                        coffient_index] >= 0 else f' - {-row[coffient_index]} * X{coffient_index+1}'
            self.__get_constrain += f' {constraints[row_index]} {constrain[row_index]}\n'

        return self.__get_constrain

    def _find_invar(self):
        if max(self.b) <= 0:
            return -1
        index = 0
        index_return = -2
        max_num = 1e-6
        for var in self.b:
            if var > max_num and self._find_outvar(index) != -2:
                index_return = index-1
                max_num = var
            index += 1

        if index_return == -2:
            return -2
        return index_return+1

    def _find_outvar(self, invar):
        if invar == -2:
            return -2
        invar_col = [self.A[i][invar] for i in range(len(self.A))]
        no_border = True
        i = 0
        theta_max, outvar_index = 0, 0
        for index in range(len(invar_col)):
            if invar_col[index] > 1e-6:
                if i == 0:
                    i += 1
                    theta_max = self.constrain[index]/invar_col[index]+1
                no_border = False
                theta = self.constrain[index]/invar_col[index]
                if theta <= theta_max:
                    theta_max = theta
                    outvar_index = index
        if no_border:
            return -2
        return outvar_index

    def _solve_step_one(self):
        while True:
            self.invar = self._find_invar()
            self.outvar = self._find_outvar(self.invar)
            if self.invar == -1:
                return 0  # 状态码0代表已找到最优解，准备进行下一步
            if self.outvar == -2:
                return 2  # 状态码2代表本问题有无界解

            print(self.create_table(dimension=(self.outvar, self.invar)))
            print(
                f'以X{self.invar+1}为入基变量，{self.variable_names[self.base_ind[self.outvar]]}为出基变量进行转轴计算，得：\n')

            self.b_copy = self.trans(self.outvar, self.invar, b=self.b_copy)

    def _solve_step_two(self):
        self.b = self.b_copy
        self.b_in_base = []
        others = False
        for index in self.base_ind_artificial:
            if index in self.base_ind:
                others = True
                self.b_in_base.append(index)

        if not others:
            # 所有人工变量均不在基变量中，直接删除所有人工变量
            string = '所有人工变量均不在基变量中，删除所有人工变量:' + \
                ' '.join([self.variable_names[i]
                         for i in self.base_ind_artificial])
            print(string)
            for index in sorted(self.base_ind_artificial, reverse=True):
                del self.variable_names[index]
                del self.b_origin[index]
                del self.b[index]
                for row in self.A:
                    del row[index]

            print('最终单纯形表为：')
            print(self.create_table())
            result_x, result_y = self._get_result()
            print(f'线性规划解得最优解为：{result_x},此时目标函数极大值为：{result_y}')

        else:
            string = '人工变量'+' '.join([self.variable_names[i]
                                     for i in self.b_in_base])+'在基变量中，进行判断'
            print(string)
            delete = True
            no_solution = False
            trans_dimension_lst = []

            for index in range(self.variable_nums-len(self.base_ind_artificial)):
                for row_index in self.b_in_base:
                    if abs(self.A[self.base_ind.index(row_index)][index]-0) > 1e-6:
                        delete = False
                        trans_dimension_lst.append(
                            [self.base_ind.index(row_index), index])
                    if abs(self.constrain[self.base_ind.index(row_index)]-0) > 1e-6:
                        no_solution = True

            if not no_solution:
                if delete:
                    print('人工变量对应行的原始决策变量约束都为0，直接删除所有人工变量和基变量人工变量对应的行')
                    for row_index in self.b_in_base:
                        del self.A[self.base_ind.index(row_index)]
                        del self.constrain[self.base_ind.index(row_index)]
                        del self.base_ind[self.base_ind.index(row_index)]

                    for index in sorted(self.base_ind_artificial, reverse=True):
                        del self.variable_names[index]
                        del self.b_origin[index]
                        del self.b[index]
                        for row in self.A:
                            del row[index]

                    self.constrain_nums = len(self.constrain)
                    self.variable_nums = len(self.variable_names)

                    print(self.create_table())

                    while True:
                        self.invar = self._find_invar()
                        self.outvar = self._find_outvar(self.invar)
                        if self.invar == -1:
                            status = -1
                            break
                        if self.outvar == -2:
                            status = -2
                            break

                        print(self.create_table(
                            dimension=(self.outvar, self.invar)))
                        print(
                            f'以X{self.invar+1}为入基变量，{self.variable_names[self.base_ind[self.outvar]]}为出基变量进行转轴计算，得：\n')

                        self.trans(self.outvar, self.invar)

                    print('最终单纯形表为：')
                    print(self.create_table())
                    if status == -2:
                        print('该问题是无界的')
                    else:
                        result_x, result_y = self._get_result()
                        print(f'线性规划解得最优解为：{result_x},此时目标函数极大值为：{result_y}')
                else:
                    print('人工变量对应行的原始决策变量约束存在不为0的值，直接删除所有人工变量和基变量人工变量对应的行')
                    for dimension in trans_dimension_lst:
                        print(self.create_table((dimension[0], dimension[1])))
                        print(
                            f'以X{dimension[1]+1}为入基变量，X{self.base_ind[dimension[0]]+1}为出基变量进行转轴计算，得：\n')

                        self.trans(dimension[0], dimension[1])

                        ind_num = 0
                        for ind in self.base_ind:
                            if ind in self.base_ind_nature:
                                ind_num += 1

                        if ind_num == self.constrain_nums:
                            break

                    print(self.create_table())
                    for index in sorted(self.base_ind_artificial, reverse=True):
                        del self.variable_names[index]
                        del self.b_origin[index]
                        del self.b[index]
                        for row in self.A:
                            del row[index]

                    print('最终单纯形表为：')
                    print(self.create_table())
                    result_x, result_y = self._get_result()
                    print(f'线性规划解得最优解为：{result_x},此时目标函数极大值为：{result_y}')

            else:
                print('该线性规划问题无最优解！')

    def _get_result(self):
        result_x = []
        for index in range(len(self.variable_names)):
            if index in self.base_ind:
                result_x.append(self.constrain[self.base_ind.index(index)])
            else:
                result_x.append(0)

        print(result_x)

        result_y = 0

        for i in range(len(result_x)):
            x = result_x[i]
            result_y += self.b_origin[i]*x

        return result_x, result_y
