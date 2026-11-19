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
Azure. It hosts PHP-based CMS sites like WordPress, much like
traditional shared hosting, but fully automated and cloud-native.

## What I set out to build

The requirements were easy to state and harder to deliver:

- Host multiple websites on a LAMP-style stack
- Support multiple PHP versions
- Achieve high availability and performance
- Ensure secure access and traffic flow
- Integrate CI/CD for deployments
- Provide monitoring and logging

## What's in the platform

I split the implementation into layers to keep it modular:

- Architecture: a Hub-Spoke design with a shared management hub
  (Jenkins jumpbox, Key Vault, backups) peered to a platform spoke that
  runs the hosting VMs, with Azure Front Door and a Load Balancer in
  front
- Infrastructure provisioning with Terraform
- Configuration management with Ansible, which sets up Apache and PHP
  across the compute fleet
- Jenkins as the deployment and operations portal. It runs Dockerized
  on the hub's jumpbox instead of as a separate managed service

Follow-up posts cover each layer in more depth.

**Repo**: [azure-vm-hosting-solution](https://github.com/chinmaymjog/azure-vm-hosting-solution)
