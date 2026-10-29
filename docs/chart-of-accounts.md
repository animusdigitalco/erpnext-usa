# The US Small Business Chart of Accounts

A numbered, GAAP-style chart designed for a US LLC or S-corp doing product or service business, accrual basis. About 75 accounts: enough structure for clean financials, small enough that a non-accountant can find things.

## Numbering

| Range | Section |
| --- | --- |
| 1000s | Assets (1100 current, 1600 fixed, 1800 other, 1900 temporary) |
| 2000s | Liabilities (2100 current incl. payroll + sales tax, 2300 long-term) |
| 3000s | Equity (capital, draws, retained earnings, opening balance) |
| 4000s | Income (sales, service, shipping, returns, discounts, 4900 other income) |
| 5000s | Cost of Goods Sold (materials, freight in, subcontractors, inventory adjustments) |
| 6000s | Operating expenses (alphabetical-ish, incl. 6090 Contract Labor for 1099 work) |
| 7000s | Other expenses (interest, penalties, exchange, write-off, round-off) |

## ERPNext account types

The chart carries every account type ERPNext's automation depends on, so a company set up with it works for both service and inventory businesses: Bank, Cash, Receivable, Payable, Stock, Stock Received But Not Billed, Stock Adjustment, Expenses Included In Valuation, Cost of Goods Sold, Fixed Asset, Accumulated Depreciation, Depreciation, Capital Work in Progress, Tax, Round Off, Temporary, Equity, Income Account.

## Applying it

Only on a company with **no posted transactions** — the function refuses otherwise:

```bash
bench --site <site> execute erpnext_usa.setup.coa.apply_us_chart \
  --kwargs "{'company': 'My Company LLC'}"
```

What it does, in order:

1. Verifies the company exists and has no GL entries.
2. Removes the existing (default) accounts using ERPNext's own chart-importer plumbing.
3. Creates the US chart via `create_charts` — the same code path core uses for its verified charts.
4. Wires the company's default account fields (receivable, payable, cash, bank, income, expense, round-off, write-off, exchange gain/loss, depreciation, and the stock accounts) by account type or name, and prints anything you need to set manually.

Pass `'dry_run': True` first to see the account count without changing anything.

## Design notes

- **Owner's Draws and Opening Balance Equity** exist because that's what QuickBooks refugees look for on day one.
- **Undeposited Funds** is typed as Bank so payment entries can land there before the real deposit.
- **Meals (50% Deductible)** and **Penalties and Fines** are split out because they're tax-return adjustments your CPA will ask about.
- **Contract Labor (1099)** pairs with the supplier 1099 fields: book 1099 work there and the year-end review is one filtered report.
- Sales tax collected goes to **2130 Sales Tax Payable** (type Tax); the Phase-1 sales tax templates will point there by default.

## Known limits

- One flavor for now (LLC/S-corp small business). A C-corp variant (income tax provision accounts, etc.) is on the roadmap if demand shows.
- Numbers render in account names using ERPNext's standard `number - name` convention; renumbering after the fact is manual, like any ERPNext chart.
