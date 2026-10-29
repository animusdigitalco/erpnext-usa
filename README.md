# ERPNext USA

US localization for ERPNext. A fresh install configured the way an American bookkeeper expects: a real US chart of accounts, American locale defaults, and proper 1099/W-9 handling — with sales tax, ACH, and bank feeds on the roadmap.

Built on [ERPNext](https://github.com/frappe/erpnext). Not affiliated with or endorsed by Frappe Technologies.

## Why this exists

ERPNext is excellent software that ships India-first. As of v15, core has **no verified US chart of accounts** (France, Belgium, Brazil, and Burkina Faso all have one), and the entire US regional module is a 1099 checkbox, two sales-tax-exempt flags, and one report. Most US evaluations die in that first hour of configuration. This app packages the missing hour.

## What it does today

| Feature | Status | Docs |
| --- | --- | --- |
| US small-business chart of accounts (numbered, GAAP-style) | Shipped | [docs/chart-of-accounts.md](docs/chart-of-accounts.md) |
| US locale defaults (MM-DD-YYYY, Sunday week start, Letter paper, USD on fresh sites) | Shipped | [docs/locale-defaults.md](docs/locale-defaults.md) |
| 1099-NEC/MISC classification + W-9 tracking on Supplier | Shipped | [docs/1099-and-w9.md](docs/1099-and-w9.md) |
| Sales tax structure (state/county/city templates, exemption certificates) | Planned — Phase 1 | [docs/roadmap.md](docs/roadmap.md) |
| NACHA/ACH payment file export | Planned — Phase 1 | [docs/roadmap.md](docs/roadmap.md) |
| TaxJar rates, Plaid bank feeds, economic nexus tracking | Planned — Phase 2 | [docs/roadmap.md](docs/roadmap.md) |

## Requirements

- Frappe Framework and ERPNext, v15 or v16
- A bench you can install apps on, or Frappe Cloud

## Installation

### Bench (self-hosted)

```bash
bench get-app https://github.com/animusdigitalco/erpnext-usa
bench --site yoursite.example.com install-app erpnext_usa
bench --site yoursite.example.com migrate
bench restart
```

The app name is `erpnext_usa` (underscore); the repository is `erpnext-usa`.

### Frappe Cloud

1. Bench group → **Apps** → **Add App** → **From GitHub** → paste `https://github.com/animusdigitalco/erpnext-usa`.
2. Deploy, then install **ERPNext USA** on your site.

### What installation changes, exactly

Install applies the **site-level** locale defaults (documented, reversible — see [docs/locale-defaults.md](docs/locale-defaults.md)) and adds the Supplier 1099/W-9 fields. It does **not** touch any company's chart of accounts: that step is explicit, because replacing a chart is only safe on a company with no transactions.

### Applying the US chart of accounts

For a company with no posted transactions (ideally a brand-new one):

```bash
# see what would happen
bench --site yoursite.example.com execute erpnext_usa.setup.coa.apply_us_chart \
  --kwargs "{'company': 'My Company LLC', 'dry_run': True}"

# do it
bench --site yoursite.example.com execute erpnext_usa.setup.coa.apply_us_chart \
  --kwargs "{'company': 'My Company LLC'}"
```

This replaces the default chart with the numbered US chart and wires the company's default accounts (receivable, payable, bank, COGS, round-off, and the rest). Anything it could not wire is printed so you can set it by hand. Full account list and design notes in [docs/chart-of-accounts.md](docs/chart-of-accounts.md).

### Uninstall / revert

```bash
bench --site yoursite.example.com execute erpnext_usa.setup.install.revert_site_defaults
bench --site yoursite.example.com uninstall-app erpnext_usa
```

## Architecture

Everything is an overlay: fixtures, custom fields (namespaced `us_*`), and explicit setup functions. No core files are modified, no doctypes are overridden, and the app tracks upstream v15/v16. The companion repos are the clean [tracking fork of erpnext](https://github.com/animusdigitalco/erpnext) (zero divergent commits, used for pinning and upstream PRs) and, later, a one-command distribution.

## Disclaimer

This software configures accounting defaults; it is not tax, legal, or accounting advice. Have a CPA review your chart of accounts and filings. Tax rules change; you are responsible for what you file.

## Related apps by the same author

- [erpnext-assistant](https://github.com/animusdigitalco/erpnext-assistant) — read-only AI chat over your own ERPNext data
- [erp-portal-branding](https://github.com/animusdigitalco/erp-portal-branding) — rebrand the portal with no CSS
- [erpnext_debug](https://github.com/animusdigitalco/erpnext_debug) — on-screen tracer for developers

## Contributing

Issues and PRs welcome, especially from bookkeepers and CPAs who can pressure-test the chart and the 1099 flow. Roadmap and scope fences are in [docs/roadmap.md](docs/roadmap.md).

## License

GPL-3.0 (this app extends ERPNext, which is GPL-3.0).
