# Generated migration for adding site field to Number model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '__first__'),
        ('phonebox_plugin', '0004_alter_number_created_alter_number_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='site',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='site_set',
                to='dcim.site'
            ),
        ),
    ]
