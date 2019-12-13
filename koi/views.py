"""Test"""
from collections import namedtuple
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Sum
from utils.greek_utils import grdate, grnum
from utils.distribute import distr
from . import models as mdl


class IndexView(generic.ListView):
    template_name = 'koi/index.html'
    context_object_name = 'koinoxrista_list'

    def get_queryset(self):
        return mdl.Koinoxrista.objects.order_by('-ekdosi')


class DapanesView(generic.DetailView):
    model = mdl.Koinoxrista
    template_name = 'koi/dapanes.html'


def DapanesViewDet(request, koinoxrista_id):
    Gdat = namedtuple('Gdata', 'value align')
    koin = get_object_or_404(mdl.Koinoxrista, pk=koinoxrista_id)
    categories = mdl.Category.objects.order_by('id')
    dapanes = koin.dapanes_set.all().order_by('par_date')
    ttot = {}
    gtotal = 0
    for cat in categories:
        ttot[cat.category] = 0.0
    tdi = []
    for dap in dapanes:
        ddi = {'t_date': Gdat(grdate(dap.par_date), 'center'),
               't_par': Gdat(dap.par_num, 'center'),
               't_per': Gdat(dap.par_per, 'left')}
        for cat in categories:
            ddi[cat.category] = ''
        ddi[dap.category.category] = Gdat(grnum(dap.value), 'right')
        ttot[dap.category.category] += float(dap.value)
        gtotal += float(dap.value)
        tdi.append(ddi)
    gtotal = grnum(gtotal)
    ttot = {key: grnum(val) for key, val in ttot.items()}
    return render(request,
                  'koi/dapanes.html',
                  {'dapanes': tdi,
                   'total': ttot,
                   'koin': koin,
                   'cats': categories,
                   'gtotal': gtotal,
                   'clen': len(categories)})


def xiliosta_view(request):
    categories = mdl.Category.objects.order_by('id')
    xiliosta = mdl.Xiliosta.objects.order_by('diamerisma')
    tdi = {}
    ttot = {'name': 'Σύνολα'}
    for cat in categories:
        ttot[cat.category] = 0
    for xil in xiliosta:
        dname = xil.diamerisma.guest
        ddi = {'name': dname}
        for cat in categories:
            ddi[cat.category] = 0
        tdi[dname] = tdi.get(dname, ddi)
        tdi[dname][xil.category.category] = xil.xiliosta
        ttot[xil.category.category] += xil.xiliosta
    return render(request,
                  'koi/xiliosta.html',
                  {'categories': categories, 'xiliosta': tdi, 'totals': ttot})


def distribution(request, koin_id):
    diam = [i.id for i in mdl.Diamerisma.objects.all().order_by('id')]
    cate = [i.id for i in mdl.Category.objects.all().order_by('id')]
    xiliosta = mdl.Xiliosta.objects.all()
    koin = mdl.Koinoxrista.objects.get(pk=koin_id)
    dap = koin.dapanes_set.values('category').order_by(
        'category').annotate(tprice=Sum('value'))
    fposa = {}
    for el in dap:
        fposa[el['category']] = float(el['tprice'])
    fdi = {}
    # Καρτεσιανό γινόμενο διαμερίσματα Χ κατηγορίες με αρχική τιμή 0
    for c in cate:
        for d in diam:
            fdi[(c, d)] = 0
    # Αντικατάσταση με τιμές από τη βάση δεδομένων
    for el in xiliosta:
        fdi[(el.category.id, el.diamerisma.id)] = el.xiliosta
    rlines, total_categories, gtotal = distr(fposa, fdi)
    title = f'Κατανομή κοινοχρήστων δαπανών της {grdate(koin.ekdosi)}'
    hcat = [i.category for i in mdl.Category.objects.all().order_by('id')]
    ddiam = {i.id: i.guest for i in mdl.Diamerisma.objects.all().order_by('id')}
    headers = ['Διαμερίσματα'] + hcat + ['Σύνολο']
    lines = []
    for line in rlines:
        lin = [{'val': ddiam[line[0]], 'lcr': 'left'}]
        for col in line[1:]:
            lin.append({'val': grnum(col), 'lcr': 'right'})
        lines.append(lin)
    footer1 = [{'span': 1, 'lcr': 'center', 'val': 'Σύνολα'}]
    for col in total_categories:
        footer1.append({'span': 1, 'lcr': 'right',
                        'val': grnum(total_categories[col])})
    footer1.append({'span': 1, 'lcr': 'right', 'val': grnum(gtotal)})
    # lines = [
    #     [
    #         {'lcr': 'left', 'val': 'Διαμ1'},
    #         {'lcr': 'right', 'val': '100,26'},
    #         {'lcr': 'right', 'val': '34,56'}
    #     ],
    #     [
    #         {'lcr': 'left', 'val': 'Διαμ2'},
    #         {'lcr': 'right', 'val': '200,00'},
    #         {'lcr': 'right', 'val': '65,44'}
    #     ]
    # ]
    # footer1 = [
    #     {'span': 1, 'lcr': 'center', 'val': 'Σύνολα'},
    #     {'span': 1, 'lcr': 'right', 'val': '442,56'},
    #     {'span': 1, 'lcr': 'right', 'val': '788,89'},
    # ]
    # footer2 = [
    #     {'span': 1, 'lcr': 'center', 'val': 'Γενικό σύνολο'},
    #     {'span': 2, 'lcr': 'center', 'val': '1256,68'},
    # ]
    return render(
        request,
        'koi/katanomi.html',
        {
            'title': title,
            'headers': headers,
            'lines': lines,
            'footer1': footer1,
        }
    )


def apodeijeis(request, apod_id):
    diamerismata = mdl.Diamerisma.objects.all().order_by('id')
    xiliosta = mdl.Xiliosta.objects.all()
    koin = mdl.Koinoxrista.objects.get(pk=apod_id)
    dap = koin.dapanes_set.values()
    cate = [i.id for i in mdl.Category.objects.all().order_by('id')]
    diam = [i.id for i in mdl.Diamerisma.objects.all().order_by('id')]
    fdi = {}
    # Καρτεσιανό γινόμενο διαμερίσματα Χ κατηγορίες με αρχική τιμή 0
    for c in cate:
        for d in diam:
            fdi[(c, d)] = 0
    # Αντικατάσταση με τιμές από τη βάση δεδομένων
    for el in xiliosta:
        fdi[(el.category.id, el.diamerisma.id)] = el.xiliosta
    adi = {'headers': ['Ημ/νία', 'Παρ/κό',
                       'Περιγραφή', 'Ποσό', 'Χιλιοστά', 'Αναλογούν']}
    adi['diamerismata'] = diamerismata
    adi['koinoxrista'] = koin
    adi['ptitle'] = 'Απόδειξη εξώφλησης κοινοχρήστων'
    adi['lines'] = []
    for diamerisma in diamerismata:
        dline = {'diamerisma': diamerisma, 'lines': [], 'footer': []}
        total = 0
        for dapani in dap:
            xiliosta = fdi[(dapani['category_id'], diamerisma.id)]
            anal = xiliosta / 1000 * float(dapani['value'])
            total += anal
            line = [
                {'lcr': 'center', 'val': dapani['par_date']},
                {'lcr': 'center', 'val': dapani['par_num']},
                {'lcr': 'left', 'val': dapani['par_per']},
                {'lcr': 'right', 'val': dapani['value']},
                {'lcr': 'center', 'val': xiliosta},
                {'lcr': 'right', 'val': grnum(anal)},
            ]
            dline['lines'].append(line)

        dline['footer1'] = [
            {'span': 5, 'lcr': 'center', 'val': 'Πληρωτέο ποσό'},
            {'span': 1, 'lcr': 'right', 'val': grnum(total)},
        ]
        if total != 0:
            adi['lines'].append(dline)

    return render(request, 'koi/apodeijeis.html', adi)
