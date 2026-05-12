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

## What this app contains (planned)

- **Supplier Custom Fields**: `agent_authority`, `tone_reference_message_id`, `frequency`, `follow_up_level`, `default_lead_time_days`, `order_minimum_text`, `vendor_sends_truck`, `we_arrange_freight`, `freight_fee`, `pallet_fee`, `statement_email_or_url` (see b2b-starter issue [#31](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/31))
- **Item Custom Fields**: `storage_type`, `is_perishable`, `default_buy_unit`, `notes_for_agent` (see [#32](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/32))
- **Purchase Order workflow + Custom Fields + whitelisted REST methods**: `create_po_draft`, `mark_po_sent`, `mark_po_confirmed`, `mark_po_needs_review`, `cancel_po`, `resolve_placeholder` (see [#33](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/33))
- **`LIM Activity` Custom DocType**: polymorphic audit log + Frappe hooks emitting Activities on PO submit / cancel / Supplier authority changes (see [#34](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/34))
- **Notion catalog seed script**: imports historical Supplier / Item / Item Supplier data (see [#35](https://github.com/yemi-lagosinternationalmarket/b2b-starter/issues/35))

## Setup

To install on a Frappe bench (Frappe Cloud auto-handles this once the app is added to the site):

```bash
bench get-app https://github.com/yemi-lagosinternationalmarket/lim-procurement.git
bench --site lagosinternationalmarket.v.frappe.cloud install-app lim_procurement
bench --site lagosinternationalmarket.v.frappe.cloud migrate
```

LIM's production site: `https://lagosinternationalmarket.v.frappe.cloud/`

## License

Unlicensed. Per ADR 0019, this app stays unlicensed while LIM uses it internally. If distribution ever becomes a concern (sell to other businesses, open-source, multi-tenant SaaS), license under **GPL v3** to align with ERPNext's GPL v3 upstream.
