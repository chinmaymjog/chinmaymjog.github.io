---
title: Building a Shared Hosting Platform on Azure
date: '2026-09-16T08:05:52.693737+05:30'
draft: false
description: Why I built a fully automated, cloud-native shared hosting platform on
  Azure, and what's in the series that follows.
tags:
- azure
- terraform
- ansible
- jenkins
- hosting
canonicalURL: ''
cover:
  image: "/images/building-a-shared-hosting-platform-on-azure/hero.jpg"
  alt: "A cPanel-style shared hosting control panel"
  relative: false
---

As part of a personal project, I built a shared hosting platform on
Azure. The goal was to support web hosting for PHP-based CMS platforms
like WordPress - similar to traditional shared hosting, but fully
automated and cloud-native.

## What I Set Out to Build

The requirements were simple to state, less simple to deliver:

- Host multiple websites on a LAMP-style stack
- Support multiple PHP versions
- Achieve high availability and performance
- Ensure secure access and traffic flow
- Integrate CI/CD for deployments
- Provide monitoring and logging

## What's Actually In the Platform

To keep it modular, I split the implementation into layers:

- **Architecture**: a Hub-Spoke design - a shared management hub (Jenkins
  jumpbox, Key Vault, backups) peered to a platform spoke running the
  actual hosting VMs, with Azure Front Door and a Load Balancer in front
- **Infrastructure provisioning** with Terraform
- **Configuration management** with Ansible - Apache/PHP runtime setup
  across the compute fleet
- **Jenkins** as the deployment and operations portal, running
  Dockerized on the hub's jumpbox rather than as a separate managed
  service

I'll be publishing follow-ups covering each layer in more depth.

**Repo**: [azure-vm-hosting-solution](https://github.com/chinmaymjog/azure-vm-hosting-solution)
