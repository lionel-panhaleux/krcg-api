# Deploying krcg-api

Ansible deploy for the KRCG API, built on the shared roles from
[server-setup](https://github.com/lionel-panhaleux/server-setup)
(the `lionel_panhaleux.server_setup` collection).

## What it does

`deploy.yml` (run against a single host) provisions:

- a `krcg_api` system user and an `/opt/krcg-api` virtualenv on Python 3.12
  (provisioned with [uv](https://docs.astral.sh/uv/));
- the latest `krcg-api` release from PyPI installed into that venv;
- a `krcg_api.service` systemd unit running uvicorn on `127.0.0.1:8000`
  (data is loaded in memory per worker, so `krcg_api_workers` defaults to 2);
- an nginx reverse-proxy vhost for `api.krcg.org` with automatic Let's Encrypt
  issuance, via the `nginx_site` role in `proxy` mode.

All app logs (the uvicorn service and the nginx site) land in journald under the
shared `krcg_api` tag:

```bash
journalctl -t krcg_api -f
```

## Variables

Override at the play/CLI level as needed:

| variable             | default          | meaning                                   |
| -------------------- | ---------------- | ----------------------------------------- |
| `krcg_api_domain`    | `api.krcg.org`   | public hostname (nginx + Let's Encrypt)   |
| `krcg_api_port`      | `8000`           | local port uvicorn binds (proxied)        |
| `krcg_api_workers`   | `2`              | uvicorn worker processes                  |
| `krcg_api_user`      | `krcg_api`       | service user                              |
| `krcg_api_home`      | `/opt/krcg-api`  | install tree (venv lives here)            |

## Running from CI

> The CI workflow lives in [`ci/deploy.yml`](ci/deploy.yml) and must be moved to
> `.github/workflows/deploy.yml` by a maintainer — see [`ci/README.md`](ci/README.md).


The deploy workflow runs on every published release and via
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
