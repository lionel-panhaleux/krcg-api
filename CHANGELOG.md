# Changelog

## 4.0 (2026-07-04)

- BREAKING CHANGE: upgrade to krcg v5. Cards and decks are now served in the
  [krcg v5](https://github.com/lionel-panhaleux/krcg) JSON format.
  - Cards expose the v5 model (`prints`, `i18n`, `text`, `legal`, `variants`, …)
    instead of the previous `sets`/`scans`/`card_text`/`legality` shape.
  - Decks expose a flat `cards` list of entries (`id`, `count`, `kind`, `types`,
    `comment`) instead of the `crypt`/`library` sections; tournament metadata
    moves under `event`.
  - `/convert` JSON input/output now uses the v5 deck shape; added `txt` and
    `vdb` plain-text output formats.
- Requires Python 3.12+.
- API reference served with [Scalar](https://scalar.com) at `/docs` (root
  redirects there). Card search filter values are enumerated in the OpenAPI
  schema and operation ids match handler names, for clean generated SDKs.
- New Ansible deploy under `deploy/` (server-setup collection), run by CI on
  every published release. Two API versions run side by side during the
  migration window: `v3.api.krcg.org` (legacy 3.x, pre-v5 JSON) and
  `v4.api.krcg.org` (this version). `api.krcg.org` stays on v3 for now and
  will switch to v4 at the end of the window.
- CORS moved out of the app: api.krcg.org serves permissive CORS headers from
  nginx for the whole site. If you self-host, add CORS at your reverse proxy
  (or wrap the ASGI app in a CORS middleware) for browser clients.
- Releases are now published by CI (PyPI trusted publishing + GitHub release).


## 3.4 (2025-11-01)

- Upgrade build system (uv, just, hatchling, coverage)

## 3.3 (2025-10-09)

- Bump krcg (New Blood III)

## 3.2 (2025-02-28)

- Bump krcg (V5 Hecata)

## 3.1 (2024-09-15)

- Removed deprecated "submit ruling" endpoint. Direct users to https://rulings.krcg.org from now on.

## 3.0 (2024-09-15)

- BREAKING CHANGE: New rulings format. Now an array of objects.
- FLIGHT is now always upper-case

## 2.22 (2024-07-20)

- Added `legality` date to cards
- 30th anniversary release
- Bump KRCG (3.12)

## 2.21 (2024-02-08)

- Add OpenAPI validator
- Upgrade OpenAPI to 3.1
- Use Python 3.11
- New packaging
- Fix tests

## 2.20 (2022-11-21)

- Fix /vdb endpoint (bug)

## 2.19 (2022-11-20)

- Bump KRCG (2.32)
- Fix /vdb endpoint (new URL format)

## 2.18 (2022-11-16)

- New fields in card: `_set` and `ordered_sets`
- Bump KRCG (2.30)

## 2.17 (2022-11-14)

- Bump KRCG (2.30)

## 2.16 (2022-10-05)

- Bump KRCG (2.29)
- Improve twda/list endpoint and documentation

## 2.15 (2022-08-08)

- Bump KRCG (2.23)
- Update VDB domain name (now vdb.im)
- Update python version for tests (3.9)

## 2.14 (2022-01-17)

- Bump KRCG (2.21)

## 2.13 (2021-12-04)

- Adapt to V5 Anarch
- Additional fields for crypt cards: "has_advanced", "has_evolution", "is_evolution"
- Standard card names now always include the group in parenthesis for crypt cards
- Crypt cards have a new field "printed_name" (non-unique)

## 2.12 (2021-08-27)

- Bump KRCG version

## 2.11 (2021-08-22)

- New endpoints: twda/list and twda/random

## 2.10 (2021-07-22)

- Fix VDB endpoint for form-encoded data

## 2.9 (2021-07-09)

- Improve logging

## 2.8 (2021-07-08)

- Bump KRCG version

## 2.7 (2021-03-02)

- Additional rulings
- Fix Lackey export

## 2.6 (2021-01-27)

- Unquote/decode text parameters in URL path
- Fix players_count search parameter for the TWDA

## 2.5 (2021-01-11)

- Provide card scans URLs for all prints

## 2.4 (2020-12-30)

- Add /vdb endpoint to fetch a deck from VDB

## 2.3 (2020-12-21)

- Fix the way multi-valued search filters are handled

## 2.2 (2020-12-21)

- Fix Python 3.7

## 2.1 (2020-12-21)

- Minor fixes (doc, packaging)

## 2.0 (2020-12-20)

- Initial stable release
