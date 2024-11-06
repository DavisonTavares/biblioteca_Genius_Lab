# Generated by Django 5.0.1 on 2024-11-06 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimos', '0003_reserva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='status',
            field=models.CharField(choices=[('AA', 'Aguardando Aprovação'), ('AR', 'Aguardando Retirada'), ('AP', 'Aprovada'), ('CA', 'Cancelada')], default='AB', max_length=2, verbose_name='Status da Reserva'),
        ),
    ]
