---
title: Auditing Azure RBAC Shouldn't Be This Hard
date: '2026-11-22T17:09:14.676847+05:30'
draft: false
description: How I built Azure RBAC Insight, a local-first Streamlit dashboard that
  pulls role assignments from many Azure subscriptions into one filterable view, with
  live fetch or offline CSV upload.
tags:
- azure
- rbac
- security
- python
- platform-engineering
canonicalURL: ''
---

If you've ever had to review role-based access control across several Azure subscriptions, you know how it goes. You click through the Portal, open resource after resource, and try to piece together who has access to what.

I got tired of that, so I built [Azure RBAC Insight](https://github.com/chinmaymjog/azure-rbac-insight).

## The problem: Portal fatigue

The Access Control (IAM) blade is fine for checking a single resource. It falls apart when the questions are bigger:

- Which service principals have Owner access anywhere in the tenant?
- Which resources have the most direct role assignments?
- Can I see all my subscriptions in one view?

In the Portal that means a lot of clicking and a spreadsheet you build by hand.

## The solution: one local dashboard

Azure RBAC Insight is a small Streamlit app that gathers role assignments from one or more subscriptions into a single filterable view. It runs on my machine, and the RBAC data never goes to a hosted backend.

![Azure RBAC Insight dashboard](/images/auditing-azure-rbac-shouldn-t-be-this-hard/azure-rbac-insight-dashboard.png)

You pick the subscriptions you want and pull their assignments in one run, or upload CSV exports from the Azure Portal instead. Charts show role distribution, principal types and the resources with the most assignments. Filters slice by subscription, role, principal type and scope, and a detail table lets me drill into individual assignments. Nothing is stored or sent anywhere else.

![Detailed audit table](/images/auditing-azure-rbac-shouldn-t-be-this-hard/azure-rbac-insight-audit-logs.png)

## Live fetch or CSV

I kept both modes because people audit in different situations. Live mode is for a current-state sweep. It needs Reader access on the subscriptions, and it uses your local `az login` session.

The Azure SDK only returns principal object IDs, not display names. The Portal CSV export includes display names, so I use CSV mode when I need to hand a report to someone who wants to read names. It also works offline, which suits audit snapshots and restricted environments.

The app checks that an uploaded CSV has the columns it needs (`Subscription`, `RoleDefinitionName`, `ObjectType` and `ObjectId`) before it renders anything. A different export format or a hand-edited file gets a clear error instead of a crash halfway down the page. `Scope` is optional, and when it's missing the resource name shows as `Unknown`.

## Running it

Locally with Python:

```bash
git clone https://github.com/chinmaymjog/azure-rbac-insight.git
cd azure-rbac-insight
pip install -r requirements.txt
az login   # only needed for live fetch
streamlit run app.py
```

Then open `http://localhost:8501`.

There is also a Docker Compose path (`docker-compose up --build`). CSV upload works there without any setup. Live fetch needs a service principal, because the image doesn't include the Azure CLI and your local `az login` isn't visible inside the container. You pass `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` and `AZURE_TENANT_ID` through the environment or a git-ignored `.env` file. The service principal only needs Reader on the subscriptions you want to inspect.

## How it's built

It's one `app.py` using the Azure SDK for Python (`AuthorizationManagementClient`) to list assignments and map role definition IDs to names, pandas for the data, and Plotly for the charts.

Live fetch walks the subscriptions one at a time, which is fine for a handful and slow for dozens. There's no hosted or team-shared version, on purpose. RBAC exports are sensitive, and a local-only tool has a much simpler security story.

The code, user guide and architecture notes are in the [repository](https://github.com/chinmaymjog/azure-rbac-insight).
