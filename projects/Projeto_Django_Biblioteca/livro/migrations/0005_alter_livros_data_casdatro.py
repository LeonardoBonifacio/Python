# Generated by Django 5.0.4 on 2024-05-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0004_alter_livros_data_casdatro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livros',
            name='data_casdatro',
            field=models.DateField(auto_now_add=True),
        ),
    ]
