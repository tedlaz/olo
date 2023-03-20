def distribute(val: float, dist_array: list[int]):
    """
    input parameters:
    val       : Decimal value for distribution
    distArray : Distribution Array
    decimals  : Number of decimal digits
    """
    res = []
    val = round(val, 2)
    tar = sum(dist_array)

    for elm in dist_array:
        res.append(round(val * elm / tar, 2))
    nval = round(sum(res), 2)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max value Element gets the difference
        max_index = res.index(max(res))
        res[max_index] = round(res[max_index] + dif, 2)
    return tuple(res)


def distribute_many(data: list[dict]):
    res = {}
    for line in data:
        res[line["cat"]] = distribute(line["val"], line["dist_array"])
    return res


def distr(values: dict, xiliosta: dict):
    vals = {}
    tcat = {}
    tdia = {}
    total = 0
    for cat_dia, xil in xiliosta.items():
        cat, dia = cat_dia
        vals[cat_dia] = round(xil * values.get(cat, 0) / 1000, 2)
        tcat[cat] = round(tcat.get(cat, 0) + vals[cat_dia], 2)
        tdia[dia] = round(tdia.get(dia, 0) + vals[cat_dia], 2)
        total = round(total + vals[cat_dia], 2)
    lines = []
    for diamerisma_id, diamerisma_total in tdia.items():
        lin = [diamerisma_id]
        for category_id, _ in tcat.items():
            lin.append(vals[(category_id, diamerisma_id)])
        lin.append(diamerisma_total)
        lines.append(lin)
    return lines, tcat, total


if __name__ == "__main__":
    print(distribute(171.39, [0, 204, 159, 243, 120, 274]))
    print(distribute(149.15, [0, 139, 108, 249, 122, 382]))
    print(
        distribute_many(
            [
                {"cat": 1, "val": 171.39, "dist_array": (0, 204, 159, 243, 120, 274)},
                {"cat": 2, "val": 149.15, "dist_array": (0, 139, 108, 249, 122, 382)},
            ]
        )
    )
