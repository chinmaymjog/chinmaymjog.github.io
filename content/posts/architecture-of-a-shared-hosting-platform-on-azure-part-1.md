---
title: Architecture of a Shared Hosting Platform on Azure — Part 1
date: '2026-09-16T08:37:41.022186+05:30'
draft: false
description: The Hub-Spoke design behind the shared hosting platform - Front Door,
  Load Balancer, a Jumpbox, and where the data actually lives.
tags:
- azure
- architecture
- hosting
canonicalURL: ''
---

This is Part 1 of the series on the shared hosting platform I built on
Azure. [The intro post](https://chinmaymjog.github.io/posts/building-a-shared-hosting-platform-on-azure/)
covers the goals. This one covers the architecture, which the rest of
the series builds on.

## The Hub-Spoke design

The platform uses Azure's Hub-and-Spoke model to keep shared services
central and the hosting workload isolated:

- Hub VNet: the management side. It holds a Jumpbox VM (running the
  Jenkins admin portal), Key Vault for secrets, and backup storage.
- Spoke VNet: the platform side. It holds Azure Front Door, the Load
  Balancer, the Apache/PHP web VM fleet, MySQL, and website storage.

Only two things are reachable from the public internet, and network
security groups lock down both: the Load Balancer's public IP accepts
traffic only from Front Door's backend range, and the Jumpbox's public
IP accepts SSH only from your own IP. The web VMs, MySQL, and storage
are all private.

![Hub-Spoke architecture diagram](/images/architecture-of-a-shared-hosting-platform-on-azure-part-1/hub-spoke-architecture.png)

## Key design decisions

- Azure Front Door + WAF handles SSL termination, edge caching, and
  threat detection at the edge. The WAF ships in Detection mode, so it
  logs threats but doesn't block them until you switch it to Prevention.
- Azure Load Balancer distributes traffic across the Ubuntu web VM
  fleet.
- Azure Files Premium NFS backs website storage. I started out planning
  to use Azure NetApp Files, but NetApp needs a minimum 4 TiB capacity
  pool and, on many subscriptions, a manual quota approval. That is a
  real barrier for a first attempt, and Premium NFS gets most of the way
  there at a fraction of the cost. NetApp is still available on the
  repo's `advanced` branch for anyone who needs sub-millisecond latency
  at production scale.
- Azure Database for MySQL (Flexible Server) is private-only, reachable
  from the spoke over Private DNS rather than a public endpoint.
- Key Vault holds the DB password and SSH private key, fetched at
  provision time via the Jumpbox's managed identity. Neither is written
  to disk or committed anywhere.
- Network Security Groups keep only ports 80/443 open publicly;
  everything else is SSH-key-only, IP-restricted access to the Jumpbox.

I didn't end up needing Azure Bastion. A single Jumpbox VM with
key-only SSH and Fail2Ban gives the same "one hardened entry point"
without the extra managed-service cost.

## Connection flow

1. A user hits the app over HTTPS via Azure Front Door
2. Front Door routes to the Azure Load Balancer
3. The Load Balancer distributes across the Ubuntu web VMs
4. App files are served from Azure Files Premium NFS
5. Database queries go to MySQL Flexible Server over the VNet, resolved through Private DNS

## One environment, not several

The original plan called for separate production and preproduction
spokes. Running two full spoke environments doubles the VM, database
and storage cost just to try the platform, so the Terraform on this
repo's `main` branch deploys a single environment. The `advanced`
branch keeps the preprod/prod workspace split for anyone who wants it.

Next up is deploying all of this with Terraform.

**Repo**: [azure-vm-hosting-solution](https://github.com/chinmaymjog/azure-vm-hosting-solution)
