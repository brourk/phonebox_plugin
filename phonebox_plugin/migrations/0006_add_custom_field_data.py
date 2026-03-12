from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebox_plugin', '0005_add_site_to_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='custom_field_data',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='voicecircuit',
            name='custom_field_data',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
