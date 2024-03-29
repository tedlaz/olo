"""Test"""
from collections import namedtuple

from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.views import generic

from utils.distribute import distribute_view
from utils.greek_utils import gr2float, grdate, grnum

from . import models as mdl


class IndexView(generic.ListView):
    template_name = "koi/index.html"
    context_object_name = "koinoxrista_list"

    def get_queryset(self):
        return mdl.Koinoxrista.objects.filter(published=True).order_by("-ekdosi")


class DapanesView(generic.DetailView):
    model = mdl.Koinoxrista
    template_name = "koi/dapanes.html"


def DapanesViewDet(request, koinoxrista_id):
    Gdat = namedtuple("Gdata", "value align")
    koin = get_object_or_404(mdl.Koinoxrista, pk=koinoxrista_id)
    categories = mdl.Category.objects.order_by("id")
    dapanes = koin.dapanes_set.all().order_by("par_date")
    ttot = {}
    gtotal = 0
    for cat in categories:
        ttot[cat.category] = 0.0
    tdi = []
    for dap in dapanes:
        ddi = {
            "t_date": Gdat(grdate(dap.par_date), "center"),
            "t_par": Gdat(dap.par_num, "center"),
            "t_per": Gdat(dap.par_per, "left"),
        }
        for cat in categories:
            ddi[cat.category] = ""
        ddi[dap.category.category] = Gdat(grnum(dap.value), "right")
        ttot[dap.category.category] += float(dap.value)
        gtotal += float(dap.value)
        tdi.append(ddi)
    gtotal = grnum(gtotal)
    ttot = {key: grnum(val) for key, val in ttot.items()}
    return render(
        request,
        "koi/dapanes.html",
        {
            "dapanes": tdi,
            "total": ttot,
            "koin": koin,
            "cats": categories,
            "gtotal": gtotal,
            "clen": len(categories),
        },
    )


def xiliosta_view(request):
    categories = mdl.Category.objects.order_by("id")
    xiliosta = mdl.Xiliosta.objects.order_by("diamerisma")
    tdi = {}
    ttot = {"name": "Σύνολα"}
    for cat in categories:
        ttot[cat.category] = 0
    for xil in xiliosta:
        dname = xil.diamerisma.guest
        ddi = {"name": dname}
        for cat in categories:
            ddi[cat.category] = 0
        tdi[dname] = tdi.get(dname, ddi)
        tdi[dname][xil.category.category] = xil.xiliosta
        ttot[xil.category.category] += xil.xiliosta
    return render(
        request,
        "koi/xiliosta.html",
        {"categories": categories, "xiliosta": tdi, "totals": ttot},
    )


def calc_distribution(koin_id):
    diamer = {i.id: i.guest for i in mdl.Diamerisma.objects.all().order_by("id")}
    categ = {i.id: i.category for i in mdl.Category.objects.all().order_by("id")}
    xiliosta = mdl.Xiliosta.objects.all()
    koin = mdl.Koinoxrista.objects.get(pk=koin_id)
    dap_per_cat = (
        koin.dapanes_set.values("category")
        .order_by("category")
        .annotate(tvalue=Sum("value"))
    )
    header, data, footer = distribute_view(dap_per_cat, xiliosta, diamer, categ)
    return header, data, footer, koin


def distribution(request, koin_id):
    header, data, footer, koin = calc_distribution(koin_id)
    title = f"Κατανομή κοινοχρήστων δαπανών {koin.id}-{grdate(koin.ekdosi)}"

    return render(
        request,
        "koi/katanomi.html",
        {
            "title": title,
            "headers": header,
            "lines": data,
            "footer1": footer,
        },
    )


def apodeijeis(request, apod_id):
    diamerismata = mdl.Diamerisma.objects.all().order_by("id")
    xiliosta = mdl.Xiliosta.objects.all()
    koin = mdl.Koinoxrista.objects.get(pk=apod_id)
    dap = koin.dapanes_set.values()
    cate = [i.id for i in mdl.Category.objects.all().order_by("id")]
    diam = [i.id for i in mdl.Diamerisma.objects.all().order_by("id")]
    fdi = {}
    # Καρτεσιανό γινόμενο διαμερίσματα Χ κατηγορίες με αρχική τιμή 0
    for c in cate:
        for d in diam:
            fdi[(c, d)] = 0
    # Αντικατάσταση με τιμές από τη βάση δεδομένων
    for el in xiliosta:
        fdi[(el.category.id, el.diamerisma.id)] = el.xiliosta
    adi = {
        "headers": ["Ημ/νία", "Παρ/κό", "Περιγραφή", "Ποσό", "Χιλιοστά", "Αναλογούν"]
    }
    adi["diamerismata"] = diamerismata
    adi["koinoxrista"] = koin
    adi["ptitle"] = "Απόδειξη εξώφλησης κοινοχρήστων"
    adi["lines"] = []
    _, data, _, _ = calc_distribution(apod_id)
    totals1 = [i[-1] for i in data]
    for i, diamerisma in enumerate(diamerismata):
        dline = {"diamerisma": diamerisma, "lines": [], "footer": []}
        total = 0
        for dapani in dap:
            xiliosta = fdi[(dapani["category_id"], diamerisma.id)]
            anal = round(xiliosta / 1000 * float(dapani["value"]), 2)
            total = round(total + anal, 2)
            line = [
                {"lcr": "center", "val": dapani["par_date"]},
                {"lcr": "center", "val": dapani["par_num"]},
                {"lcr": "left", "val": dapani["par_per"]},
                {"lcr": "right", "val": dapani["value"]},
                {"lcr": "center", "val": xiliosta},
                {"lcr": "right", "val": grnum(anal)},
            ]
            dline["lines"].append(line)

        dline["footer1"] = [
            {"span": 5, "lcr": "center", "val": "Πληρωτέο ποσό"},
            {"span": 1, "lcr": "right", "val": totals1[i]},
        ]
        if total != 0:
            if abs(total - gr2float(totals1[i])) > 0.05:
                raise ValueError
            adi["lines"].append(dline)

    return render(request, "koi/apodeijeis.html", adi)
