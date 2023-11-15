def parse_input():
    """
    解析用户输入的线性规划问题。
    返回目标函数的系数、约束系数、常数和约束类型。
    """
    # 用户输入目标函数的系数
    b = [float(x) for x in input("请输入目标函数的系数，用空格分隔: ").split()]

    # 初始化约束列表
    A = []
    c = []
    constraints = []  # 用于存储约束类型 ('<=', '>=', '=')

    while True:
        constraint_input = input("请输入约束条件（例如 '1 2 <= 3'），输入 'end' 或直接回车结束输入: ")

        # 检查是否结束输入
        if constraint_input in ('end', ''):
            break

        # 尝试解析输入的约束条件
        try:
            *coeffs, constraint_type, const = constraint_input.split()
            if constraint_type not in ('<=', '>=', '='):
                raise ValueError("约束类型必须是 '<=', '>=', 或 '='。")
            A.append([float(x) for x in coeffs])
            c.append(float(const))
            constraints.append(constraint_type)
        except ValueError as e:
            print(f"输入错误: {e} 请重新输入。")

    return c, A, b, constraints

