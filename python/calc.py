from .data import get_data
from .matrix import ext_matrix, sub_matrix
from sympy.polys.specialpolys import interpolating_poly

import sympy as sp
import numpy as np

PI = np.pi


def get_K_i(I_z, E, L):
    return I_z * E / (L**3) * sp.Matrix([
        [12, 6*L, -12, 6*L],
        [6*L, 4*L**2, -6*L, 2*L**2],
        [-12, -6*L, 12, -6*L],
        [6*L, 2*L**2, -6*L, 4*L**2]
    ])


def get_M_i(rho, A, L):
    return rho * A * L / 420 * sp.Matrix([
        [156, 22*L, 54, -13*L],
        [22*L, 4*L**2, 13*L, -3*L**2],
        [54, 13*L, 156, -22*L],
        [-13*L, -3*L**2, -22*L, 4*L**2]
    ])


def get_alpha_i(K, M, lim=0):
    a = sp.symbols("a")

    poly = (K - a * M).det("berkowitz")

    roots = sp.roots(poly)

    alpha = [x**(1/2) for x in roots]

    return alpha


def calculate(config):
    Data = get_data(config["code"])
    Data["name"] = config["name"]
    Data["neptun"] = config["neptun"]

    a = Data['a']
    b = Data['b']
    c = a + b
    d = Data['d']

    m = Data['m']
    E = Data['E']
    rho = Data['rho']

    code = Data['code']

    parametric = Data['parametric']
    numeric = Data['numeric'](code[1], a, b)

    # Calculate area and second inertia
    A = d**2 * PI / 4
    I_z = d**4 * PI / 64

    # Calculate lengths
    L = {
        2: [b, a],
        3: [b / 2, b / 2, a]
    }

    # Calculate K_i matrices
    K_i = {
        2: [
            get_K_i(I_z, E, L[2][0]),
            get_K_i(I_z, E, L[2][1]),
        ],
        3: [
            get_K_i(I_z, E, L[3][0]),
            get_K_i(I_z, E, L[3][1]),
            get_K_i(I_z, E, L[3][2]),
        ]
    }

    # Calculate global K
    r = {
        2: sp.Matrix(parametric["rods"][2]),
        3: sp.Matrix(parametric["rods"][3]),
    }

    DOF = {
        2: [
            [2*r[2][0, 0]-1, 2*r[2][0, 0], 2*r[2][0, 1]-1, 2*r[2][0, 1]],
            [2*r[2][1, 0]-1, 2*r[2][1, 0], 2*r[2][1, 1]-1, 2*r[2][1, 1]],
        ],
        3: [
            [2*r[3][0, 0]-1, 2*r[3][0, 0], 2*r[3][0, 1]-1, 2*r[3][0, 1]],
            [2*r[3][1, 0]-1, 2*r[3][1, 0], 2*r[3][1, 1]-1, 2*r[3][1, 1]],
            [2*r[3][2, 0]-1, 2*r[3][2, 0], 2*r[3][2, 1]-1, 2*r[3][2, 1]],
        ],
    }

    K = {
        2:
        ext_matrix(K_i[2][0], DOF[2][0], 6)
            + ext_matrix(K_i[2][1], DOF[2][1], 6),
        3:
        ext_matrix(K_i[3][0], DOF[3][0], 8)
            + ext_matrix(K_i[3][1], DOF[3][1], 8)
            + ext_matrix(K_i[3][2], DOF[3][2], 8),
    }

    # Calculate M_i matrices
    M_i = {
        2: [
            get_M_i(rho, A, L[2][0]),
            get_M_i(rho, A, L[2][1]),
        ],
        3: [
            get_M_i(rho, A, L[3][0]),
            get_M_i(rho, A, L[3][1]),
            get_M_i(rho, A, L[3][2]),
        ]
    }

    # Calculate global M
    M = {
        2:
        ext_matrix(M_i[2][0], DOF[2][0], 6)
            + ext_matrix(M_i[2][1], DOF[2][1], 6),
        3:
        ext_matrix(M_i[3][0], DOF[3][0], 8)
            + ext_matrix(M_i[3][1], DOF[3][1], 8)
            + ext_matrix(M_i[3][2], DOF[3][2], 8),
    }

    M_0 = sp.zeros(8, 8)
    M_0[parametric["m_idx"], parametric["m_idx"]] = m
    M_0_param = sp.zeros(8, 8)
    M_0_param[parametric["m_idx"], parametric["m_idx"]] = sp.symbols("m_0")

    M_d = []
    for i in range(3):
        M_d.append((lambda L: rho * A * L[i] / 2 * sp.Matrix([
            [1, 0, 0, 0],
            [0, L[i]**2/12, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, L[i]**2/12]]
        ))(L[3]))

    M_e = ext_matrix(
        M_d[0], DOF[3][0], 8
    ) + ext_matrix(
        M_d[1], DOF[3][1], 8
    ) + ext_matrix(
        M_d[2], DOF[3][2], 8
    )

    M["a"] = M[2]
    M["b"] = M[3]
    M["c"] = M[3] + M_0
    M["d"] = M_e + M_0
    # Calculate alpha
    free = parametric["free"]

    K_kond = {
        2: sub_matrix(K[2], free[2]),
        3: sub_matrix(K[3], free[3]),
    }
    M_kond = {
        "a": sub_matrix(M["a"], free[2]),
        "b": sub_matrix(M["b"], free[3]),
        "c": sub_matrix(M["c"], free[3]),
        "d": sub_matrix(M["d"], free[3]),
    }

    alpha = {
        "a": get_alpha_i(K_kond[2], M_kond["a"], lim=3),
        "b": get_alpha_i(K_kond[3], M_kond["b"], lim=4),
        "c": get_alpha_i(K_kond[3], M_kond["c"], lim=5),
        "d": get_alpha_i(K_kond[3], M_kond["d"], lim=5),
    }

    f = {
        "a": [a / 2 / PI for a in alpha["a"]],
        "b": [a / 2 / PI for a in alpha["b"]],
        "c": [a / 2 / PI for a in alpha["c"]],
        "d": [a / 2 / PI for a in alpha["d"]],
    }

    # Merge newly created variables with original variables
    Merger = {
        "parametric": parametric,
        "numeric": numeric,
        "c": c,
        "hb": b / 2,

        "A": A,
        "I": I_z,
        "L": L,

        "DOF": DOF,

        "K_i": K_i,
        "K": K,
        "K_kond": K_kond,

        "M_i": M_i,
        "M": M,
        "M_0": M_0,
        "M_0_param": M_0_param,
        "M_d": M_d,
        "M_e": M_e,
        "M_kond": M_kond,

        "alpha": alpha,
        "f": f,
    }

    for k, v in Merger.items():
        Data[k] = v

    # Return variables
    return Data

# # KU = F equation
# v_1, v_2, v_3, v_4 = sp.symbols(
#     "v_1, v_2, v_3, v_4"
# )
# phi_1, phi_2, phi_3, phi_4 = sp.symbols(
#     "\\varphi_1, \\varphi_2, \\varphi_3, \\varphi_4"
# )
# F_1, F_2, F_3, F_4 = sp.symbols(
#     "F_1, F_2, F_3, F_3"
# )
# M_1, M_2, M_3, M_4 = sp.symbols(
#     "M_1, M_2, M_3, M_4"
# )
#
# U_sym = {
#     2: sp.Matrix([
#         [v_1], [phi_1],
#         [v_2], [phi_2],
#         [v_3], [phi_3],
#     ]),
#     3: sp.Matrix([
#         [v_1], [phi_1],
#         [v_2], [phi_2],
#         [v_3], [phi_3],
#         [v_4], [phi_4],
#     ])
# }
# F_sym = {
#     2: sp.Matrix([
#         [F_1], [M_1],
#         [F_2], [M_2],
#         [F_3], [M_3],
#     ]),
#     3: sp.Matrix([
#         [F_1], [M_1],
#         [F_2], [M_2],
#         [F_3], [M_3],
#         [F_4], [M_4],
#     ])
# }
