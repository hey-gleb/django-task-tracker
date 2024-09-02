from django.db import migrations


def create_default_groups(apps, schema_editor):
    group = apps.get_model('auth', 'Group')

    groups = ['Manager', 'Developer', 'QA']

    for group_name in groups:
        group.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0001_initial'),  # Replace with the previous migration
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]