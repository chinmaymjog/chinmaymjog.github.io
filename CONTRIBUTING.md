# Contributing

This is a personal blog. Corrections (typos, broken links, factual errors) are
welcome as issues or small pull requests; new posts are written by the owner.

- Open an issue before larger changes.
- Check that the site builds: `hugo --gc --minify`.
- One logical change per pull request, referencing the issue (`Fixes #N`).

## AI-assisted contributions

AI tools are welcome, with these rules:

- **You are accountable** for every line you submit. Read and understand the
  change; unreviewed AI output will be closed.
- **Disclose** substantial AI assistance in the PR description.
- AI-generated posts or large rewrites of the author's content are not accepted.
- Low-effort, bulk or off-topic AI-generated PRs and issues may be closed
  without review.

## Maintainer automation

The Claude agent GitHub workflow is restricted to the repository owner. Agent
pull requests get the same review as any other and are never auto-merged;
merging deploys the site.

## Security issues

See [SECURITY.md](SECURITY.md); do not file them as public issues.
