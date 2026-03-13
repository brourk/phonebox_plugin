import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebox_plugin', '0006_add_custom_field_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='custom_field_data',
            field=models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
        ),
        migrations.AlterField(
            model_name='voicecircuit',
            name='custom_field_data',
            field=models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
        ),
    ]
