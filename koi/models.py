from django.db import models
from utils import greek_utils


class Diamerisma(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Διαμέρισμα')
    num = models.IntegerField(unique=True, verbose_name='Αριθμός')
    orofos = models.IntegerField(default=0, verbose_name='Όροφος')
    sizesm = models.DecimalField(
        decimal_places=2, max_digits=7, verbose_name='Μέγεθος τ.μ.')
    owner = models.CharField(max_length=50, verbose_name='Ιδιοκτήτης')
    guest = models.CharField(max_length=50, verbose_name='Ένοικος')

    class Meta:
        ordering = ['num']
        verbose_name = 'Διαμέρισμα'
        verbose_name_plural = 'Διαμερίσματα'

    def __str__(self):
        return f'{self.guest}({self.orofos})'


class Category(models.Model):
    category = models.CharField(
        max_length=50, unique=True, verbose_name='Κατηγορία')

    class Meta:
        ordering = ['category']
        verbose_name = 'Κατηγορία'
        verbose_name_plural = 'Κατηγορίες'

    def __str__(self):
        return self.category


class Xiliosta(models.Model):
    diamerisma = models.ForeignKey(
        Diamerisma, on_delete=models.CASCADE, verbose_name='Διαμέρισμα')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Κατηγορία')
    xiliosta = models.IntegerField(verbose_name='Χιλιοστά')

    class Meta:
        unique_together = ['diamerisma', 'category']
        ordering = ['diamerisma', 'category']
        verbose_name = 'Χιλιοστό'
        verbose_name_plural = 'Χιλιοστά'

    def __str__(self):
        return f'{self.diamerisma} {self.category} {self.xiliosta}'


class Diaxeiristis(models.Model):
    name = models.CharField(max_length=50, verbose_name='Όνομα')
    date_from = models.DateField(verbose_name='Ημ/νία ανάληψης καθηκόντων')
    SEX_CHOICES = [(1, 'Άντρας'), (2, 'Γυναίκα')]
    sex = models.IntegerField(
        choices=SEX_CHOICES, default=1, verbose_name='Φύλο')

    class Meta:
        unique_together = ['name', 'date_from']
        verbose_name = 'Διαχειριστής'
        verbose_name_plural = 'Διαχειριστές'

    def __str__(self):
        return f'{self.name}'


class Koinoxrista(models.Model):
    ekdosi = models.DateField('Ημερομηνία', unique=True)
    diaxeiristis = models.ForeignKey(
        Diaxeiristis, on_delete=models.CASCADE, verbose_name='Διαχειριστής')
    sxolia = models.TextField(verbose_name='Σχόλια')

    @property
    def ekdosi_gr(self):
        return f'{self.ekdosi.day}/{self.ekdosi.month}/{self.ekdosi.year}'

    def totals(self):
        tval = 0
        for el in self.dapanes_set.values():
            tval += float(el['value'])
        return greek_utils.grnum(tval)

    class Meta:
        ordering = ['-ekdosi', 'id']
        verbose_name = 'Κοινόχρηστα'
        verbose_name_plural = 'Κοινόχρηστα'

    def __str__(self):
        return f'{self.id} -> {greek_utils.grdate(self.ekdosi)}'


class Dapanes(models.Model):
    koinoxrista = models.ForeignKey(
        Koinoxrista, on_delete=models.CASCADE, verbose_name='Κοινοχρηστα')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Κατηγορία')
    par_date = models.DateField('Ημερομηνία παραστατικού')
    par_num = models.CharField(
        max_length=20, verbose_name='Αριθμός παραστατικού')
    par_per = models.CharField(max_length=100, verbose_name='περιγραφη')
    value = models.DecimalField(
        decimal_places=2, max_digits=9, verbose_name='Ποσό')

    class Meta:
        unique_together = ['par_date', 'par_num']
        ordering = ['koinoxrista', 'par_date']
        verbose_name = 'Δαπάνη'
        verbose_name_plural = 'Δαπάνες'

    def __str__(self):
        return f'{self.par_date} {self.par_num} {self.par_per} {self.value}'
