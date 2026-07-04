# CI workflow files (staging)

These two files belong under `.github/workflows/` but are parked here because
the automation that opened this branch pushes with a token that lacks the
GitHub `workflow` OAuth scope (GitHub rejects any push that creates or edits
files under `.github/workflows/` without it).

A maintainer (or any push with `workflow` scope) should move them into place:

```bash
git mv deploy/ci/deploy.yml .github/workflows/deploy.yml
mv deploy/ci/validation.yml .github/workflows/validation.yml   # overwrites the existing one
git add .github/workflows/validation.yml
git commit -m "CI: add deploy workflow, bump validation matrix to Python 3.12"
```

- **`deploy.yml`** — new. Runs the Ansible deploy (`deploy/deploy.yml`) on every
  published release and via `workflow_dispatch`. Targets the `production`
  environment and reads `DEPLOY_HOST` / `DEPLOY_HOST_KEY` (variables) and
  `DEPLOY_SSH_KEY` (secret) from it. See [`../README.md`](../README.md).
- **`validation.yml`** — replacement for the existing test workflow; the only
  change is the Python matrix (`3.11` → `3.12`), required by krcg v5.
