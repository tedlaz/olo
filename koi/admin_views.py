from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CategoryForm,
    DapanesForm,
    DapanesFormSet,
    DiamerismaForm,
    DiaxeiristisForm,
    KoinoxristaForm,
    XiliostaForm,
)
from .models import Category, Dapanes, Diamerisma, Diaxeiristis, Koinoxrista, Xiliosta


# Dashboard view
@login_required
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    context = {
        "total_diamerismata": Diamerisma.objects.count(),
        "total_categories": Category.objects.count(),
        "total_koinoxrista": Koinoxrista.objects.count(),
        "total_dapanes": Dapanes.objects.count(),
        "total_diaxeiristes": Diaxeiristis.objects.count(),
        "total_xiliosta": Xiliosta.objects.count(),
        "recent_koinoxrista": Koinoxrista.objects.order_by("-ekdosi")[:5],
        "recent_dapanes": Dapanes.objects.order_by("-par_date")[:5],
        "dapanes_sum": Dapanes.objects.aggregate(total=Sum("value"))["total"] or 0,
    }
    return render(request, "koi/admin/dashboard.html", context)


# ============== Category CRUD ==============
@login_required
def category_list(request):
    search = request.GET.get("search", "")
    categories = Category.objects.all()
    if search:
        categories = categories.filter(category__icontains=search)

    paginator = Paginator(categories, 10)
    page = request.GET.get("page", 1)
    categories = paginator.get_page(page)

    return render(
        request,
        "koi/admin/category_list.html",
        {"categories": categories, "search": search},
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Η κατηγορία δημιουργήθηκε επιτυχώς!")
            return redirect("koi:admin_category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "koi/admin/category_form.html",
        {"form": form, "title": "Νέα Κατηγορία", "action": "Δημιουργία"},
    )


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Η κατηγορία ενημερώθηκε επιτυχώς!")
            return redirect("koi:admin_category_list")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "koi/admin/category_form.html",
        {
            "form": form,
            "title": "Επεξεργασία Κατηγορίας",
            "action": "Αποθήκευση",
            "object": category,
        },
    )


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Η κατηγορία διαγράφηκε επιτυχώς!")
        return redirect("koi:admin_category_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": category,
            "object_name": "Κατηγορία",
            "cancel_url": "koi:admin_category_list",
        },
    )


# ============== Diamerisma CRUD ==============
@login_required
def diamerisma_list(request):
    search = request.GET.get("search", "")
    diamerismata = Diamerisma.objects.all()
    if search:
        diamerismata = diamerismata.filter(
            Q(name__icontains=search)
            | Q(owner__icontains=search)
            | Q(guest__icontains=search)
        )

    paginator = Paginator(diamerismata, 10)
    page = request.GET.get("page", 1)
    diamerismata = paginator.get_page(page)

    return render(
        request,
        "koi/admin/diamerisma_list.html",
        {"diamerismata": diamerismata, "search": search},
    )


@login_required
def diamerisma_create(request):
    if request.method == "POST":
        form = DiamerismaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Το διαμέρισμα δημιουργήθηκε επιτυχώς!")
            return redirect("koi:admin_diamerisma_list")
    else:
        form = DiamerismaForm()

    return render(
        request,
        "koi/admin/diamerisma_form.html",
        {"form": form, "title": "Νέο Διαμέρισμα", "action": "Δημιουργία"},
    )


@login_required
def diamerisma_edit(request, pk):
    diamerisma = get_object_or_404(Diamerisma, pk=pk)
    if request.method == "POST":
        form = DiamerismaForm(request.POST, instance=diamerisma)
        if form.is_valid():
            form.save()
            messages.success(request, "Το διαμέρισμα ενημερώθηκε επιτυχώς!")
            return redirect("koi:admin_diamerisma_list")
    else:
        form = DiamerismaForm(instance=diamerisma)

    return render(
        request,
        "koi/admin/diamerisma_form.html",
        {
            "form": form,
            "title": "Επεξεργασία Διαμερίσματος",
            "action": "Αποθήκευση",
            "object": diamerisma,
        },
    )


@login_required
def diamerisma_delete(request, pk):
    diamerisma = get_object_or_404(Diamerisma, pk=pk)
    if request.method == "POST":
        diamerisma.delete()
        messages.success(request, "Το διαμέρισμα διαγράφηκε επιτυχώς!")
        return redirect("koi:admin_diamerisma_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": diamerisma,
            "object_name": "Διαμέρισμα",
            "cancel_url": "koi:admin_diamerisma_list",
        },
    )


# ============== Diaxeiristis CRUD ==============
@login_required
def diaxeiristis_list(request):
    search = request.GET.get("search", "")
    diaxeiristes = Diaxeiristis.objects.all()
    if search:
        diaxeiristes = diaxeiristes.filter(name__icontains=search)

    paginator = Paginator(diaxeiristes, 10)
    page = request.GET.get("page", 1)
    diaxeiristes = paginator.get_page(page)

    return render(
        request,
        "koi/admin/diaxeiristis_list.html",
        {"diaxeiristes": diaxeiristes, "search": search},
    )


@login_required
def diaxeiristis_create(request):
    if request.method == "POST":
        form = DiaxeiristisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ο διαχειριστής δημιουργήθηκε επιτυχώς!")
            return redirect("koi:admin_diaxeiristis_list")
    else:
        form = DiaxeiristisForm()

    return render(
        request,
        "koi/admin/diaxeiristis_form.html",
        {"form": form, "title": "Νέος Διαχειριστής", "action": "Δημιουργία"},
    )


@login_required
def diaxeiristis_edit(request, pk):
    diaxeiristis = get_object_or_404(Diaxeiristis, pk=pk)
    if request.method == "POST":
        form = DiaxeiristisForm(request.POST, instance=diaxeiristis)
        if form.is_valid():
            form.save()
            messages.success(request, "Ο διαχειριστής ενημερώθηκε επιτυχώς!")
            return redirect("koi:admin_diaxeiristis_list")
    else:
        form = DiaxeiristisForm(instance=diaxeiristis)

    return render(
        request,
        "koi/admin/diaxeiristis_form.html",
        {
            "form": form,
            "title": "Επεξεργασία Διαχειριστή",
            "action": "Αποθήκευση",
            "object": diaxeiristis,
        },
    )


@login_required
def diaxeiristis_delete(request, pk):
    diaxeiristis = get_object_or_404(Diaxeiristis, pk=pk)
    if request.method == "POST":
        diaxeiristis.delete()
        messages.success(request, "Ο διαχειριστής διαγράφηκε επιτυχώς!")
        return redirect("koi:admin_diaxeiristis_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": diaxeiristis,
            "object_name": "Διαχειριστής",
            "cancel_url": "koi:admin_diaxeiristis_list",
        },
    )


# ============== Koinoxrista CRUD ==============
@login_required
def koinoxrista_list(request):
    search = request.GET.get("search", "")
    published = request.GET.get("published", "")
    koinoxrista = Koinoxrista.objects.all().order_by("-ekdosi")

    if search:
        koinoxrista = koinoxrista.filter(
            Q(sxolia__icontains=search) | Q(diaxeiristis__name__icontains=search)
        )
    if published:
        koinoxrista = koinoxrista.filter(published=(published == "true"))

    paginator = Paginator(koinoxrista, 10)
    page = request.GET.get("page", 1)
    koinoxrista = paginator.get_page(page)

    return render(
        request,
        "koi/admin/koinoxrista_list.html",
        {"koinoxrista_list": koinoxrista, "search": search, "published": published},
    )


@login_required
def koinoxrista_create(request):
    if request.method == "POST":
        form = KoinoxristaForm(request.POST)
        formset = DapanesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            koinoxrista = form.save()
            formset.instance = koinoxrista
            formset.save()
            messages.success(request, "Τα κοινόχρηστα δημιουργήθηκαν επιτυχώς!")
            return redirect("koi:admin_koinoxrista_list")
    else:
        form = KoinoxristaForm()
        formset = DapanesFormSet()

    return render(
        request,
        "koi/admin/koinoxrista_form.html",
        {
            "form": form,
            "formset": formset,
            "title": "Νέα Κοινόχρηστα",
            "action": "Δημιουργία",
        },
    )


@login_required
def koinoxrista_edit(request, pk):
    koinoxrista = get_object_or_404(Koinoxrista, pk=pk)
    if request.method == "POST":
        form = KoinoxristaForm(request.POST, instance=koinoxrista)
        formset = DapanesFormSet(request.POST, instance=koinoxrista)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Τα κοινόχρηστα ενημερώθηκαν επιτυχώς!")
            return redirect("koi:admin_koinoxrista_list")
    else:
        form = KoinoxristaForm(instance=koinoxrista)
        formset = DapanesFormSet(instance=koinoxrista)

    return render(
        request,
        "koi/admin/koinoxrista_form.html",
        {
            "form": form,
            "formset": formset,
            "title": "Επεξεργασία Κοινοχρήστων",
            "action": "Αποθήκευση",
            "object": koinoxrista,
        },
    )


@login_required
def koinoxrista_delete(request, pk):
    koinoxrista = get_object_or_404(Koinoxrista, pk=pk)
    if request.method == "POST":
        koinoxrista.delete()
        messages.success(request, "Τα κοινόχρηστα διαγράφηκαν επιτυχώς!")
        return redirect("koi:admin_koinoxrista_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": koinoxrista,
            "object_name": "Κοινόχρηστα",
            "cancel_url": "koi:admin_koinoxrista_list",
        },
    )


# ============== Xiliosta CRUD ==============
@login_required
def xiliosta_list(request):
    search = request.GET.get("search", "")
    xiliosta = Xiliosta.objects.all().select_related("diamerisma", "category")

    if search:
        xiliosta = xiliosta.filter(
            Q(diamerisma__name__icontains=search)
            | Q(category__category__icontains=search)
        )

    paginator = Paginator(xiliosta, 15)
    page = request.GET.get("page", 1)
    xiliosta = paginator.get_page(page)

    return render(
        request,
        "koi/admin/xiliosta_list.html",
        {"xiliosta_list": xiliosta, "search": search},
    )


@login_required
def xiliosta_create(request):
    if request.method == "POST":
        form = XiliostaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Τα χιλιοστά δημιουργήθηκαν επιτυχώς!")
            return redirect("koi:admin_xiliosta_list")
    else:
        form = XiliostaForm()

    return render(
        request,
        "koi/admin/xiliosta_form.html",
        {"form": form, "title": "Νέα Χιλιοστά", "action": "Δημιουργία"},
    )


@login_required
def xiliosta_edit(request, pk):
    xiliosta = get_object_or_404(Xiliosta, pk=pk)
    if request.method == "POST":
        form = XiliostaForm(request.POST, instance=xiliosta)
        if form.is_valid():
            form.save()
            messages.success(request, "Τα χιλιοστά ενημερώθηκαν επιτυχώς!")
            return redirect("koi:admin_xiliosta_list")
    else:
        form = XiliostaForm(instance=xiliosta)

    return render(
        request,
        "koi/admin/xiliosta_form.html",
        {
            "form": form,
            "title": "Επεξεργασία Χιλιοστών",
            "action": "Αποθήκευση",
            "object": xiliosta,
        },
    )


@login_required
def xiliosta_delete(request, pk):
    xiliosta = get_object_or_404(Xiliosta, pk=pk)
    if request.method == "POST":
        xiliosta.delete()
        messages.success(request, "Τα χιλιοστά διαγράφηκαν επιτυχώς!")
        return redirect("koi:admin_xiliosta_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": xiliosta,
            "object_name": "Χιλιοστά",
            "cancel_url": "koi:admin_xiliosta_list",
        },
    )


# ============== Dapanes CRUD ==============
@login_required
def dapanes_list(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    dapanes = (
        Dapanes.objects.all()
        .select_related("koinoxrista", "category")
        .order_by("-par_date")
    )

    if search:
        dapanes = dapanes.filter(
            Q(par_per__icontains=search) | Q(par_num__icontains=search)
        )
    if category:
        dapanes = dapanes.filter(category_id=category)

    categories = Category.objects.all()

    paginator = Paginator(dapanes, 15)
    page = request.GET.get("page", 1)
    dapanes = paginator.get_page(page)

    return render(
        request,
        "koi/admin/dapanes_list.html",
        {
            "dapanes_list": dapanes,
            "search": search,
            "categories": categories,
            "selected_category": category,
        },
    )


@login_required
def dapanes_create(request):
    if request.method == "POST":
        form = DapanesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Η δαπάνη δημιουργήθηκε επιτυχώς!")
            return redirect("koi:admin_dapanes_list")
    else:
        form = DapanesForm()

    return render(
        request,
        "koi/admin/dapanes_form.html",
        {"form": form, "title": "Νέα Δαπάνη", "action": "Δημιουργία"},
    )


@login_required
def dapanes_edit(request, pk):
    dapanes = get_object_or_404(Dapanes, pk=pk)
    if request.method == "POST":
        form = DapanesForm(request.POST, instance=dapanes)
        if form.is_valid():
            form.save()
            messages.success(request, "Η δαπάνη ενημερώθηκε επιτυχώς!")
            return redirect("koi:admin_dapanes_list")
    else:
        form = DapanesForm(instance=dapanes)

    return render(
        request,
        "koi/admin/dapanes_form.html",
        {
            "form": form,
            "title": "Επεξεργασία Δαπάνης",
            "action": "Αποθήκευση",
            "object": dapanes,
        },
    )


@login_required
def dapanes_delete(request, pk):
    dapanes = get_object_or_404(Dapanes, pk=pk)
    if request.method == "POST":
        dapanes.delete()
        messages.success(request, "Η δαπάνη διαγράφηκε επιτυχώς!")
        return redirect("koi:admin_dapanes_list")

    return render(
        request,
        "koi/admin/confirm_delete.html",
        {
            "object": dapanes,
            "object_name": "Δαπάνη",
            "cancel_url": "koi:admin_dapanes_list",
        },
    )
