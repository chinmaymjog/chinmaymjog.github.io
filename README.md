# chinmaymjog.github.io

My technical blog - Kubernetes, Terraform, Azure, and platform
engineering notes. Built with [Hugo](https://gohugo.io/) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme,
deployed to GitHub Pages via GitHub Actions on every push to `main`.

Live at [chinmaymjog.github.io](https://chinmaymjog.github.io/).

## Local development

```bash
git clone --recurse-submodules git@github.com:chinmaymjog/chinmaymjog.github.io.git
cd chinmaymjog.github.io
hugo server -D
```

`-D` includes drafts. Open http://localhost:1313/.

## Writing a post

```bash
hugo new posts/my-post-slug.md
```

Edit the generated front matter (`title`, `description`, `tags`) and set
`draft: false` when it's ready to publish. Pushing to `main` deploys
automatically.

Most posts here are written and formatted via
[`content-ops`](https://github.com/chinmaymjog/content-ops) rather than
by hand - see that repo for the actual publishing workflow (Hugo +
Medium cross-post + LinkedIn companion post from one markdown source).

## Updating the theme

PaperMod is a git submodule:

```bash
git submodule update --remote --merge themes/PaperMod
```
