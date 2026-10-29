app_name = "erpnext_usa"
app_title = "ERPNext USA"
app_publisher = "Animus Digital"
app_description = (
    "US localization for ERPNext: a real US chart of accounts, American locale "
    "defaults, and proper 1099/W-9 handling. Built on ERPNext; not affiliated "
    "with Frappe."
)
app_email = "jon@animusdigital.co"
app_license = "GPL-3.0"

required_apps = ["erpnext"]

# Applies US locale defaults (date format, Letter paper, week start) and the
# 1099/W-9 supplier fields. Safe and documented in docs/locale-defaults.md,
# with a revert function. Company-level setup (chart of accounts) is explicit
# and never runs automatically — see docs/chart-of-accounts.md.
after_install = "erpnext_usa.setup.install.after_install"
