# ERPNext USA — Full Scope (pre-build)

Status: SCOPING — nothing built, awaiting Jon's decisions at the bottom.
Date: 2026-10-29

## Thesis

ERPNext loses nearly every US small-business evaluation in the first hour, and it loses on configuration, not capability. The product ships India-first; the US story in core is almost nothing. We package the missing hour: an overlay app plus a distribution that makes a fresh install feel like American accounting software out of the box. Same engine, opinionated defaults, a name people can say.

## Evidence (verified against frappe/erpnext version-15, 2026-10-29)

- **No verified US chart of accounts in core.** The verified COA folder has charts for France, Belgium, Brazil, Canada (francophone), Burkina Faso (two), and more. Nothing for the United States.
- **US regional support in core** = one supplier checkbox (1099 required), sales-tax-exempt checkboxes on Sales Order/Invoice, an IRS 1099 report and print format. That is the entire `regional/united_states` module.
- **Zero public TaxJar or Avalara apps** on GitHub. Zero NACHA/ACH apps. Three one-star Plaid experiments (one active: aerele/plaid_integration, pushed 2026-06).
- **frappe/banking is not public** (paid marketplace app), so open-source bank feeds are an unfilled gap.
- Main repo: 40.7k stars, 13.3k forks, ~2.5k PRs merged in 2 months. Core is healthy; a divergent fork would drown. The most-upvoted open issue has 18 reactions, which means demand lives on the forum and in lost evaluations, not the tracker.

## Naming & trademark (decision needed)

"ERPNext" is Frappe's trademark. Community convention tolerates app/repo names like `erpnext_usa` (cf. erpnext_chinese etc.), but the distribution brand must not read as official. Proposal: app and repos stay `erpnext_usa` / `erpnext-usa` (searchable, conventional); the distribution gets its own brand with the tagline "built on ERPNext." Name candidates to react to: Mainstreet ERP, Homestead ERP, Ledger & Main. Check Frappe's trademark policy before launch either way.

## Licensing (decision needed)

ERPNext is GPL-3.0. The overlay app extends and imports it, so `erpnext_usa` ships GPL-3.0, unlike the three MIT apps. The distribution repo (scripts, docs, compose files) can stay MIT. No practical effect on the business model (services, not license sales), but it is a deliberate choice Jon should sign off on.

## Architecture — three repos

1. **Tracking fork** of frappe/erpnext under animusdigitalco. Zero divergent commits, synced automatically. Exists for discoverability, issue triage against pinned versions, and emergency patches. Never the product.
2. **`erpnext_usa`** — the overlay app. All features live here via fixtures, custom fields, hooks, regional overrides, and a setup wizard hook. CI runs install + smoke tests against v15 and v16 nightly so upstream churn surfaces within a day.
3. **Distribution repo** — one-command install (script + docker compose), seeded demo company (generic name, e.g. "Prairie Supply Co."), docs, and the bundle manifest that pulls in erpnext_debug, erp-portal-branding, and erpnext-assistant as optional extras.

## Phase 1 — US defaults (the credibility release)

Goal: a fresh site that an American bookkeeper recognizes. Est. 10–14 focused build days.

- **Verified US chart of accounts**: numbered GAAP-style chart, accrual, with an LLC/S-corp small-business flavor. Also submitted upstream as a PR to frappe/erpnext — real contribution, credibility, and attention in one move.
- **Locale defaults**: MM-DD-YYYY, USD number formats, US timezones, Letter-size print formats (core defaults to A4), US-English terminology fixtures (no GST strings in sight).
- **Module decluttering**: hide India/GCC regional artifacts and unused workspaces; opinionated workspace layout for a US SMB.
- **Sales tax foundation (manual tier)**: state/county/city tax template structure, origin vs destination rules flagged per state, taxable-shipping flags, tax categories wired to the exempt checkboxes core already has.
- **Exemption certificates**: customer exemption workflow with certificate attachment and expiry reminders.
- **1099 done properly**: 1099-NEC vs MISC classification, W-9 request + storage on Supplier, year-end totals report + CSV export.
- **NACHA/ACH export**: Payment Order → NACHA file (PPD/CCD), bank header config doctype. Vendors get paid without re-keying into the bank portal.

Explicit Phase 1 boundary: manual tax tables are labeled estimates; accuracy tier arrives in Phase 2.

## Phase 2 — connected services (the accuracy release)

Est. 15–20 focused build days.

- **TaxJar connector** (rates at quote/invoice time; filing-ready liability reports). Avalara later if demand shows.
- **Plaid bank feeds**: evaluate contributing to aerele/plaid_integration before building fresh; feed → Bank Transaction → reconciliation flow.
- **Economic nexus tracker**: per-state revenue/transaction thresholds with alerts as you approach them. Biggest fear of growing e-commerce SMBs; nobody in the ecosystem has it; this is the headline feature of the launch story.
- **State sales tax return summaries**: collected vs owed by jurisdiction, per filing period.

## Phase 3 — the distribution (the attention release)

Est. 8–10 focused build days.

- One-command install + docker compose, seeded US demo company.
- Hosted demo site, docs site, launch video (assistant answering questions about US data is the demo moment).
- Frappe marketplace listings; bundle manifest for the three existing apps.
- Launch content: Frappe forum (the localization threads with years of unanswered demand), Show HN, r/selfhosted, QuickBooks-alternative SEO content.

## Phase 4 — candidates (not committed)

- **QuickBooks escape hatch**: QBO export importer (COA, customers, vendors, open invoices). Probably the single biggest adoption lever; large surface, so it earns its own scope doc if Phases 1–3 validate.
- Gusto/ADP payroll journal import (payroll itself stays out, see below).
- Avalara connector, ACH debit (customer pulls), lockbox import.

## Out of scope, permanently (v1 horizon)

- **Payroll.** US payroll is a compliance product, not a feature. Integrate journals from Gusto/ADP, never calculate withholding.
- Direct tax **filing** with states.
- GAAP inventory valuation changes to core, multi-entity consolidation, audited-financials features.

## Risks

| Risk | Mitigation |
| --- | --- |
| Tax rate staleness → wrong tax collected | Connector-first messaging; manual tables shipped as labeled estimates; prominent "not tax advice" disclaimer; CPA review of the COA and 1099 logic before launch |
| Upstream churn breaks overlay | Overlay-only architecture; nightly CI against v15/v16; tracking fork for emergency pins |
| Support burden ("you're the US maintainer now") | GitHub Discussions only; paid support tier routed to Animus; README sets expectations |
| Trademark complaint | Distinct distro brand; "built on ERPNext" phrasing; review Frappe policy pre-launch |
| TaxJar pricing/API changes | Connector is optional tier; manual tier always works |
| Scope creep toward accounting-firm features | This doc is the fence; Phase 4 items need their own scope |

## Business model

The software is free and open source. Revenue is Animus: implementation, hosting, support retainers, and eventually a "we run it for you" managed tier. Every install is a lead; the README and docs site say plainly who built it and where to get help.

## Success metrics (90 days post Phase-3 launch)

- 500+ GitHub stars across the three repos; 100+ documented installs (forum threads, marketplace counts)
- The upstream US COA PR merged or in serious review
- 10+ active community threads referencing the distro
- 3+ qualified Animus implementation leads attributable to it

## Effort summary

~33–44 focused build days total across the three phases, sequenced so each phase is independently shippable and each ends with a launchable story. Claude builds; Jon decides, tests on a scratch bench, fronts the forum presence, and records the launch video.

## Open decisions (Jon)

1. Distribution brand name (Mainstreet ERP / Homestead ERP / Ledger & Main / other?)
2. GPL-3.0 for `erpnext_usa` — comfortable?
3. COA flavor for v1: LLC/S-corp small business only, or also a C-corp variant?
4. TaxJar account for connector development (Phase 2 gate)
5. Demo hosting: Frappe Cloud vs DigitalOcean droplet
6. Bundle the three existing apps as default-on or opt-in extras?
7. Confirm payroll stays out permanently
8. Scratch bench for testing: Kingsway dev bench or a fresh dedicated site?
