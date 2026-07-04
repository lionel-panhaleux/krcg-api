# Deploying krcg-api

Ansible deploy for the KRCG API, built on the shared roles from
[server-setup](https://github.com/lionel-panhaleux/server-setup)
(the `lionel_panhaleux.server_setup` collection).

## What it does

`deploy.yml` (run against a single host) provisions **two API versions side by
side**, each with its own venv (Python 3.12, provisioned with
[uv](https://docs.astral.sh/uv/)), systemd service and nginx vhost with
automatic Let's Encrypt issuance:

| version | package (PyPI)      | stack             | domain             | CORS            |
| ------- | ------------------- | ----------------- | ------------------ | --------------- |
| `v3`    | `krcg-api<4, krcg<5`| Flask / gunicorn  | `v3.api.krcg.org`  | served by app   |
| `v4`    | `krcg-api>=4,<5`    | FastAPI / uvicorn | `v4.api.krcg.org`  | served by nginx |

The apex `api.krcg.org` is an nginx alias on the version selected by
`krcg_api_live` (currently `v3`). To switch the apex to v4 at the end of the
migration window, set `krcg_api_live: v4` and re-run the playbook — the
nginx_site role expands the v4 TLS certificate automatically.

DNS for `v3.api.krcg.org`, `v4.api.krcg.org` and `api.krcg.org` must point at
the server before the first run (Let's Encrypt HTTP-01).

Logs land in journald, one tag per version:

```bash
journalctl -t krcg_api_v3 -f
journalctl -t krcg_api_v4 -f
```

## Variables

Override at the play/CLI level as needed:

| variable             | default          | meaning                                    |
| -------------------- | ---------------- | ------------------------------------------ |
| `krcg_api_domain`    | `api.krcg.org`   | apex hostname (versions serve `vN.` + it)  |
| `krcg_api_live`      | `v3`             | version the apex domain is an alias of     |
| `krcg_api_versions`  | see playbook     | per-version pins, port, server, CORS       |
| `krcg_api_workers`   | `2`              | worker processes per version               |
| `krcg_api_user`      | `krcg_api`       | service user                               |
| `krcg_api_home`      | `/opt/krcg-api`  | install tree (one venv per version inside) |

## Running from CI

The [deploy workflow](../.github/workflows/deploy.yml) runs on every published release and via
`workflow_dispatch`. It targets the `production` GitHub environment and reads,
from that environment:

- `DEPLOY_HOST` (variable) — the target server IP;
- `DEPLOY_HOST_KEY` (variable) — the server's SSH host key line;
- `DEPLOY_SSH_KEY` (secret) — the private deploy key.

These are pushed to the repo by server-setup's `just sync` / `just sync-key`
recipes (krcg-api maps to the `strasbourg` host in server-setup's
`deploy-targets.yml`).

## Running locally

```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook deploy.yml -i "1.2.3.4," --user deploy --private-key ~/.ssh/deploy
```

(Run from this `deploy/` directory so `ansible.cfg` is picked up. Add
`--check --diff` for a dry run.)

Before the first run, decommission the old Flask/uWSGI deployment once with
[`cleanup.yml`](cleanup.yml).
