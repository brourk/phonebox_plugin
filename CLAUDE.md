# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PhoneBox Plugin is a telephone number management plugin for NetBox. It extends NetBox to manage phone numbers and voice circuits (SIP trunks, digital/analog voice circuits).

**Current version:** v0.0.11
**Minimum NetBox version:** 4.2.0
**Maximum NetBox version:** 4.9.99
**Plugin base URL:** `/plugins/phonebox/`

## Core Models

Both models inherit from `NetBoxModel` which provides automatic support for:
- Change logging
- Custom fields
- Tags
- Export templates
- Webhooks
- Journaling

### Number (phonebox_plugin/models.py:18)
Represents a single telephone number with DTMF character validation.
- **Base class:** NetBoxModel
- **Unique constraint:** (number, tenant) - numbers must be unique per tenant
- **Required fields:** number, tenant
- **Optional relations:** provider (circuits.Provider), region (dcim.Region), site (dcim.Site), forward_to (self-reference)
- **Validation:** Only allows leading +, digits 0-9, chars A-D, #, and * (no delimiters)

### VoiceCircuit (phonebox_plugin/models.py:79)
Represents voice circuits assigned to device/VM interfaces.
- **Base class:** NetBoxModel
- **Types:** SIP Trunk, Digital Voice Circuit, Analog Voice Circuit (defined in choices.py:5)
- **Assignment:** Uses GenericForeignKey to assign to dcim.Interface or virtualization.VMInterface
- **Required fields:** name, voice_circuit_type
- **Optional relations:** tenant, provider, region, site

## Architecture

### NetBox Version Compatibility
The plugin supports NetBox 4.2.0 through 4.9.x. Previous versions supported multiple NetBox versions with conditional logic, but v0.0.11 simplifies this by removing version checks and targeting NetBox 4.x+ with modern APIs.

### URL Structure
- Main plugin URLs: `phonebox_plugin/urls.py`
- API endpoints: `phonebox_plugin/api/urls.py` → `/api/plugins/phonebox/`
- Plugin registered at base_url='phonebox' (phonebox_plugin/__init__.py:18)

### Views Pattern
All views use NetBox's generic class-based views:
- List views: `generic.ObjectListView` with filterset and table
- Detail views: `generic.ObjectView`
- Edit views: `generic.ObjectEditView`
- Bulk operations: `generic.BulkEditView`, `generic.BulkDeleteView`, `generic.BulkImportView`

### API Structure
- Serializers use nested representations for related objects (TenantSerializer, RegionSerializer, SiteSerializer, etc.)
- VoiceCircuit.assigned_object uses dynamic serializer lookup via `get_serializer_for_model()`
- REST API compatible with pynetbox

### Export Functionality
The plugin supports two types of data export:

**CSV Export:**
- Available via "Export" button on list views (Numbers, Voice Circuits)
- Automatically provided by NetBox's ObjectListView
- Exports all visible columns in the current table view

**Export Templates:**
- Models are registered in NetBox's Export Template system
- Navigate to `/extras/export-templates/` to create custom templates
- Select "phonebox_plugin | number" or "phonebox_plugin | voice circuit" as object type
- Supports Jinja2 templating for custom formats (JSON, XML, CSV, etc.)

## Development Commands

### Installation for Development
```bash
# From source
source /opt/netbox/venv/bin/activate
pip3 install .

# Or in editable mode for development
pip3 install -e .
```

### Database Migrations
```bash
# After model changes
python3 manage.py makemigrations phonebox_plugin
python3 manage.py migrate
```

### Collect Static Files
```bash
# Required after modifying templates/static files
cd /opt/netbox/netbox/
python3 manage.py collectstatic
```

### NetBox Service Management
```bash
# Apply changes
sudo systemctl restart netbox

# View logs
sudo journalctl -u netbox -f
```

## Key Files

- `phonebox_plugin/__init__.py`: Plugin configuration and version detection
- `phonebox_plugin/models.py`: Number and VoiceCircuit models
- `phonebox_plugin/views.py`: All view classes with version-specific template selection
- `phonebox_plugin/choices.py`: VoiceCircuitTypeChoices and assignment model filters
- `phonebox_plugin/api/serializers.py`: REST API serializers with nested relations
- `phonebox_plugin/filters.py`: FilterSets for list views
- `phonebox_plugin/forms.py`: Forms for create/edit/bulk operations
- `phonebox_plugin/tables.py`: django-tables2 definitions for list views

## Important Constraints

- Numbers are validated by regex: `^\+?[0-9A-D\#\*]*$` (models.py:12)
- Number + Tenant must be unique together
- Voice circuits can only be assigned to dcim.Interface or virtualization.VMInterface
- Tenant is mandatory for Numbers, optional for VoiceCircuits

## Recent Changes (v0.0.11)

- **Base Class Migration**: Changed from `ChangeLoggedModel` to `NetBoxModel` for both Number and VoiceCircuit models
- **Site Field**: Added optional site field to Number model (migration 0005)
- **Export Support**: Enabled CSV export and Export Template integration
- **NetBox 4.2+**: Removed backward compatibility code, now supports NetBox 4.2.0 through 4.9.x
- **Simplified Code**: Removed version checking logic throughout the codebase
- **Forked Repository**: Updated URLs to point to brourk/phonebox_plugin
