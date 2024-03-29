# Generated by Django 4.0 on 2021-12-30 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, unique=True, verbose_name='Κατηγορία')),
            ],
            options={
                'verbose_name': 'Κατηγορία',
                'verbose_name_plural': 'Κατηγορίες',
                'ordering': ['category'],
            },
        ),
        migrations.CreateModel(
            name='Diamerisma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Διαμέρισμα')),
                ('num', models.IntegerField(unique=True, verbose_name='Αριθμός')),
                ('orofos', models.IntegerField(default=0, verbose_name='Όροφος')),
                ('sizesm', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Μέγεθος τ.μ.')),
                ('owner', models.CharField(max_length=50, verbose_name='Ιδιοκτήτης')),
                ('guest', models.CharField(max_length=50, verbose_name='Ένοικος')),
            ],
            options={
                'verbose_name': 'Διαμέρισμα',
                'verbose_name_plural': 'Διαμερίσματα',
                'ordering': ['num'],
            },
        ),
        migrations.CreateModel(
            name='Diaxeiristis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Όνομα')),
                ('date_from', models.DateField(verbose_name='Ημ/νία ανάληψης καθηκόντων')),
                ('sex', models.IntegerField(choices=[(1, 'Άντρας'), (2, 'Γυναίκα')], default=1, verbose_name='Φύλο')),
            ],
            options={
                'verbose_name': 'Διαχειριστής',
                'verbose_name_plural': 'Διαχειριστές',
                'unique_together': {('name', 'date_from')},
            },
        ),
        migrations.CreateModel(
            name='Koinoxrista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ekdosi', models.DateField(unique=True, verbose_name='Ημερομηνία')),
                ('sxolia', models.TextField(verbose_name='Σχόλια')),
                ('published', models.BooleanField(default=False)),
                ('diaxeiristis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koi.diaxeiristis', verbose_name='Διαχειριστής')),
            ],
            options={
                'verbose_name': 'Κοινόχρηστα',
                'verbose_name_plural': 'Κοινόχρηστα',
                'ordering': ['-ekdosi', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Xiliosta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xiliosta', models.IntegerField(verbose_name='Χιλιοστά')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koi.category', verbose_name='Κατηγορία')),
                ('diamerisma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koi.diamerisma', verbose_name='Διαμέρισμα')),
            ],
            options={
                'verbose_name': 'Χιλιοστό',
                'verbose_name_plural': 'Χιλιοστά',
                'ordering': ['diamerisma', 'category'],
                'unique_together': {('diamerisma', 'category')},
            },
        ),
        migrations.CreateModel(
            name='Dapanes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('par_date', models.DateField(verbose_name='Ημερομηνία παραστατικού')),
                ('par_num', models.CharField(max_length=20, verbose_name='Αριθμός παραστατικού')),
                ('par_per', models.CharField(max_length=100, verbose_name='περιγραφη')),
                ('value', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ποσό')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koi.category', verbose_name='Κατηγορία')),
                ('koinoxrista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koi.koinoxrista', verbose_name='Κοινοχρηστα')),
            ],
            options={
                'verbose_name': 'Δαπάνη',
                'verbose_name_plural': 'Δαπάνες',
                'ordering': ['koinoxrista', 'par_date'],
                'unique_together': {('par_date', 'par_num')},
            },
        ),
    ]
