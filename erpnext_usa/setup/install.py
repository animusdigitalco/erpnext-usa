"""Install-time setup: US locale defaults and 1099/W-9 supplier fields.

Everything here is reversible and documented in docs/locale-defaults.md.
Company-level setup (the chart of accounts) never runs automatically —
see erpnext_usa.setup.coa.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

SYSTEM_DEFAULTS = {
	"date_format": "mm-dd-yyyy",
	"first_day_of_the_week": "Sunday",
	"number_format": "#,###.##",
	"float_precision": 2,
	"currency_precision": 2,
}

# What the site looked like before we touched it is stored here so
# revert_site_defaults can put it back.
BACKUP_KEY = "erpnext_usa_previous_system_defaults"


def after_install():
	apply_site_defaults()
	make_custom_fields()
	frappe.db.commit()


def apply_site_defaults():
	"""US locale defaults for System Settings, Print Settings, and (on a
	fresh site only) Global Defaults."""
	system = frappe.get_doc("System Settings")
	backup = {}
	for fieldname, value in SYSTEM_DEFAULTS.items():
		if system.meta.has_field(fieldname):
			backup[fieldname] = system.get(fieldname)
			system.set(fieldname, value)
	system.flags.ignore_mandatory = True
	system.save()
	frappe.db.set_default(BACKUP_KEY, frappe.as_json(backup))

	if frappe.get_meta("Print Settings").has_field("pdf_page_size"):
		frappe.db.set_value("Print Settings", "Print Settings", "pdf_page_size", "Letter")

	# Only steer country/currency on a site with no company yet. An existing
	# site may be multi-national; we do not guess for it.
	if not frappe.db.count("Company"):
		gd = frappe.get_doc("Global Defaults")
		if gd.meta.has_field("country"):
			gd.country = "United States"
		if gd.meta.has_field("default_currency"):
			gd.default_currency = "USD"
		gd.save()

	frappe.clear_cache()


def revert_site_defaults():
	"""Put System Settings back the way they were before install.

	Run with: bench --site <site> execute erpnext_usa.setup.install.revert_site_defaults
	"""
	backup = frappe.parse_json(frappe.db.get_default(BACKUP_KEY) or "{}")
	if not backup:
		print("No backup of previous defaults found; nothing reverted.")
		return
	system = frappe.get_doc("System Settings")
	for fieldname, value in backup.items():
		if system.meta.has_field(fieldname):
			system.set(fieldname, value)
	system.flags.ignore_mandatory = True
	system.save()
	frappe.db.commit()
	print(f"Reverted System Settings fields: {', '.join(backup)}")


def make_custom_fields():
	"""1099/W-9 fields on Supplier. Namespaced us_* so they never collide
	with core's regional fields (core adds irs_1099 when a US company exists)."""
	create_custom_fields(
		{
			"Supplier": [
				dict(
					fieldname="us_tax_section",
					fieldtype="Section Break",
					label="US Tax Reporting",
					insert_after="tax_withholding_category",
					collapsible=1,
				),
				dict(
					fieldname="us_1099_form",
					fieldtype="Select",
					label="1099 Form",
					options="\n1099-NEC\n1099-MISC",
					insert_after="us_tax_section",
					description="Which 1099 this supplier receives at year end, if any.",
				),
				dict(
					fieldname="us_tin_type",
					fieldtype="Select",
					label="TIN Type",
					options="\nEIN\nSSN",
					insert_after="us_1099_form",
					depends_on="us_1099_form",
				),
				dict(
					fieldname="us_tax_column",
					fieldtype="Column Break",
					insert_after="us_tin_type",
				),
				dict(
					fieldname="us_w9_on_file",
					fieldtype="Check",
					label="W-9 on File",
					insert_after="us_tax_column",
				),
				dict(
					fieldname="us_w9_document",
					fieldtype="Attach",
					label="W-9 Document",
					insert_after="us_w9_on_file",
					depends_on="us_w9_on_file",
				),
			]
		},
		update=True,
	)
