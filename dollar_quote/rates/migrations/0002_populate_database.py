from django.core.management import call_command
from django.db import migrations


def populate_database(apps, schema_editor):
    call_command('populate_database')


class Migration(migrations.Migration):
    dependencies = [
        ('rates', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_database),
    ]
