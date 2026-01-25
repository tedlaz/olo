from django.urls import path

from . import admin_views, views

app_name = "koi"
urlpatterns = [
    # Public views
    path("", views.IndexView.as_view(), name="index"),
    path("<int:koinoxrista_id>/", views.DapanesViewDet, name="dapanes"),
    path("<int:koin_id>/dist", views.distribution, name="katanomi"),
    path("xiliosta/", views.xiliosta_view, name="xiliosta"),
    path("<int:apod_id>/apodeijeis/", views.apodeijeis, name="apodeijeis"),
    # Custom Admin Dashboard
    path("manage/", admin_views.admin_dashboard, name="admin_dashboard"),
    # Category Admin
    path("manage/categories/", admin_views.category_list, name="admin_category_list"),
    path(
        "manage/categories/create/",
        admin_views.category_create,
        name="admin_category_create",
    ),
    path(
        "manage/categories/<int:pk>/edit/",
        admin_views.category_edit,
        name="admin_category_edit",
    ),
    path(
        "manage/categories/<int:pk>/delete/",
        admin_views.category_delete,
        name="admin_category_delete",
    ),
    # Diamerisma Admin
    path(
        "manage/diamerismata/",
        admin_views.diamerisma_list,
        name="admin_diamerisma_list",
    ),
    path(
        "manage/diamerismata/create/",
        admin_views.diamerisma_create,
        name="admin_diamerisma_create",
    ),
    path(
        "manage/diamerismata/<int:pk>/edit/",
        admin_views.diamerisma_edit,
        name="admin_diamerisma_edit",
    ),
    path(
        "manage/diamerismata/<int:pk>/delete/",
        admin_views.diamerisma_delete,
        name="admin_diamerisma_delete",
    ),
    # Diaxeiristis Admin
    path(
        "manage/diaxeiristes/",
        admin_views.diaxeiristis_list,
        name="admin_diaxeiristis_list",
    ),
    path(
        "manage/diaxeiristes/create/",
        admin_views.diaxeiristis_create,
        name="admin_diaxeiristis_create",
    ),
    path(
        "manage/diaxeiristes/<int:pk>/edit/",
        admin_views.diaxeiristis_edit,
        name="admin_diaxeiristis_edit",
    ),
    path(
        "manage/diaxeiristes/<int:pk>/delete/",
        admin_views.diaxeiristis_delete,
        name="admin_diaxeiristis_delete",
    ),
    # Koinoxrista Admin
    path(
        "manage/koinoxrista/",
        admin_views.koinoxrista_list,
        name="admin_koinoxrista_list",
    ),
    path(
        "manage/koinoxrista/create/",
        admin_views.koinoxrista_create,
        name="admin_koinoxrista_create",
    ),
    path(
        "manage/koinoxrista/<int:pk>/edit/",
        admin_views.koinoxrista_edit,
        name="admin_koinoxrista_edit",
    ),
    path(
        "manage/koinoxrista/<int:pk>/delete/",
        admin_views.koinoxrista_delete,
        name="admin_koinoxrista_delete",
    ),
    # Xiliosta Admin
    path("manage/xiliosta/", admin_views.xiliosta_list, name="admin_xiliosta_list"),
    path(
        "manage/xiliosta/create/",
        admin_views.xiliosta_create,
        name="admin_xiliosta_create",
    ),
    path(
        "manage/xiliosta/<int:pk>/edit/",
        admin_views.xiliosta_edit,
        name="admin_xiliosta_edit",
    ),
    path(
        "manage/xiliosta/<int:pk>/delete/",
        admin_views.xiliosta_delete,
        name="admin_xiliosta_delete",
    ),
    # Dapanes Admin
    path("manage/dapanes/", admin_views.dapanes_list, name="admin_dapanes_list"),
    path(
        "manage/dapanes/create/",
        admin_views.dapanes_create,
        name="admin_dapanes_create",
    ),
    path(
        "manage/dapanes/<int:pk>/edit/",
        admin_views.dapanes_edit,
        name="admin_dapanes_edit",
    ),
    path(
        "manage/dapanes/<int:pk>/delete/",
        admin_views.dapanes_delete,
        name="admin_dapanes_delete",
    ),
]
