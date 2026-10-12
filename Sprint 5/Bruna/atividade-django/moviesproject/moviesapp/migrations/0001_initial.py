from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('frequencia', models.CharField(choices=[('n', 'nunca'), ('s', 'às vezes'), ('a', 'sempre')], max_length=1)),
                ('prioridade', models.IntegerField()),
                ('categoria', models.CharField(choices=[('l', 'lazer'), ('h', 'saúde'), ('w', 'trabalho')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('diretor', models.CharField(max_length=70)),
                ('genero', models.CharField(max_length=20)),
                ('data_lancamento', models.DateField()),
            ],
        ),
    ]
