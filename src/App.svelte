<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly, slide } from 'svelte/transition';
  import { expoOut, cubicInOut } from 'svelte/easing';
  import { tweened } from 'svelte/motion';
  import realData from './lib/real_data.json';

  // State using runes (Svelte 5)
  let isLoaded = $state(false);
  let searchQuery = $state('');
  let activeFilter = $state<string | null>(null);
  let hoveredId = $state<string | null>(null);

  // Derived state for filtering
  let filteredVulns = $derived(
    realData.vulnerabilities.filter(v => {
      const matchSearch = v.id.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          v.pkg.toLowerCase().includes(searchQuery.toLowerCase());
      
      let matchSeverity = true;
      if (activeFilter === 'priority') matchSeverity = v.score >= 0.8;
      else if (activeFilter === 'ignored') matchSeverity = v.cvss >= 8.0 && v.score < 0.6; // High CVSS but low composite
      
      return matchSearch && matchSeverity;
    })
  );

  // Animated metric counters
  const totalCounter = tweened(0, { duration: 1200, easing: expoOut });
  const criticalCounter = tweened(0, { duration: 1600, easing: expoOut });
  const reducedCounter = tweened(0, { duration: 2000, easing: cubicInOut });

  onMount(() => {
    isLoaded = true;
    totalCounter.set(realData.metrics.total);
    criticalCounter.set(realData.metrics.critical);
    
    // Simulate complex loading logic for the alert reduction stat
    setTimeout(() => reducedCounter.set(realData.metrics.alertReduction), 800);
  });

  function getSeveritySoftColor(score: number) {
    if (score >= 0.8) return 'var(--color-critical-bg)';
    if (score >= 0.6) return 'var(--color-high-bg)';
    return 'var(--color-low-bg)';
  }

  function getSeverityBorder(score: number) {
    if (score >= 0.8) return 'var(--color-critical-border)';
    if (score >= 0.6) return 'var(--color-high-border)';
    return 'var(--color-low-border)';
  }

  function formatPct(val: number) {
    return Math.round(val * 100) + '%';
  }
</script>

<svelte:head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');

    :root {
      /* Refined Ultra-Light Editorial Theme */
      --bg-canvas: #f7f6f2; /* Soft ivory/newsprint background */
      --bg-surface: #ffffff;
      
      --text-main: #1a1a1a;
      --text-soft: #666461;
      --text-accent: #b05c33; /* Terracotta serif accent */
      
      --border-light: rgba(0, 0, 0, 0.08);
      --border-dark: rgba(0, 0, 0, 0.9);
      
      /* Subtle Pastel Severity Colors */
      --color-critical-bg: #faebeb;
      --color-critical-border: #e6b3b3;
      --color-high-bg: #fff5e6;
      --color-high-border: #ffd1b3;
      --color-low-bg: #eef6f0;
      --color-low-border: #bae0c7;

      --font-serif: 'Cormorant Garamond', serif;
      --font-sans: 'Outfit', sans-serif;
    }

    body {
      background-color: var(--bg-canvas);
      color: var(--text-main);
      margin: 0;
      padding: 0;
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
    }
  </style>
</svelte:head>

<main class="editorial-container">
  {#if isLoaded}
    <div class="inner-wrapper">
      
      <!-- Masthead -->
      <header class="masthead" in:fly={{ y: 20, duration: 1000, easing: expoOut }}>
        <p class="eyebrow">EPSS AUGMENTED VULNERABILITY REPORT</p>
        <h1 class="serif-title">Intelligence <br/><i>&</i> Prioritization</h1>
        <div class="meta-data">
          <div>
            <span class="meta-label">TARGET ASSET</span>
            <span class="meta-value">{realData.image}</span>
          </div>
          <div>
            <span class="meta-label">ANALYSIS DATE</span>
            <span class="meta-value">{new Date(realData.scannedAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric'})}</span>
          </div>
        </div>
      </header>
      
      <!-- Stat Strip -->
      <section class="stat-strip">
        <div class="stat-box" in:fade={{ delay: 200, duration: 800 }}>
          <div class="stat-number">{Math.floor($totalCounter)}</div>
          <div class="stat-caption">Total Exploit Vectors Found</div>
        </div>
        <div class="stat-box" in:fade={{ delay: 400, duration: 800 }}>
          <div class="stat-number active-hightlight">{Math.floor($criticalCounter)}</div>
          <div class="stat-caption">Requires Immediate Intervention</div>
        </div>
        <div class="stat-box" in:fade={{ delay: 600, duration: 800 }}>
          <div class="stat-number serif-accent">{Math.floor($reducedCounter)}%</div>
          <div class="stat-caption">Reduction in Alert Fatigue via EPSS Context</div>
        </div>
      </section>

      <!-- Controls -->
      <div class="control-panel" in:fly={{ y: 10, delay: 800, duration: 600, easing: expoOut }}>
        <input 
          type="text" 
          bind:value={searchQuery} 
          placeholder="Filter by CVE or Package..." 
          class="elegant-input"
        />
        <div class="pill-group">
          <button class:active={activeFilter === null} onclick={() => activeFilter = null}>Overview</button>
          <button class:active={activeFilter === 'priority'} onclick={() => activeFilter = 'priority'}>High Priority</button>
          <button class:active={activeFilter === 'ignored'} onclick={() => activeFilter = 'ignored'}>De-prioritized</button>
        </div>
      </div>

      <!-- Vulnerability Catalog -->
      <section class="catalog" in:fade={{ delay: 1000, duration: 800 }}>
        {#each filteredVulns as vuln, index (vuln.id)}
          <article 
            class="vuln-card"
            class:hovered={hoveredId === vuln.id}
            onmouseenter={() => hoveredId = vuln.id}
            onmouseleave={() => hoveredId = null}
            in:fly={{ y: 20, delay: 1000 + (index * 50), duration: 600, easing: expoOut }}
          >
            <!-- Severity Swatch -->
            <div class="severity-swatch" style="background: {getSeveritySoftColor(vuln.score)}; border-right: 1px solid {getSeverityBorder(vuln.score)}">
              <span class="score-main">{formatPct(vuln.score)}</span>
              <span class="score-label">COMPOSITE</span>
            </div>
            
            <!-- Details -->
            <div class="vuln-details">
              <div class="vuln-header">
                <h2 class="cve-title">{vuln.id}</h2>
                <span class="pkg-name">{vuln.pkg}</span>
              </div>
              
              <div class="metrics-row">
                <div class="metric-mini">
                  <span class="lbl">CVSS v3</span>
                  <span class="val">{vuln.cvss.toFixed(1)}</span>
                </div>
                <div class="metric-mini">
                  <span class="lbl">EPSS Likelihood</span>
                  <span class="val">{formatPct(vuln.epss)}</span>
                </div>
                <div class="metric-mini">
                  <span class="lbl">Reachability</span>
                  <span class="val">{formatPct(vuln.reachability)}</span>
                </div>
              </div>
            </div>

            <!-- Resolution -->
            <div class="resolution-col">
              {#if vuln.fix}
                <div class="fix-badge available">
                  <span>Fix Exists</span>
                  <strong>{vuln.fix}</strong>
                </div>
              {:else}
                <div class="fix-badge unvailable">
                  <span>No Fix Known</span>
                </div>
              {/if}
              
              {#if vuln.cvss >= 8.0 && vuln.score < 0.6}
                <div class="insight-pill">De-prioritized by EPSS</div>
              {/if}
            </div>
          </article>
        {:else}
          <div class="empty-state" in:fade>
            <p>No vulnerabilities match the current editorial filters.</p>
          </div>
        {/each}
      </section>
      
    </div>
  {/if}
</main>

<style>
  /* Editorial Layout */
  .editorial-container {
    padding: 4vw 6vw;
    min-height: 100vh;
  }

  .inner-wrapper {
    max-width: 1100px;
    margin: 0 auto;
  }

  /* Typography & Header */
  .masthead {
    border-bottom: 2px solid var(--text-main);
    padding-bottom: 3rem;
    margin-bottom: 4rem;
  }

  .eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-soft);
    margin-bottom: 1rem;
    font-weight: 500;
  }

  .serif-title {
    font-family: var(--font-serif);
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 400;
    line-height: 1.05;
    margin: 0 0 2rem 0;
    letter-spacing: -0.02em;
  }
  
  .serif-title i {
    font-style: italic;
    color: var(--text-accent);
  }

  .meta-data {
    display: flex;
    gap: 4rem;
  }

  .meta-label {
    display: block;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: var(--text-soft);
    margin-bottom: 0.2rem;
  }

  .meta-value {
    font-size: 1.1rem;
    font-weight: 500;
  }

  /* Stats Section */
  .stat-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-bottom: 4rem;
  }

  .stat-box {
    border-top: 1px solid var(--border-light);
    padding-top: 1.5rem;
  }

  .stat-number {
    font-size: 3.5rem;
    font-weight: 300;
    line-height: 1;
    margin-bottom: 0.5rem;
    letter-spacing: -0.03em;
  }

  .active-hightlight {
    font-weight: 500;
    color: var(--text-main);
  }

  .serif-accent {
    font-family: var(--font-serif);
    color: var(--text-accent);
    font-style: italic;
  }

  .stat-caption {
    font-size: 0.85rem;
    color: var(--text-soft);
    font-weight: 400;
  }

  /* Controls */
  .control-panel {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-light);
  }

  .elegant-input {
    background: transparent;
    border: none;
    border-bottom: 1px dashed var(--text-soft);
    padding: 0.5rem 0;
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-style: italic;
    color: var(--text-main);
    width: 350px;
    outline: none;
    transition: border-color 0.3s ease;
  }

  .elegant-input:focus {
    border-bottom-color: var(--text-main);
    border-bottom-style: solid;
  }

  .elegant-input::placeholder {
    color: #b3b3b3;
  }

  .pill-group {
    display: flex;
    gap: 1rem;
  }

  .pill-group button {
    background: transparent;
    border: none;
    padding: 0.25rem 0;
    font-size: 0.85rem;
    color: var(--text-soft);
    cursor: pointer;
    position: relative;
    font-weight: 500;
  }

  .pill-group button::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 1px;
    background: var(--text-main);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s cubic-bezier(0.19, 1, 0.22, 1);
  }

  .pill-group button:hover::after,
  .pill-group button.active::after {
    transform: scaleX(1);
    transform-origin: left;
  }

  .pill-group button.active {
    color: var(--text-main);
  }

  /* Catalog List */
  .catalog {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding-bottom: 4rem;
  }

  .vuln-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: 8px; /* Slight organic roundness */
    display: flex;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  }

  .vuln-card.hovered {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    border-color: rgba(0,0,0,0.15);
  }

  .severity-swatch {
    width: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    flex-shrink: 0;
  }

  .score-main {
    font-family: var(--font-serif);
    font-size: 2.5rem;
    line-height: 1;
    margin-bottom: 0.25rem;
  }

  .score-label {
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    font-weight: 600;
    color: rgba(0,0,0,0.4);
  }

  .vuln-details {
    padding: 2rem;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .vuln-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .cve-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
  }

  .pkg-name {
    font-size: 0.85rem;
    color: var(--text-soft);
    background: var(--bg-canvas);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
  }

  .metrics-row {
    display: flex;
    gap: 3rem;
  }

  .metric-mini {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .metric-mini .lbl {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-soft);
  }

  .metric-mini .val {
    font-family: var(--font-serif);
    font-size: 1.2rem;
    font-style: italic;
  }

  .resolution-col {
    padding: 2rem;
    width: 200px;
    border-left: 1px dashed var(--border-light);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
    background: #fafaf9;
  }

  .fix-badge {
    display: flex;
    flex-direction: column;
    font-size: 0.8rem;
  }

  .fix-badge.available span { color: #5c8567; }
  .fix-badge.unvailable span { color: #b36666; }
  
  .fix-badge strong {
    font-weight: 600;
    margin-top: 0.25rem;
  }

  .insight-pill {
    font-size: 0.65rem;
    border: 1px solid var(--color-high-border);
    color: var(--text-accent);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    text-align: center;
    background: #fff;
  }

  .empty-state {
    text-align: center;
    padding: 6rem 0;
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-style: italic;
    color: var(--text-soft);
  }
</style>
