<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { expoOut } from 'svelte/easing';
  
  import Masthead from '$lib/components/Masthead.svelte';
  import StatStrip from '$lib/components/StatStrip.svelte';
  import ControlPanel from '$lib/components/ControlPanel.svelte';
  import VulnerabilityGrid from '$lib/components/VulnerabilityGrid.svelte';
  import VulnDetailPanel from '$lib/components/VulnDetailPanel.svelte';
  import TickerTape from '$lib/components/TickerTape.svelte';
  
  import realData from '$lib/real_data.json';

  // State using Svelte 5 runes
  let isLoaded = $state(false);
  let searchQuery = $state('');
  let activeFilter = $state<string | null>(null);
  let sortKey = $state<'score' | 'cvss' | 'epss' | 'pkg'>('score');
  let sortDesc = $state(true);
  
  let selectedVulnId = $state<string | null>(null);
  let selectedVuln = $derived(
    selectedVulnId ? realData.vulnerabilities.find(v => v.id === selectedVulnId) : null
  );

  onMount(() => {
    isLoaded = true;
  });

  // Complex filtering & sorting functionality
  let processedVulns = $derived(() => {
    // 1. Filter
    let filtered = realData.vulnerabilities.filter(v => {
      const matchSearch = v.id.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          v.pkg.toLowerCase().includes(searchQuery.toLowerCase());
      
      let matchSeverity = true;
      if (activeFilter === 'priority') matchSeverity = v.score >= 0.8;
      else if (activeFilter === 'ignored') matchSeverity = v.cvss >= 8.0 && v.score < 0.6;
      else if (activeFilter === 'fixable') matchSeverity = v.fix !== null;
      
      return matchSearch && matchSeverity;
    });

    // 2. Sort
    filtered.sort((a, b) => {
      let valA = a[sortKey];
      let valB = b[sortKey];
      
      if (typeof valA === 'string' && typeof valB === 'string') {
        return sortDesc ? valB.localeCompare(valA) : valA.localeCompare(valB);
      }
      return sortDesc ? (valB as number) - (valA as number) : (valA as number) - (valB as number);
    });

    return filtered;
  });

</script>

<svelte:head>
  <style>
    /* Maximalist Editorial Typography */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600&display=swap');

    :root {
      /* High-contrast Paper & Ink Palette */
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

    body {
      background-color: var(--bg-paper);
      color: var(--ink-main);
      margin: 0;
      padding: 0;
      font-family: var(--font-ui);
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
  </style>
</svelte:head>

<TickerTape />

{#if isLoaded}
  <main class="maximal-layout" class:panel-open={selectedVulnId !== null}>
    
    <div class="content-core">
      <Masthead targetImage={realData.image} scanDate={realData.scannedAt} />
      
      <StatStrip 
        total={realData.metrics.total}
        critical={realData.metrics.critical}
        reduction={realData.metrics.alertReduction}
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

    <!-- Slide-over Detailed Analysis Panel -->
    {#if selectedVuln}
      <aside class="detail-sidebar" transition:fly={{ x: 400, duration: 600, easing: expoOut }}>
        <VulnDetailPanel 
          vuln={selectedVuln} 
          onClose={() => selectedVulnId = null} 
        />
      </aside>
    {/if}

  </main>
{/if}

<style>
  .maximal-layout {
    display: flex;
    min-height: 100vh;
    transition: padding-right 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .content-core {
    flex-grow: 1;
    padding: 0 4vw 4vw 4vw;
    display: flex;
    flex-direction: column;
    max-width: 100%;
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
    width: 450px;
    height: 100vh;
    background: var(--bg-surface);
    border-left: var(--border-thick);
    z-index: 100;
    overflow-y: auto;
    box-shadow: -20px 0 40px rgba(0,0,0,0.05);
  }

  @media (max-width: 1024px) {
    .maximal-layout.panel-open .content-core {
      max-width: 100%;
    }
    .detail-sidebar {
      width: 100%;
      border-left: none;
      border-top: var(--border-thick);
    }
  }
</style>
