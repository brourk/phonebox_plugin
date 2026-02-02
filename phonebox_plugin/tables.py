import django_tables2 as tables
from netbox.tables import BaseTable, columns
from .models import Number, VoiceCircuit

ToggleColumn = columns.ToggleColumn


class NumberTable(BaseTable):

    pk = ToggleColumn()
    number = tables.LinkColumn()
    tenant = tables.LinkColumn()
    region = tables.LinkColumn()
    site = tables.LinkColumn()
    provider = tables.LinkColumn()
    forward_to = tables.LinkColumn()
    tags = columns.TagColumn()

    class Meta(BaseTable.Meta):
        model = Number
        fields = ('pk', 'number', 'tenant', 'region', 'site', 'description', 'provider', 'forward_to', 'tags')


class VoiceCircuitTable(BaseTable):

    pk = ToggleColumn()
    name = tables.LinkColumn()
    voice_device_or_vm = tables.Column(
        accessor='assigned_object.parent_object',
        linkify=True,
        orderable=False,
        verbose_name='Device/VM'
    )
    voice_circuit_type = tables.LinkColumn()
    tenant = tables.LinkColumn()
    region = tables.LinkColumn()
    site = tables.LinkColumn()
    provider = tables.LinkColumn()
    tags = columns.TagColumn()

    class Meta(BaseTable.Meta):
        model = VoiceCircuit
        fields = ('pk', 'name', 'voice_device_or_vm', 'voice_circuit_type', 'tenant', 'region', 'site', 'provider', 'tags')
