# Generated by Django 2.0 on 2017-12-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171214_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('A', 'Article'), ('B', 'Blog')], max_length=1),
        ),
    ]
