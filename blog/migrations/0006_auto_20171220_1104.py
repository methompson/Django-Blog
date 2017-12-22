# Generated by Django 2.0 on 2017-12-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20171218_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_title',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='subject',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('A', 'Article'), ('B', 'Blog'), ('P', 'Permanent Page')], max_length=1),
        ),
    ]
