# Generated by Django 4.1.4 on 2023-02-11 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_project_project_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_id',
            new_name='team_id',
        ),
    ]