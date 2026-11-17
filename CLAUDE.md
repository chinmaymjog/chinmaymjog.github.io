# chinmaymjog.github.io

Personal technical blog (Kubernetes, Terraform, Azure, platform engineering). Hugo with the PaperMod theme (git submodule in `themes/PaperMod`), config in `hugo.yaml`, posts in `content/posts/`, deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## Hard rules
- **Merging to `main` publishes the site.** Keep changes small and reviewable.
- Never create, publish or substantially rewrite blog posts unless the issue explicitly asks. New posts must start with `draft: true`. Don't change the author's voice or technical claims in existing posts; for corrections, make the minimal fix and say what changed.
- Don't edit `themes/PaperMod` (submodule); override with files in `layouts/`, `assets/` or `i18n/` instead.
- Don't change `.github/workflows/` unless the issue asks for it. If `HUGO_VERSION` is bumped, update `HUGO_SHA256` in both `deploy.yml` and `claude-agent.yml` from the release's checksums file.
- Never commit secrets, analytics tokens or private data. Don't add third-party scripts or trackers without an explicit request.

## Working on issues
- Verify the site builds: `hugo --gc --minify --destination /tmp/public` (exit code 0, no new warnings).
- Keep changes minimal and scoped to the issue; one issue per PR.
- Open a PR against `main` that references the issue (`Fixes #N`). Never push to `main` directly.
