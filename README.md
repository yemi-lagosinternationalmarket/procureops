# lim_procurement

LIM-specific Frappe Custom App on top of ERPNext. Extends ERPNext's native Supplier / Item / Purchase Order DocTypes with LIM's procurement attributes, adds the `LIM Activity` polymorphic audit-log DocType, and exposes whitelisted REST methods for the procurement-agent to call.

## Where this fits

This app is one piece of LIM's commerce + procurement platform. The platform's architectural decisions live in the [`b2b-starter`](https://github.com/yemi-lagosinternationalmarket/b2b-starter) repo:

- **ADR 0018** ([link](https://github.com/yemi-lagosinternationalmarket/b2b-starter/blob/main/docs/adr/0018-erpnext-as-erp-medusa-scoped-to-commerce.md)) — ERPNext as ERP system of record; Medusa scoped to commerce; this Custom App is the LIM-specific extension layer
- **ADR 0019** ([link](https://github.com/yemi-lagosinternationalmarket/b2b-starter/blob/main/docs/adr/0019-lim-custom-app-licensing-posture.md)) — licensing posture (separable Frappe app, ERPNext GPL v3 upstream, this app unlicensed until distribution)
- **`apps/backend/CONTEXT.md`** in b2b-starter — canonical domain glossary (Supplier / Item / Purchase Order / `agent_authority` / Activity / etc.)

## Rules (per ADR 0019)

1. **Don't fork ERPNext.** Use hooks, Custom Fields (via Fixtures), and whitelisted REST methods.
2. **Don't import private ERPNext modules.** Use documented Frappe Framework primitives (`frappe.get_doc`, `frappe.db.get_value`, `@frappe.whitelist`, hooks).
3. **Custom Fields go in Fixtures** (`lim_procurement/fixtures/custom_field.json`). Versioned, portable, deployable as data — not as patches.
4. **Custom DocTypes only when ERPNext has no native equivalent** (e.g., `LIM Activity` for cross-system audit log).
5. **Tests in pytest** under `tests/`. Frappe test runner via `bench run-tests --app lim_procurement`.

## What this app contains

### Shipped in A.1' (b2b-starter [#31](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/31))

- **App scaffold** — standard Frappe app layout (`hooks.py`, `modules.txt`, `pyproject.toml`/`setup.py`, fixtures dir, default module dir).
- **11 Supplier Custom Fields** declared in `lim_procurement/fixtures/custom_field.json`:
  - `agent_authority` (Select: `full_auto` / `draft_only` / `review_only`, default `draft_only`)
  - `tone_reference_message_id` (Data — opaque ref into `apps/messaging`)
  - `frequency` (Select: `As Needed` / `Weekly` / `Bi-weekly` / `Monthly`, default `As Needed`)
  - `follow_up_level` (Select: `Low` / `Medium` / `High`, default `Medium`)
  - `default_lead_time_days` (Int)
  - `order_minimum_text` (Small Text)
  - `vendor_sends_truck` (Check, default 0)
  - `we_arrange_freight` (Check, default 0)
  - `freight_fee` (Currency, default 0)
  - `pallet_fee` (Currency, default 0)
  - `statement_email_or_url` (Data — distinct from `email_id`)
- `hooks.py` `fixtures` declaration so `bench migrate` re-applies them across environments.

### Deferred (decision recorded here)

- **`LIM Vendor Tag` Custom DocType** — deferred to a follow-up. The A.1' issue marks this Optional ("can defer if Supplier Group covers categorization adequately"). ERPNext's native **Supplier Group** plus the **Tag** primitive on Supplier covers categorization for now; we'll re-open this if/when those prove insufficient.

### Planned in later slices

- **Item Custom Fields**: `storage_type`, `is_perishable`, `default_buy_unit`, `notes_for_agent` (see [#32](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/32))
- **Purchase Order workflow + Custom Fields + whitelisted REST methods**: `create_po_draft`, `mark_po_sent`, `mark_po_confirmed`, `mark_po_needs_review`, `cancel_po`, `resolve_placeholder` (see [#33](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/33))
- **`LIM Activity` Custom DocType**: polymorphic audit log + Frappe hooks emitting Activities on PO submit / cancel / Supplier authority changes (see [#34](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/34))
- **Notion catalog seed script**: imports historical Supplier / Item / Item Supplier data (see [#35](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/35))

## Setup

### Frappe Cloud (production — `lagosinternationalmarket.v.frappe.cloud`)

1. Open the Frappe Cloud dashboard for the site.
2. Apps → **Add app** → **Bring your own app** → point at `https://github.com/yemi-lagosinternationalmarket/lim-procurement` (branch `main`).
3. Frappe Cloud builds the bench image. Once ready, install on the site.
4. The fixture in `lim_procurement/fixtures/custom_field.json` applies on install + on every `bench migrate`. Verify by opening any Supplier — the 11 Custom Fields should appear after **Supplier Group**.

### Local bench

```bash
bench get-app https://github.com/yemi-lagosinternationalmarket/lim-procurement.git
bench --site <your-site> install-app lim_procurement
bench --site <your-site> migrate
```

## License

Unlicensed. Per ADR 0019, this app stays unlicensed while LIM uses it internally. If distribution ever becomes a concern (sell to other businesses, open-source, multi-tenant SaaS), license under **GPL v3** to align with ERPNext's GPL v3 upstream.
