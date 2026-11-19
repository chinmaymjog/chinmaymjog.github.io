---
title: Jenkins + Ansible Automation for a Web Hosting Platform — Part 3
date: '2026-11-18T19:03:45.654219+05:30'
draft: true
description: How a Dockerized Jenkins on the Jumpbox, configured as code, gives operators
  a click-and-run front end over Ansible playbooks for site onboarding and backups.
tags:
- jenkins
- ansible
- docker
- hosting
- azure
canonicalURL: ''
---

[Part 1](https://chinmaymjog.github.io/posts/architecture-of-a-shared-hosting-platform-on-azure-part-1/)
covered the architecture and
[Part 2](https://chinmaymjog.github.io/posts/deploying-azure-infrastructure-using-terraform-part-2/)
the Terraform. This part covers what sits on top of that
infrastructure: a Jenkins instance that gives operators a click-and-run
interface, with Ansible doing the work underneath.

Operators should be able to add a website, toggle HTTP authentication or
take a backup without SSHing into a web server. Jenkins is the front end
and Ansible is the engine.

All the code is in
[azure-vm-hosting-solution](https://github.com/chinmaymjog/azure-vm-hosting-solution).

## What the platform can do

Once Jenkins is up, these tasks run from a button instead of a shell:

- Configure the Apache and PHP-FPM web servers and install PHP versions
- Add, enable, disable and remove HTML or PHP sites
- Turn HTTP authentication on and off per site
- Generate certificate signing requests and PFX bundles
- Back up Apache config, per-site config and databases
- List the sites that exist

Underneath are nearly twenty Ansible playbooks, one per task, and a
Jenkins job wrapping each of them.

## How the pieces fit

![Mermaid Diagram](/images/jenkins-ansible-automation-for-a-web-hosting-platform-part-3/mermaid_8195c3a52484.png)

- The Jumpbox is the single entry point. Jenkins runs there in a Docker
  container and is not exposed publicly; operators reach it through an
  SSH tunnel to `localhost:8080`.
- Jenkins and Ansible share one image. The Dockerfile starts from
  `jenkins/jenkins:lts`, installs the plugins from `plugins.txt`, and adds
  Ansible with `apt`. The `infra/ansible` directory is mounted into the
  container at `/etc/ansible`, so the playbooks Jenkins runs are the same
  files in the repo.
- Jenkins is configured as code. Jenkins Configuration as Code
  (`casc.yaml`) defines the admin user, the security settings and the SSH
  credential Ansible uses. The jobs themselves are checked in as XML under
  `infra/jenkins/jobs`, so a fresh container comes up with everything in
  place and no setup wizard.
- Secrets are injected at start time. `make jenkins-up` passes the admin
  password and the SSH private key to the container as environment
  variables, and neither is written into the image or the repo.

## From repo to running portal

Two Make targets do the work:

```bash
make jenkins-sync   # build the Ansible inventory from Terraform outputs and rsync infra/ to the Jumpbox
make jenkins-up     # docker compose up --build -d on the Jumpbox
```

`jenkins-sync` generates the inventory from the Terraform output of the
platform stack, so the Ansible `hosts` file always matches the VMs that
actually exist. That is what makes the playbooks safe to run against a
fleet that changes size.

## What an operator does

Jobs live in two folders: Hosting Management Portal for day-to-day site
work and Administrative Tools for server configuration and backups. To
add a site the operator opens `site_add`, enters the domain, picks `html`
or `php`, and for PHP picks a version. The PHP version list is not
hardcoded: a cascading parameter reads `installed_php_versions.json`,
which the server-configuration and PHP-install playbooks update after
they run.

The job runs the matching playbook across all web VMs at once. Before
touching anything it validates the domain, and for PHP sites it fetches
the MySQL admin password from Azure Key Vault using the Jumpbox's
managed identity, so no database password lives in a job definition or
a vars file.

The same pattern covers backups. Each backup job runs one playbook for
the preproduction and production host groups, writing to the shared NFS
backup share mounted on the hosts.

If you prefer the terminal, every job has a direct equivalent:

```bash
ansible-playbook -i /etc/ansible/hosts /etc/ansible/playbooks/php_site_add.yml \
  --extra-vars "site_url=mytestsite.com php_version=php8.1"
```

## Why this shape works

Jenkins always calls the same playbook, so a task runs the same way the
first time and the fiftieth. Teams use Jenkins without needing SSH
access to the web VMs. A new capability is a new playbook plus a new job
definition in the repo, and Jenkins config, jobs and playbooks all go
through Git like the Terraform does.

One limitation: this is a single Jenkins instance on a single Jumpbox.
That is a reasonable trade for this platform's size, and the decision is
recorded in the repo's architecture notes along with the condition for
revisiting it.

## What's next

Part 4 goes through the individual Ansible jobs and the playbooks behind
them.
