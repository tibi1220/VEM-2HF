Data = {
    # Non specific info about construction
    "parametric": {
        1: {
            "wall": "a",
            "mass": "b",
            "m_idx": 4,
            "pivot": "c",
            "rods": {
                2: [[1, 2], [2, 3]],
                3: [[1, 2], [2, 3], [3, 4]],
            },
            "free": {
                2: [3, 4, 6],
                3: [3, 4, 5, 6, 8],
            },
            "not_free": {
                2: [1, 2, 5],
                22: {
                    "pv": 3,
                    "wv": 1,
                    "wphi": 1,
                },
                3: [1, 2, 7],
                33: {
                    "pv": 4,
                    "wv": 1,
                    "wphi": 1,
                },
            },
        },
        2: {
            "wall": "a",
            "mass": "c",
            "m_idx": 6,
            "pivot": "b",
            "rods": {
                2: [[1, 2], [2, 3]],
                3: [[1, 2], [2, 3], [3, 4]],
            },
            "free": {
                2: [4, 5, 6],
                3: [3, 4, 6, 7, 8],
            },
            "not_free": {
                2: [1, 2, 3],
                22: {
                    "pv": 2,
                    "wv": 1,
                    "wphi": 1,
                },
                3: [1, 2, 5],
                33: {
                    "pv": 3,
                    "wv": 1,
                    "wphi": 1,
                },
            },
        },
        3: {
            "wall": "c",
            "mass": "b",
            "m_idx": 4,
            "pivot": "a",
            "rods": {
                2: [[1, 2], [2, 3]],
                3: [[1, 2], [2, 3], [3, 4]],
            },
            "free": {
                2: [2, 3, 4],
                3: [2, 3, 4, 5, 6],
            },
            "not_free": {
                2: [1, 5, 6],
                22: {
                    "pv": 1,
                    "wv": 3,
                    "wphi": 3,
                },
                3: [1, 7, 8],
                33: {
                    "pv": 1,
                    "wv": 4,
                    "wphi": 4,
                },
            },
        },
        4: {
            "wall": "c",
            "mass": "a",
            "m_idx": 0,
            "pivot": "b",
            "rods": {
                2: [[1, 2], [2, 3]],
                3: [[1, 2], [2, 3], [3, 4]],
            },
            "free": {
                2: [1, 2, 4],
                3: [1, 2, 3, 4, 6],
            },
            "not_free": {
                2: [3, 5, 6],
                22: {
                    "pv": 2,
                    "wv": 3,
                    "wphi": 3,
                },
                3: [3, 7, 8],
                33: {
                    "pv": 3,
                    "wv": 4,
                    "wphi": 4,
                },
            },
        },
    },

    # Specific info about construction
    "numeric": lambda code, a, b: {
        1: {
            "wall": 0,
            "mass": b,
            "pivot": a+b,
        },
        2: {
            "wall": 0,
            "mass": a+b,
            "pivot": b,
        },
        3: {
            "wall": a+b,
            "mass": b,
            "pivot": 0,
        },
        4: {
            "wall": a+b,
            "mass": 0,
            "pivot": b,
        },
    }[code],

    # Dimensions
    "a": [1.2, 1.7, 2.1, 2.6],  # m
    "b": [5, 6, 7, 8],  # m
    "d": [25, 35, 45, 55],  # mm

    "m": [15, 20, 25, 30],  # kg
    "E": [170, 190, 210, 230],  # GPa
    "rho": [6000, 6500, 7000, 7500],  # kg/m3
}


def get_data(code):
    return {
        # A -- code 1
        "parametric": Data["parametric"][code[1]],
        "numeric": Data["numeric"],

        # B -- code 2
        "a": Data["a"][code[2]-1],
        "m": Data["m"][code[2]-1],

        # C -- code 3
        "b": Data["b"][code[3]-1],
        "d": Data["d"][code[3]-1] / 1_000,

        # D -- code 4
        "E": Data["E"][code[4]-1] * 1_000_000_000,
        "rho": Data["rho"][code[4]-1],

        # Code information
        "code": code,
    }
