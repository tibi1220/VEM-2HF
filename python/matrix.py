import sympy as sp


def sub_matrix(Mx, rows):
    n = len(rows)
    mx = sp.zeros(n, n)

    for i in range(n):
        for j in range(n):
            mx[i, j] = Mx[rows[i]-1, rows[j]-1]

    return mx


def ext_matrix(mx, rows, size):
    n = len(rows)
    Mx = sp.zeros(size, size)

    for i in range(n):
        for j in range(n):
            Mx[rows[i]-1, rows[j]-1] = mx[i, j]

    return Mx


def sub_vector(Vec, rows):
    n = len(rows)
    vec = sp.zeros(n, 1)

    for i in range(n):
        vec[i, 0] = Vec[rows[i]-1, 0]

    return vec


def ext_vector(vec, rows, size):
    n = len(rows)
    Vec = sp.zeros(size, 1)

    for i in range(n):
        Vec[rows[i]-1, 0] = vec[i, 0]

    return Vec
