

def Det(matrix):
    """
    Calculate the determinant of a matrix using recursion.

    Args:
    matrix (list of lists of floats): A square matrix.

    Returns:
    float: The determinant of the matrix.
    """

    if len(matrix) == 1:
        return matrix[0][0]

    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(len(matrix)):
        sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]

        det += ((-1) ** c) * matrix[0][c] * Det(sub_matrix)

    return det
