<script lang="ts">
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';
  import { expoOut } from 'svelte/easing';

  import Masthead from './lib/components/Masthead.svelte';
  import StatStrip from './lib/components/StatStrip.svelte';
  import ControlPanel from './lib/components/ControlPanel.svelte';
  import VulnerabilityGrid from './lib/components/VulnerabilityGrid.svelte';
  import VulnDetailPanel from './lib/components/VulnDetailPanel.svelte';
  import TickerTape from './lib/components/TickerTape.svelte';

  import fallbackData from './lib/real_data.json';
  import { loadLiveDashboardData, type DashboardData } from './lib/data/liveData';

  let isLoaded = $state(false);
  let searchQuery = $state('');
  let activeFilter = $state<string | null>(null);
  let sortKey = $state<'score' | 'cvss' | 'epss' | 'pkg'>('score');
  let sortDesc = $state(true);

  let dashboardData = $state<DashboardData>(fallbackData as DashboardData);
  let dataSource = $state<'live' | 'fallback'>('fallback');
  let loadError = $state<string | null>(null);

  let selectedVulnId = $state<string | null>(null);
  let selectedVuln = $derived(
    selectedVulnId ? dashboardData.vulnerabilities.find((v) => v.id === selectedVulnId) : null
  );

  onMount(async () => {
    try {
      dashboardData = await loadLiveDashboardData();
      dataSource = 'live';
      loadError = null;
    } catch (error) {
      console.warn('Falling back to bundled dashboard data:', error);
      dashboardData = fallbackData as DashboardData;
      dataSource = 'fallback';
      loadError = 'Live dataset unavailable. Showing bundled snapshot.';
    }
    isLoaded = true;
  });

  let processedVulns = $derived(() => {
    let filtered = dashboardData.vulnerabilities.filter((v) => {
      const matchSearch =
        v.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        v.pkg.toLowerCase().includes(searchQuery.toLowerCase());

      let matchSeverity = true;
      if (activeFilter === 'priority') matchSeverity = v.score >= 0.8;
      else if (activeFilter === 'ignored') matchSeverity = v.cvss >= 8.0 && v.score < 0.6;
      else if (activeFilter === 'fixable') matchSeverity = v.fix !== null;

      return matchSearch && matchSeverity;
    });

    filtered.sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];

      if (typeof valA === 'string' && typeof valB === 'string') {
        return sortDesc ? valB.localeCompare(valA) : valA.localeCompare(valB);
      }
      return sortDesc ? (valB as number) - (valA as number) : (valA as number) - (valB as number);
    });

    return filtered;
  });

  let tickerMessages = $derived(() => {
    const mode = dataSource === 'live' ? 'LIVE_DATASET' : 'FALLBACK_DATASET';
    return [
      `SOURCE: ${mode} //`,
      `TARGET: ${dashboardData.image} //`,
      `TOTAL_VULNS: ${dashboardData.metrics.total} //`,
      `CRITICAL: ${dashboardData.metrics.critical} // HIGH: ${dashboardData.metrics.high} //`,
      `ALERT_REDUCTION: ${dashboardData.metrics.alertReduction}% //`,
      `SCAN_TS: ${new Date(dashboardData.scannedAt).toISOString()} //`
    ];
  });
</script>

<svelte:head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600&display=swap');

    :root {
      --bg-paper: #f4f4f0;
      --bg-surface: #ffffff;
      --bg-inverted: #111111;

      --ink-main: #111111;
      --ink-muted: #555555;
      --ink-faint: #d4d4d0;

      --accent-vermilion: #fc440f;
      --accent-cerulean: #2a52be;
      --accent-chartreuse: #dcfc0f;

      --border-thin: 1px solid var(--ink-main);
      --border-thick: 4px solid var(--ink-main);

      --font-display: 'Syne', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --font-ui: 'Inter', sans-serif;
    }

    *, *::before, *::after {
      box-sizing: border-box;
    }

    body {
      background-color: var(--bg-paper);
      color: var(--ink-main);
      margin: 0;
      padding: 0;
      font-family: var(--font-ui);
      -webkit-font-smoothing: antialiased;
      overflow-x: clip;
    }
  </style>
</svelte:head>

<TickerTape messages={tickerMessages()} />

{#if isLoaded}
  <main class="maximal-layout" class:panel-open={selectedVulnId !== null}>
    <div class="content-core">
      <Masthead targetImage={dashboardData.image} scanDate={dashboardData.scannedAt} />

      {#if loadError}
        <div class="data-warning">{loadError}</div>
      {/if}

      <StatStrip
        total={dashboardData.metrics.total}
        critical={dashboardData.metrics.critical}
        reduction={dashboardData.metrics.alertReduction}
      />

      <ControlPanel
        bind:searchQuery
        bind:activeFilter
        bind:sortKey
        bind:sortDesc
      />

      <VulnerabilityGrid
        vulns={processedVulns()}
        bind:selectedVulnId
      />
    </div>

    {#if selectedVuln}
      <aside class="detail-sidebar" transition:fly={{ x: 400, duration: 600, easing: expoOut }}>
        <VulnDetailPanel
          vuln={selectedVuln}
          onClose={() => (selectedVulnId = null)}
        />
      </aside>
    {/if}
  </main>
{/if}

<style>
  .maximal-layout {
    display: flex;
    width: 100%;
    min-width: 0;
    min-height: 100vh;
    transition: padding-right 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .content-core {
    flex-grow: 1;
    min-width: 0;
    max-width: 100%;
    padding: 0 4vw 4vw 4vw;
    display: flex;
    flex-direction: column;
    transition: max-width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .maximal-layout.panel-open .content-core {
    max-width: calc(100% - 450px);
    padding-right: 2vw;
  }

  .detail-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: min(450px, 100vw);
    height: 100vh;
    background: var(--bg-surface);
    border-left: var(--border-thick);
    z-index: 100;
    overflow-y: auto;
    box-shadow: -20px 0 40px rgba(0, 0, 0, 0.05);
  }

  .data-warning {
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    border: var(--border-thin);
    border-left: 4px solid var(--accent-vermilion);
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.02em;
    background: var(--bg-surface);
  }

  @media (max-width: 1024px) {
    .maximal-layout.panel-open .content-core {
      max-width: 100%;
      padding-right: 4vw;
    }

    .detail-sidebar {
      width: 100%;
      border-left: none;
      border-top: var(--border-thick);
    }
  }

  @media (max-width: 640px) {
    .content-core {
      padding: 0 1rem 1.5rem 1rem;
    }

    .maximal-layout.panel-open .content-core {
      padding-right: 1rem;
    }
  }
</style>
