# US Locale Defaults

Applied once at install by `erpnext_usa.setup.install.apply_site_defaults`. Everything is reversible.

## What changes

**System Settings** (previous values are backed up automatically):

| Setting | New value |
| --- | --- |
| Date format | mm-dd-yyyy |
| First day of the week | Sunday |
| Number format | #,###.## |
| Float / currency precision | 2 |

**Print Settings:** PDF page size becomes **Letter** (core defaults to A4 — the thing every US user notices the first time they print an invoice).

**Global Defaults** — only when the site has **no Company yet**: country United States, currency USD. A site that already has companies is never touched, because it may be legitimately multi-national.

## What does NOT change

- Nothing at the company level. The chart of accounts is a separate, explicit step.
- No existing document, print format, or template is edited.
- Timezone is left alone (set it per your location in System Settings).

## Reverting

The previous System Settings values are stored at install time and restored with:

```bash
bench --site <site> execute erpnext_usa.setup.install.revert_site_defaults
```

Print Settings and Global Defaults are one-field changes; set them back by hand if needed.
