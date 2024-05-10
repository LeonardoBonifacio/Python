# Generated by Django 5.0.4 on 2024-05-10 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0016_remove_emprestimo_tempo_duracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='avaliacao',
            field=models.CharField(choices=[('P', 'Péssimo'), ('R', 'Ruim'), ('B', 'Bom'), ('O', 'Ótimo')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
