def grdate(dat):
    return f"{dat.day}/{dat.month}/{dat.year}"


def grnum(num):
    if num == 0:
        return ""
    return f"{num:,.2f}".replace(",", "|").replace(".", ",").replace("|", ".")


def gr2float(num):
    return float(num.replace(".", "").replace(",", "."))
