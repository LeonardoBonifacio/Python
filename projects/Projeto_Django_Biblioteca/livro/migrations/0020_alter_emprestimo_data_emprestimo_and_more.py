# Generated by Django 5.0.4 on 2024-05-10 23:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0019_alter_emprestimo_avaliacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 10, 20, 19, 0, 477824)),
        ),
        migrations.AlterField(
            model_name='livros',
            name='co_autor',
            field=models.CharField(blank=True, default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='livros',
            name='data_cadastro',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
