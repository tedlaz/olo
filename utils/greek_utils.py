def grdate(dat):
    return f'{dat.day}/{dat.month}/{dat.year}'


def grnum(num):
    if num == 0:
        return ''
    return f'{num:,.2f}'.replace(',', '|').replace('.', ',').replace('|', '.')
