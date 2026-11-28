---
title: From Keeping Systems Running to Designing Intelligent Platforms
date: '2026-11-28T09:12:59.819313+05:30'
draft: true
description: How my thinking has moved from keeping infrastructure online to designing
  platforms that combine automation, identity, observability, AI and governance.
tags:
- platform-engineering
- software-architecture
- kubernetes
- azure
- gitops
- ai
canonicalURL: ''
---

Technology never stands still, and architects can't either.

Over the last few years I've realized my role is changing. I used to solve infrastructure problems. Now I'm solving business problems with infrastructure, automation, AI and governance together.

Through all of it I've kept coming back to one question:

**"What will simplify operations while making the platform more secure, scalable, and easier for teams to use?"**

## The infrastructure years

Like many infrastructure engineers, I spent years on the fundamentals:

- Building reliable Kubernetes platforms
- Designing Azure architectures
- Managing networking, ingress and identity
- Running GitLab for CI/CD
- Improving monitoring and logging
- Solving production issues

The goal was stability. If applications deployed and systems stayed online, the platform had done its job.

Cloud maturity changes that view. At some point you start seeing infrastructure as the foundation that everything else is built on.

## Thinking like a platform engineer

Once an organization runs Kubernetes at scale, every team ends up solving the same problems:

- How do we deploy applications?
- How do we manage secrets?
- How do we secure workloads?
- How do we observe production?
- How do we standardize deployments?
- How do we reduce operational overhead?

Solving these again for every team gets old quickly. The better question is how to build a platform that solves them once.

That moved my focus toward platform engineering:

- GitOps
- Self-service deployments
- Standardized Helm charts
- Workload Identity
- External Secrets
- Policy-driven governance
- Golden paths for development teams

More and more of my job became enabling developers.

## Observability is more than dashboards

Observability used to mean collecting logs. Now I think of it as understanding the system.

Modern platforms produce huge volumes of telemetry, and more data doesn't automatically give you more insight. The questions I find interesting now are these:

- What data is actually valuable?
- Can we reduce ingestion costs?
- Can OpenTelemetry simplify instrumentation?
- Can we correlate logs, metrics and traces automatically?
- How do we give people actionable insights instead of a wall of dashboards?

That makes observability an architecture problem as much as a tooling one.

## Identity instead of credentials

One of my biggest shifts has been from managing secrets to managing identity.

I used to ask:

> *Where should we store credentials?*

Now I ask:

> *Why do credentials exist at all?*

Azure Workload Identity, Managed Identity, Kubernetes service accounts and federated identity are a real step forward. A secret that never exists can't leak, and designing for that changes how applications talk to cloud services and cuts a lot of operational risk.

I've tried to apply this in my own projects. In [azure-wordpress-aks](https://github.com/chinmaymjog/azure-wordpress-aks), AKS pulls images through its kubelet identity's `AcrPull` role (granted in the companion [azure-wordpress-aks-infra](https://github.com/chinmaymjog/azure-wordpress-aks-infra) repo), so there's no image pull secret. The repo's `advanced` branch logs GitHub Actions into Azure with OIDC, so no client secret is stored for the pipeline either.

## GitOps beyond continuous deployment

GitOps first looks like a deployment mechanism. In practice it turns into an operating model.

With tools like FluxCD, Argo CD and the GitLab Agent, Git repositories become the source of truth for infrastructure and applications. You get:

- Repeatable environments
- Auditable changes
- Faster disaster recovery
- A clear separation between desired state and runtime state

The conversation moves from "How do we deploy?" to "How do we govern deployments at scale?" My [k3s-argocd-sandbox](https://github.com/chinmaymjog/k3s-argocd-sandbox) is a small version of this, with Argo CD syncing modular stacks from Git on a laptop or a VM.

## AI is becoming part of the software delivery lifecycle

The part of my thinking that has moved the most is AI.

At first I saw LLMs as productivity tools. Today I see them as platform capabilities, and the questions have changed with that. I used to ask:

> *Which model should we use?*

Now I'm asking:

- How do we govern AI usage?
- How do we secure MCP servers?
- How do we build reusable skills?
- How do we audit AI interactions?
- How do we fit AI into the developer workflows we already have?
- How do we provide enterprise guardrails without limiting innovation?

AI infrastructure looks a lot like cloud infrastructure did a decade ago. It needs governance before it needs scale.

## Gateways everywhere

One idea that has caught my attention is how many gateways are showing up. Traditional architectures had API gateways. Modern ones keep extending the idea:

- Service gateways
- AI gateways
- LLM gateways
- MCP gateways
- Skill registries
- Agent catalogs

Beyond routing, they handle:

- Authentication
- Authorization
- Discovery
- Governance
- Auditability
- Rate limiting
- Policy enforcement
- Observability

As AI ecosystems grow, I expect gateways to become the control plane for these systems.

## Security is becoming invisible

Good security stays out of developers' way.

Instead of adding manual approvals or yet more credentials, I'd rather build security into the platform itself through:

- Zero Trust principles
- Least privilege access
- Policy-as-Code
- Automated compliance
- Identity federation
- Continuous vulnerability management

Then security is something developers inherit from the platform, and they don't have to implement it again in every project.

## Cost is an architectural decision

Cloud cost often gets treated as a finance problem. I see it more and more as an architecture problem.

Observability pipelines, Kubernetes clusters, storage, network traffic and logging all come with cost implications, and every design decision carries a price. Architects should optimize for operational efficiency and sustainability along with performance and reliability.

## What I'm learning

Looking back, my interests have slowly joined up:

- Kubernetes
- Azure
- GitOps
- Identity
- Observability
- Security
- AI
- Platform engineering
- Governance

They look like separate technologies, but I've come to see them as pieces of the same platform. The work I want to do next is designing ecosystems where infrastructure, applications, AI and governance fit together, more than mastering any one tool.

## Looking ahead

I don't think the next generation of architects will be judged only on how well they design infrastructure. They'll be judged on how well they design platforms that enable people.

Platforms that are:

- Secure by default
- Observable by design
- Governed through policy
- Automated end to end
- AI-enabled
- Cost-aware
- Easy for developers to adopt

The technology will keep changing, and architectural thinking has to change with it.

For me that's the best part of this work. Every new technology is a chance to rethink how platforms should be built, so that teams can ship with confidence on top of systems that keep running.
