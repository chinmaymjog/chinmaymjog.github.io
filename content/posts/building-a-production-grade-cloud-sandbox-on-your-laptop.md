---
title: Building a Production-Grade Cloud Sandbox on Your Laptop
date: '2026-11-20T17:46:05.462156+05:30'
draft: true
description: How I built CloudOps-Sandbox, a local cloud lab on Docker Compose with
  Traefik ingress, one PostgreSQL server and one folder per tool, and what I removed
  to keep it simple.
tags:
- docker
- traefik
- devops
- platform-engineering
canonicalURL: ''
---

![CloudOps-Sandbox hero image](/images/building-a-production-grade-cloud-sandbox-on-your-laptop/cloudops-sandbox-hero.png)

As a cloud infrastructure architect I keep hitting the same choice. I can spend hours and real money spinning up a cloud environment just to test something, or I can settle for a local setup that has none of the routing and TLS patterns of production.

I wanted a lab on my laptop that behaves like a small cloud provider: every tool gets its own hostname behind one entry point, there is one database server, and adding a service doesn't mean touching everything else. That became [CloudOps-Sandbox](https://github.com/chinmaymjog/cloudops-sandbox).

## The design

Most local labs are a pile of Docker Compose files. I treated this one as a small platform problem, so a few rules hold everywhere.

![Mermaid Diagram](/images/building-a-production-grade-cloud-sandbox-on-your-laptop/mermaid_95f418271315.png)

Each tool lives under `stacks/` with its own `docker-compose.yml`. The stacks share a Docker network called `control-plane` and read the same root `.env`, so a tool can be added or dropped without touching the others.

Traefik is the only thing that publishes ports 80 and 443. Every app is reachable at `https://<name>.<APP_DOMAIN>`, so I never have to remember that Grafana was on 3000 and n8n on 5678.

There is one PostgreSQL server, and each app gets its own user and database on it. Data lives in Docker named volumes instead of bind mounts, which avoids the permission problems you get on macOS and Linux. Only the Traefik and Prometheus config files are mounted from the repo.

The starter set is Traefik, PostgreSQL, Prometheus, Grafana, n8n, Portainer, WUD and Pi-hole. Image versions are pinned in `.env`, never `latest`.

## Three ways to reach it

The access mode comes down to a single variable, `APP_DOMAIN`:

| Mode | Where | `APP_DOMAIN` | Certificate |
| :--- | :--- | :--- | :--- |
| A | Laptop (default) | `127.0.0.1.nip.io` | Self-signed |
| B | Remote VM | `<VM_PUBLIC_IP>.nip.io` | Self-signed |
| C | Your own domain | `lab.yourdomain.com` | Real, via Cloudflare DNS |

nip.io is what makes the default need no configuration. `grafana.127.0.0.1.nip.io` resolves to `127.0.0.1` with no DNS setup and no `/etc/hosts` edits. The certificate is self-signed, so the browser warns once, and that is expected.

For a real domain, Traefik uses a Cloudflare DNS-01 challenge to get a valid Let's Encrypt wildcard certificate. In nip.io mode there is no Cloudflare token, so Traefik logs ACME errors. They are harmless.

If you're behind NAT with no open ports, there's also a Cloudflare Tunnel option. It lives on the `advanced` branch, along with the extra stacks I use myself.

## What I took out

My first version had more machinery: a `sync-dbs` workflow, database init scripts, generated environment files and Compose profiles. I removed all of it on 2026-10-12.

Adding a service meant editing four places, and each layer hid its own failures. When something broke I was debugging my scripts instead of the service. Now the whole flow is commands you can read:

```bash
cp .env.template .env        # replace every TODO with `openssl rand -hex 16`
make up STACKS=pgsql         # database first
make up                      # everything else
```

The `Makefile` does one thing. It loops over the `STACKS` list and runs `docker compose --env-file .env -f stacks/<name>/docker-compose.yml up -d` for each one. Its other targets are `down` and `status`.

The cost is that I create databases by hand, one `docker exec postgresql psql` command per app. If I skip that step, n8n or Grafana sits in a restart loop with `password authentication failed` until the database exists, then recovers on its own. I think that's the right trade, because the failure is visible and the fix is one command.

Adding your own service is the same idea: copy `template/` to `stacks/myapp`, add its values to `.env`, add the name to `STACKS`, and run `make up`.

## Why this matters

A local lab is where I prototype and test ideas, so I built it with the habits I'd want in a larger environment: pinned versions, one ingress, isolated stacks and real certificates when I have a domain. Removing the automation that hid failures taught me as much as adding the pieces did.

The full source and setup instructions are on GitHub: [CloudOps-Sandbox](https://github.com/chinmaymjog/cloudops-sandbox).
