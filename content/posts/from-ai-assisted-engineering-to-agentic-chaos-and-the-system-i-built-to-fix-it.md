---
title: From AI-Assisted Engineering to Agentic Chaos, and the System I Built to Fix
  It
date: '2026-11-23T08:44:20.116682+05:30'
draft: true
description: Agentic IDEs made me faster and worse at engineering. The fix was a stable
  process in version-controlled markdown, now a template repo, not another tool.
tags:
- ai
- platform-engineering
- devops
- workflow
canonicalURL: ''
---

I have spent most of my career on infrastructure, DevOps and platform engineering. Automation scripts, Terraform, Kubernetes manifests, Helm charts, CI/CD pipelines and config files are my daily work. As GitOps spread, I started treating infrastructure and configuration as code, and everything moved into Git: versioned, reviewable, reproducible.

Then AI arrived.

## The honeymoon

Like many engineers, I started with AI-assisted development in the editor. I tried extensions from almost every major provider, and at first it felt great. AI helped me:

- improve automation scripts
- generate Terraform modules
- modify Kubernetes manifests
- create configuration files
- refactor repetitive code

Inline suggestions were useful, file edits were fast, and boilerplate stopped costing me time. It felt like having an engineering assistant.

Then I moved to agentic IDEs. I loved the speed and autonomy at first. Watching an AI system read a repository, change several files and finish a task end to end felt futuristic.

## Where it went wrong

Slowly, friction showed up. The AI started:

- making architectural decisions on its own
- modifying files outside the requested scope
- forgetting constraints from earlier in the conversation
- optimizing for finishing the task instead of working with me

That is the trade-off of the newer agent-first IDEs from OpenAI, Google, Anthropic and others. The more autonomous the tool got, the more my role shifted toward reviewing, approving and reacting, and away from engineering, understanding and designing.

I came to an uncomfortable conclusion: agentic IDEs can hurt learning. The models are fine. They collapse too many decisions into automation, skip the explanation, generate complexity nobody asked for, and reward velocity over understanding. Autonomy feels productive at first, and later it shows up as architectural entropy.

My own habits got worse too. I was:

- switching tools constantly
- changing workflows every few weeks
- losing context between projects
- abandoning half-finished work
- restarting from scratch

Eventually I saw that my gap was a stable system for ideas, planning, execution, publishing and keeping what I learned. Another AI IDE would not have filled it. I needed an engineering operating system.

## From tool-driven to process-driven

I stopped chasing the perfect AI tool and built a stable process instead. It began as a repository called `engineering-system`: my idea vault, template library, AI workflow memory, patterns library and publishing system, all in plain folders.

The idea I took from it is the one that mattered most: AI memory belongs in version-controlled markdown files, not in chat history.

Every project now starts with the same small set of documents, so the AI (and I) get the same context every time:

- `docs/project-spec.md` for what is being built and why, with requirement IDs
- `docs/architecture.md` for components, trade-offs and a decision record whenever a non-trivial choice is made
- `docs/tasks.md` for the task tracker, where a task enters "Now" only when its scope is small, its requirement IDs are known and its validation is named up front
- `CLAUDE.md` for the rules the agent works under

With the same context every time, the chaos dropped a lot.

## The template repo

The `engineering-system` repo has since been archived. Its useful parts live in [project-template](https://github.com/chinmaymjog/project-template), a GitHub template repository I start every new project from. Folding it in also led me to trim the document set. The first version had separate files for AI rules, decisions, session briefs and lessons learned. In practice, decisions belong in the architecture doc and the rules belong next to the code, so the extra files mostly went unread.

The template also carries guardrails that no longer depend on my memory:

- a bootstrap script that applies standard GitHub settings: secret scanning with push protection, read-only workflow tokens and a `protect-main` ruleset that requires a pull request plus passing checks
- a Gitleaks secret scan in CI
- a Claude agent workflow that only runs when the repository owner mentions `@claude`, with no cloud credentials and no auto-merge
- contribution rules for AI-assisted changes: you are accountable for every line, and substantial AI help gets disclosed in the PR

The agent's own hard rules are short: no cloud credentials, never run deploy, apply or destroy against real systems, never commit secrets, pin versions and never use `latest`.

## How I work with AI now

I still use AI heavily, but the relationship changed. AI acts as planner, reviewer, implementation accelerator and assistant. I stay the architect, operator, reviewer and decision maker.

The biggest behavioral change is in my prompts. They used to look like this:

```text
Build the entire system
```

Now they look like this:

```text
Implement task 2 only.

Allowed:
- modify Helm manifests

Not allowed:
- CI/CD changes
- Terraform changes
- new dependencies

Explain plan before coding.
Wait for approval.
```

This one change improved output quality a lot.

Human review is mandatory again. Every task goes through the same loop:

```text
Plan -> Implement -> Review diff -> Validate architecture -> Continue
```

I apply it to everything, and most strictly to Kubernetes, Terraform, CI/CD, observability pipelines and infrastructure automation, because uncontrolled automation in platform engineering has a very large blast radius.

## The lesson

What goes wrong with modern AI tooling is unconstrained autonomy. AI is extremely useful when the architecture is documented, the constraints are explicit, the tasks are scoped and a review loop exists. Without those guardrails it slowly introduces architectural drift, hidden complexity, inconsistent patterns and context instability.

My working rules today:

- AI assists, human decides
- Plan before implementation
- One task at a time
- Review every diff
- Markdown docs are the source of truth
- No autonomous infra actions
- No architecture redesign without approval
- Keep sessions short
- A stable process beats a new tool

## Final thoughts

I no longer believe the future of engineering is fully autonomous AI development, at least not for infrastructure, DevOps, platform engineering and systems architecture. I believe in AI-assisted engineering: humans own intent, architecture and operational responsibility, and AI speeds up implementation, learning, documentation and repetitive work.

The tools will keep changing and the models will keep improving. A stable process outlasts both.
