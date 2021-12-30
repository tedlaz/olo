from django.contrib import admin

from . import models


class DapanesInline(admin.TabularInline):
    model = models.Dapanes
    extra = 1


class KoinoxristaAdmin(admin.ModelAdmin):
    inlines = [DapanesInline]
    list_display = ['ekdosi', 'id', 'diaxeiristis', 'sxolia', 'published']
    list_filter = ['ekdosi', 'diaxeiristis']


class DiamerismaAdmin(admin.ModelAdmin):
    list_display = ('guest', 'owner', 'orofos')


class DapanesAdmin(admin.ModelAdmin):
    list_display = ('koinoxrista', 'category', 'par_date',
                    'par_num', 'par_per', 'value')
    list_filter = ['category', 'par_date']
    search_fields = ['par_per']


admin.site.register(models.Category)
admin.site.register(models.Diamerisma, DiamerismaAdmin)
admin.site.register(models.Koinoxrista, KoinoxristaAdmin)
admin.site.register(models.Xiliosta)
admin.site.register(models.Diaxeiristis)
admin.site.register(models.Dapanes, DapanesAdmin)
