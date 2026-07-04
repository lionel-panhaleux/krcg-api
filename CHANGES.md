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
- New Ansible deploy under `deploy/` (server-setup collection), run by CI on
  every published release. Two API versions run side by side during the
  migration window: `v3.api.krcg.org` (legacy 3.x, pre-v5 JSON) and
  `v4.api.krcg.org` (this version). `api.krcg.org` stays on v3 for now and
  will switch to v4 at the end of the window.
- CORS moved out of the app: api.krcg.org serves permissive CORS headers from
  nginx for the whole site. If you self-host, add CORS at your reverse proxy
  (or wrap the ASGI app in a CORS middleware) for browser clients.
- Releases are now published by CI (PyPI trusted publishing + GitHub release).
