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
- New Ansible deploy under `deploy/` (server-setup collection): uvicorn systemd
  service behind nginx with Let's Encrypt, run by CI on every published release.
- Releases are now published by CI (PyPI trusted publishing + GitHub release).
