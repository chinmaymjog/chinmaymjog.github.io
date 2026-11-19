---
title: Ansible Jobs in the Web Hosting Platform — Part 4
date: '2026-11-19T09:03:44.814942+05:30'
draft: true
description: 'A tour of the Jenkins jobs and Ansible playbooks behind the shared hosting
  platform: server setup, site lifecycle, HTTP auth, certificates and backups.'
tags:
- ansible
- jenkins
- hosting
- azure
- automation
canonicalURL: ''
---

[Part 3](https://chinmaymjog.github.io/posts/jenkins-ansible-automation-for-a-web-hosting-platform-part-3/)
set up Jenkins and Ansible on the Jumpbox. This part covers what you run
from them: the jobs, the playbooks behind each one, and the order to run
them in on a fresh platform.

Every job is a thin wrapper. It collects a few parameters (a domain, an
environment, a PHP version), then calls one playbook with
`ansible-playbook`. All the logic lives in the playbooks, so anything you
can click in Jenkins you can also run from the Jumpbox terminal.

The code is in
[azure-vm-hosting-solution](https://github.com/chinmaymjog/azure-vm-hosting-solution).

## Two Jenkins folders

Jobs are split into two folders:

- Administrative Tools holds server-level operations: web stack setup,
  PHP installs, backups, and removing a site.
- Hosting Management Portal holds the day-to-day site lifecycle: add,
  enable, disable, list, HTTP auth, database dumps and certificates.

The split limits blast radius. Things that change the servers or delete
a tenant sit apart from the routine work.

## Run these first

On a fresh platform, run two jobs in this order before adding any site:

1. `configure_web_server` runs `server_web_configuration.yml`. It
   updates packages, installs Apache with `mod_fcgid` and ModSecurity,
   enables the rewrite, ssl, security2, fcgid and proxy modules, creates
   the `web_users` group and the Apache auth directories, sets the group
   ID on the document root, deploys a default virtual host, and sets up
   log rotation.
2. `php_install` takes a version such as `php8.2` and installs
   PHP-FPM with the usual extensions. It also registers a templated
   systemd service so each site can later get its own FPM pool. When it
   finishes it refreshes `installed_php_versions.json`, which feeds the
   PHP version dropdown in `site_add`.

OS-level hardening is not a Jenkins job. Terraform applies SSH lockdown,
the firewall, Fail2Ban and the umask when it provisions the VM, so a web
VM is hardened from first boot instead of after someone remembers to run
a job. Ansible only handles the web layer.

## Administrative Tools

| Job | Playbook | What it does |
|---|---|---|
| `configure_web_server` | `server_web_configuration.yml` | Apache, ModSecurity, `web_users` group, default vhost |
| `php_install` | `php_install.yml` | Installs a PHP-FPM version and registers its service |
| `site_remove` | `site_remove.yml` | Removes a site completely |
| `backup_apache_config` | `backup_apache_config.yml` | Archives Apache and PHP-FPM config |
| `backup_site_config` | `backup_site_config.yml` | Archives per-site config such as `.env` files |
| `backup_databases` | `backup_databases.yml` | Dumps every tenant database |
| `ping_test` | `ping.yml` | Checks Ansible can reach the hosts |

Backups land in a timestamped layout on the shared NFS backup share
(`/backups/shrdhosting/<environment>/...`), separated by environment.
`backup_databases` lists databases at run time, skips the MySQL system
schemas by exact name, and fails the job if a dump fails, deleting the
partial file, so a green build means every database was dumped. The
database password never appears on a command line: it is fetched from
Key Vault with the Jumpbox's managed identity and passed to the dump
through the environment.

## Hosting Management Portal

| Job | Playbook | What it does |
|---|---|---|
| `site_add` | `html_site_add.yml` / `php_site_add.yml` | Onboards an HTML or PHP site |
| `site_enable` / `site_disable` | `site_enable.yml` / `site_disable.yml` | Toggles the Apache vhost and PHP-FPM service |
| `site_list` | `site_list.yml` | Lists sites from the registry |
| `http_auth_add` / `enable` / `disable` | `http_auth_*.yml` | Basic auth per site |
| `db_dump` | `db_dump.yml` | On-demand dump of one site's database |
| `generate_csr` | `generate_csr.yml` | Private key and CSR, optionally with SAN |
| `generate_pfx` | `generate_pfx.yml` | Bundles a signed certificate into a PFX and uploads it to Key Vault |

`site_add` does the most. One job takes the domain, the site type and,
for PHP, the version, and picks the matching playbook. For a PHP site the
run validates the FQDN, fetches the MySQL admin password from Key Vault,
creates a dedicated system user, the site directories and log files, a
`.env` outside the public root, an Apache virtual host and a PHP-FPM
pool. It then creates the database and database user and writes a JSON
record of the site to the shared registry under `/backups/sites`.

The registry keeps the other jobs simple. `site_enable`, `site_disable`,
`site_remove`, `site_list` and the HTTP auth jobs read the site's record
to learn what exists, whether it has PHP, and which database belongs to
it, instead of guessing from file names on one server. Because the
registry is on shared storage, every web VM sees the same answer.

## Why one playbook per job

One playbook per task keeps the blast radius small: a change to
`site_disable.yml` cannot break `site_add`. The operator's click and the
engineer's terminal run the same file. Adding a capability means adding a
playbook and a job definition in Git, and both go through a pull request.
