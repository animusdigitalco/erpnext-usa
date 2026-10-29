"""Apply the US small-business chart of accounts to a company.

Never runs automatically. The target company must have no transactions:
replacing a chart is only safe on a company that has not posted anything.

Usage:
    bench --site <site> execute erpnext_usa.setup.coa.apply_us_chart \
        --kwargs "{'company': 'My Company LLC'}"
"""

import json
import os

import frappe
from frappe import _

CHART_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "us_gaap_small_business.json")

# Company default account fields wired after the chart is created, looked up
# by (account_type, account_name). Best effort: a missing match is reported,
# never fatal.
COMPANY_DEFAULTS = [
	("default_receivable_account", {"account_type": "Receivable"}),
	("default_payable_account", {"account_type": "Payable"}),
	("default_cash_account", {"account_type": "Cash"}),
	("default_bank_account", {"account_name": "Checking Account"}),
	("default_income_account", {"account_name": "Sales"}),
	("default_expense_account", {"account_name": "Materials and Product Costs"}),
	("round_off_account", {"account_type": "Round Off"}),
	("write_off_account", {"account_name": "Write Off"}),
	("exchange_gain_loss_account", {"account_name": "Exchange Gain or Loss"}),
	("depreciation_expense_account", {"account_name": "Depreciation Expense"}),
	("accumulated_depreciation_account", {"account_type": "Accumulated Depreciation"}),
	("stock_received_but_not_billed", {"account_type": "Stock Received But Not Billed"}),
	("stock_adjustment_account", {"account_type": "Stock Adjustment"}),
	("expenses_included_in_valuation", {"account_type": "Expenses Included In Valuation"}),
	("default_inventory_account", {"account_type": "Stock"}),
	("temporary_opening_account", {"account_type": "Temporary"}),
]


def get_chart() -> dict:
	with open(os.path.abspath(CHART_FILE)) as f:
		return json.load(f)["tree"]


def apply_us_chart(company: str, dry_run: bool = False):
	"""Replace `company`'s chart of accounts with the US small-business chart."""
	if not frappe.db.exists("Company", company):
		frappe.throw(_("Company {0} does not exist").format(company))

	if frappe.db.exists("GL Entry", {"company": company}):
		frappe.throw(
			_("{0} already has posted transactions. The chart can only be replaced "
			  "on a company with no GL entries.").format(company)
		)

	chart = get_chart()
	if dry_run:
		count = _count_accounts(chart)
		print(f"Dry run: would replace the chart of {company} with {count} US accounts.")
		return

	from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts
	from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import (
		unset_existing_data,
	)

	unset_existing_data(company)
	create_charts(company, custom_chart=chart)
	wired, missing = _set_company_defaults(company)
	frappe.db.commit()

	print(f"Applied the US chart of accounts to {company}.")
	print(f"Company default accounts wired: {', '.join(wired) or 'none'}")
	if missing:
		print(f"Set these manually in the Company record: {', '.join(missing)}")


def _count_accounts(node: dict) -> int:
	meta_keys = {"account_number", "account_type", "root_type", "is_group", "tax_rate", "account_currency"}
	count = 0
	for key, child in node.items():
		if key in meta_keys or not isinstance(child, dict):
			continue
		count += 1 + _count_accounts(child)
	return count


def _set_company_defaults(company: str) -> tuple[list, list]:
	company_meta = frappe.get_meta("Company")
	wired, missing = [], []
	for fieldname, lookup in COMPANY_DEFAULTS:
		if not company_meta.has_field(fieldname):
			continue
		filters = dict(lookup, company=company, is_group=0)
		account = frappe.db.get_value("Account", filters)
		if account:
			frappe.db.set_value("Company", company, fieldname, account)
			wired.append(fieldname)
		else:
			missing.append(fieldname)
	return wired, missing
