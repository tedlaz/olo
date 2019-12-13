import decimal
from collections import namedtuple


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """
    Always returns a decimal number. If poso is not a number or None
    returns dec(0)

    :param poso: Mumber in any format (string, float, int, ...)
    :param decimals: Number of decimals (default 2)
    :return: A decimal number rounded to decimals parameter
    """
    if poso is None:
        poso = 0
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(poso)
    else:
        tmp = decimal.Decimal('0')
    # in case of tmp = -0.00 to remove negative sign
    if tmp == decimal.Decimal(0):
        tmp = decimal.Decimal(0)
    return tmp.quantize(PLACES)


def distribute(val, distArray, decimals=2):
    """
    input parameters:
    val       : Decimal value for distribution
    distArray : Distribution Array
    decimals  : Number of decimal digits
    """
    tmpArr = []
    val = dec(val, decimals)
    try:
        tar = dec(sum(distArray), decimals)
    except Exception:
        return tmpArr
    for el in distArray:
        tmpArr.append(dec(val * dec(el, decimals) / tar, decimals))
    nval = sum(tmpArr)
    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max value Element gets the difference
        tmpArr[tmpArr.index(max(tmpArr))] += dif
    return tmpArr


def distr(values, xiliosta):
    vals = {}
    tcat = {}
    tdia = {}
    total = 0
    for cat_dia, xil in xiliosta.items():
        cat, dia = cat_dia
        vals[cat_dia] = xil * values.get(cat, 0) / 1000
        tcat[cat] = tcat.get(cat, 0) + vals[cat_dia]
        tdia[dia] = tdia.get(dia, 0) + vals[cat_dia]
        total += vals[cat_dia]
    lines = []
    for diamerisma_id, diamerisma_total in tdia.items():
        lin = [diamerisma_id]
        for category_id, category_total in tcat.items():
            lin.append(vals[(category_id, diamerisma_id)])
        lin.append(diamerisma_total)
        lines.append(lin)
    return lines, tcat, total
