# Roadmap

Three phases, each independently shippable. Full scope rationale lives with the maintainers; this is the build order.

## Phase 1 — US defaults (in progress)

- [x] US small-business chart of accounts (numbered, GAAP-style) + company default wiring
- [x] US locale defaults with backup/revert
- [x] 1099-NEC/MISC classification + W-9 tracking on Supplier
- [ ] Upstream PR: contribute the US chart to frappe/erpnext's verified charts
- [ ] Sales tax foundation: state/county/city tax template structure, origin-vs-destination flags, taxable-shipping rules (manual tables, labeled as estimates)
- [ ] Exemption certificates: customer workflow, attachment, expiry reminders
- [ ] 1099 Summary report: per-supplier year totals, $600 threshold flag, e-file-shaped CSV
- [ ] NACHA/ACH export: Payment Order → bank-ready PPD/CCD file
- [ ] Workspace decluttering for a US SMB

## Phase 2 — connected services

- [ ] TaxJar connector (live rates at quote/invoice time, filing-ready liability reports)
- [ ] Plaid bank feeds (evaluating contribution to existing community work first)
- [ ] Economic nexus tracker: per-state revenue/transaction thresholds with approach alerts
- [ ] State sales tax return summaries by jurisdiction and period

## Phase 3 — the distribution

- [ ] One-command install + docker compose with a seeded US demo company
- [ ] Hosted demo + docs site
- [ ] Frappe marketplace listing; optional bundle of erpnext-assistant, erp-portal-branding, erpnext_debug

## Explicitly out of scope

- **Payroll.** US payroll is a compliance product; journals can import from Gusto/ADP, but withholding is never calculated here.
- Direct tax **filing** with states.
- GAAP inventory valuation changes to core; multi-entity consolidation.

## Candidates after Phase 3 (not committed)

QuickBooks (QBO) importer for COA/customers/vendors/open invoices · Avalara connector · ACH debit · Gusto/ADP journal import.
