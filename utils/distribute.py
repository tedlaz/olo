from .greek_utils import grnum


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


def get_list_of_dist(xiliosta: dict, category_id, diamerismata_ids):
    xiliosta_cat = []
    # diamerismata_cat = []
    for diam_id in diamerismata_ids:
        value = 0
        for xil in xiliosta:
            if category_id == xil.category.id and diam_id == xil.diamerisma.id:
                value = xil.xiliosta
        # diamerismata_cat.append(diam_id)
        xiliosta_cat.append(value)
    return xiliosta_cat


def create_matrix(diamerismata_ids, categories_ids, distr_per_cat):
    header = ["Διαμέρισμα"] + list(categories_ids.values()) + ["Σύνολο"]
    matrix = []
    footer = ["Σύνολα"] + [0 for _ in categories_ids.keys()]
    for i, diamerisma_id in enumerate(diamerismata_ids.keys()):
        line = [diamerismata_ids[diamerisma_id]]
        for j, cat_id in enumerate(categories_ids.keys()):
            if cat_id in distr_per_cat.keys():
                line.append(distr_per_cat[cat_id][i])
                footer[j + 1] = round(footer[j + 1] + distr_per_cat[cat_id][i], 2)
            else:
                line.append(0)
        line.append(round(sum(line[1:]), 2))
        matrix.append(line)
    footer.append(round(sum(footer[1:]), 2))
    fmatrix = [format2gr(i, 1) for i in matrix]
    ffooter = format2gr(footer, 1)
    return header, fmatrix, ffooter


def format2gr(arr: list, from_index: int):
    return arr[:from_index] + [grnum(i) for i in arr[from_index:]]


def distribute_view(dapanes_ana_katigoria, xiliosta, diamerismata_ids, categories_ids):
    distr_per_cat = {}
    for line in dapanes_ana_katigoria:
        category_id = line["category"]
        value = float(line["tvalue"])
        xiliosta_kat = get_list_of_dist(xiliosta, category_id, diamerismata_ids.keys())
        distr_per_cat[category_id] = distribute(value, xiliosta_kat)
    return create_matrix(diamerismata_ids, categories_ids, distr_per_cat)


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
