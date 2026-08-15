# PodGuard dashboard

A Svelte dashboard for exploring container vulnerabilities prioritised with CVSS, EPSS, reachability, and a combined remediation score.

This repository contains only the dashboard. The scanner and report generator live in [PodGuard](https://github.com/Anurup-R-Krishnan/PodGuard).

## Features

- Search by CVE or package
- Sort by composite score, CVSS, EPSS, or package
- Filters for high-priority, fixable, and high-CVSS/low-priority findings
- Detailed vulnerability panel with scoring inputs and fixed-version data
- Live JSON loading with a bundled fallback snapshot
- Responsive Svelte 5 interface

## Run locally

Requirements: Node.js and npm.

```bash
npm ci
npm run dev
```

Open the URL shown by Vite, normally `http://localhost:5173`.

## Data

At runtime the dashboard requests `/data/live_data.json`. If it cannot load that file, it uses `src/lib/real_data.json` and displays a fallback-data warning.

To generate a fresh dataset from PodGuard JSON reports:

```bash
PODGUARD_REPORTS_DIR=/path/to/reports npm run generate:data
```

The generator deduplicates findings by CVE, keeps the highest composite score, computes summary counts, and writes `public/data/live_data.json`. When no report directory is supplied, the checked-in snapshot is preserved so a clean clone still builds.

## Verification

```bash
npm run check
npm run build
```

## Technology

Svelte 5, TypeScript, Vite, and a small Python report-conversion script.

## Interpretation

The dashboard helps order remediation work; it does not prove exploitability. A low score must not override active exploitation, a CISA KEV listing, exposed business context, or organisational policy.
