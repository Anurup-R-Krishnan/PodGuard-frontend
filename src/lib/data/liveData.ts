export type DashboardVulnerability = {
  id: string;
  score: number;
  cvss: number;
  epss: number;
  reachability: number;
  pkg: string;
  fix: string | null;
  image?: string;
};

export type DashboardData = {
  image: string;
  scannedAt: string;
  metrics: {
    total: number;
    critical: number;
    high: number;
    alertReduction: number;
  };
  vulnerabilities: DashboardVulnerability[];
};

export async function loadLiveDashboardData(): Promise<DashboardData> {
  const response = await fetch("/data/live_data.json", {
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`live_data.json request failed: ${response.status}`);
  }

  return (await response.json()) as DashboardData;
}
