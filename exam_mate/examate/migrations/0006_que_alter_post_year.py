# Generated by Django 4.1.3 on 2023-01-20 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examate', '0005_alter_post_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='que',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que', models.CharField(max_length=500)),
                ('uid', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='year',
            field=models.CharField(max_length=50),
        ),
    ]
