# Generated by Django 5.0.4 on 2024-05-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0014_alter_emprestimo_nome_emprestado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_devolucao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateField(blank=True, null=True),
        ),
    ]
