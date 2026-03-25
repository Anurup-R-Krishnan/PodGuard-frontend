#!/usr/bin/env python3
"""Generate frontend live_data.json from Phase 1 scan report outputs."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "phase1_demo_reports"
OUT_FILE = REPO_ROOT / "epss-frontend" / "public" / "data" / "live_data.json"


def _load_reports() -> list[dict]:
    reports: list[dict] = []
    for path in sorted(REPORTS_DIR.glob("epss_report_*.json")):
        try:
            reports.append(json.loads(path.read_text()))
        except Exception as exc:
            print(f"Skipping invalid report {path.name}: {exc}")
    return reports


def _make_vulnerability_rows(reports: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for report in reports:
        image_name = report.get("image", {}).get("name", "unknown")
        for vuln in report.get("vulnerabilities", []):
            rows.append(
                {
                    "id": vuln.get("cve_id", "UNKNOWN"),
                    "score": float(vuln.get("composite_score", 0.0) or 0.0),
                    "cvss": float(vuln.get("cvss_v3_score", 0.0) or 0.0),
                    "epss": float(vuln.get("epss_score", 0.0) or 0.0),
                    "reachability": float(vuln.get("reachability_score", 0.0) or 0.0),
                    "pkg": vuln.get("affected_package") or "unknown",
                    "fix": vuln.get("fixed_version"),
                    "image": image_name,
                }
            )

    # Keep highest composite score per CVE to avoid large duplicate groups.
    by_cve: dict[str, dict] = {}
    for row in rows:
        cve = row["id"]
        if cve not in by_cve or row["score"] > by_cve[cve]["score"]:
            by_cve[cve] = row

    deduped = list(by_cve.values())
    deduped.sort(key=lambda v: v["score"], reverse=True)
    return deduped


def _compute_metrics(vulns: list[dict]) -> dict:
    total = len(vulns)
    critical = sum(1 for v in vulns if v["score"] >= 0.8)
    high = sum(1 for v in vulns if 0.6 <= v["score"] < 0.8)

    cvss_critical_high = sum(1 for v in vulns if v["cvss"] >= 7.0)
    composite_critical_high = sum(1 for v in vulns if v["score"] >= 0.6)
    alert_reduction = 0.0
    if cvss_critical_high > 0:
        alert_reduction = ((cvss_critical_high - composite_critical_high) / cvss_critical_high) * 100

    return {
        "total": total,
        "critical": critical,
        "high": high,
        "alertReduction": round(max(alert_reduction, 0.0), 2),
    }


def main() -> None:
    reports = _load_reports()
    if not reports:
        raise SystemExit(f"No report files found in: {REPORTS_DIR}")

    vulns = _make_vulnerability_rows(reports)
    metrics = _compute_metrics(vulns)

    payload = {
        "image": f"phase1-demo:{len(reports)}-reports",
        "scannedAt": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "vulnerabilities": vulns,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, indent=2))
    print(f"Generated {OUT_FILE} with {len(vulns)} vulnerabilities from {len(reports)} reports")


if __name__ == "__main__":
    main()
