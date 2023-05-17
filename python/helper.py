from sympy import latex, Float, Matrix, preorder_traversal
import re


def round(num, numDecimalPlaces=None):
    if numDecimalPlaces is not None:
        num = float(f"{num:.{numDecimalPlaces}f}")
    return num


def prin_TeX(num, unit, dec=None):
    if dec is not None and dec != "":
        num = round(num, dec)
    print(f"\\SI{{{num}}}{{{unit}}}", end="")


def print_matrix(matrix, th=1e-16, mult=1, dec=""):
    (cols, rows) = matrix.shape
    for i in range(cols):
        for j in range(rows):
            num = matrix[i, j]
            if abs(num) < th:
                print(0)
            else:
                prin_TeX(num * mult, "", dec)
            if j == rows - 1:
                print("\\\\")
            else:
                print("&")


def print_raw_matrix(matrix):
    (cols, rows) = matrix.shape
    for i in range(cols):
        for j in range(rows):
            print(matrix[i, j])
            if j == rows - 1:
                print("\\\\")
            else:
                print("&")


def round_expr(expr, digits):
    for a in preorder_traversal(expr):
        if isinstance(a, Float):
            expr = expr.subs(a, round(a, digits))
    return expr


def my_latex(expr, digits=-1, **kwargs):
    if digits != -1:
        if type(expr) == Matrix:
            (c, r) = expr.shape

            for i in range(c):
                for j in range(r):
                    expr[i, j] = round_expr(expr[i, j], digits)
        else:
            expr = round_expr(expr, digits)

    return re.sub(
        r"\{,\}0(?=\D|$)",
        "",
        latex(
            expr,
            decimal_separator="comma",
            mul_symbol=r"\,",
            full_prec=False,
            **kwargs
        ).replace("frac", "dfrac")
    )


def print_SI_direct(num):
    prin_TeX(num["value"], num["unit"], num["dec"])


def get_printer(V):
    def print_SI_var(num):
        prin_TeX(V[num["name"]], num["unit"], num["dec"])

    return print_SI_var
