<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { cubicOut, backOut, expoInOut } from 'svelte/easing';
  import { tweened } from 'svelte/motion';

  // State using runes (Svelte 5)
  let isLoaded = $state(false);
  let hoveredVuln = $state<string | null>(null);
  let searchQuery = $state('');
  let selectedSeverity = $state<string | null>(null);

  // Mock data representing the enriched backend output
  const scanData = {
    image: 'nginx:1.25.3',
    scannedAt: '2026-03-25T15:45:00Z',
    metrics: {
      total: 142,
      critical: 3,
      high: 12,
      alertReduction: 74, // reduced by 74% using EPSS
    },
    vulnerabilities: [
      { id: 'CVE-2024-3312', score: 0.94, cvss: 9.8, epss: 0.88, reachability: 1.0, pkg: 'libssl3', fix: '3.0.13-1' },
      { id: 'CVE-2023-4408', score: 0.82, cvss: 8.5, epss: 0.76, reachability: 1.0, pkg: 'curl', fix: '8.5.0-dfsg-1' },
      { id: 'CVE-2024-1189', score: 0.76, cvss: 7.2, epss: 0.65, reachability: 0.8, pkg: 'zlib1g', fix: '1:1.3.dfsg-3' },
      { id: 'CVE-2023-5591', score: 0.45, cvss: 9.1, epss: 0.05, reachability: 0.0, pkg: 'bash', fix: null }, // Downranked!
      { id: 'CVE-2024-2201', score: 0.38, cvss: 6.5, epss: 0.12, reachability: 0.2, pkg: 'openssh-client', fix: '1:9.6p1-3' },
      { id: 'CVE-2024-1944', score: 0.21, cvss: 5.3, epss: 0.01, reachability: 0.0, pkg: 'systemd', fix: '255.3-1' },
    ]
  };

  // Derived state
  let filteredVulns = $derived(
    scanData.vulnerabilities.filter(v => {
      const matchSearch = v.id.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          v.pkg.toLowerCase().includes(searchQuery.toLowerCase());
      
      let matchSeverity = true;
      if (selectedSeverity === 'critical') matchSeverity = v.score >= 0.8;
      else if (selectedSeverity === 'high') matchSeverity = v.score >= 0.6 && v.score < 0.8;
      else if (selectedSeverity === 'downranked') matchSeverity = v.cvss >= 7.0 && v.score < 0.6;
      
      return matchSearch && matchSeverity;
    })
  );

  // Animated counters
  const countTotal = tweened(0, { duration: 1500, easing: cubicOut });
  const countCritical = tweened(0, { duration: 1800, easing: backOut });
  const countReduction = tweened(0, { duration: 2000, easing: expoInOut });

  onMount(() => {
    isLoaded = true;
    countTotal.set(scanData.metrics.total);
    countCritical.set(scanData.metrics.critical);
    countReduction.set(scanData.metrics.alertReduction);
  });

  function getSeverityColor(score: number) {
    if (score >= 0.8) return 'var(--c-crimson)';
    if (score >= 0.6) return 'var(--c-amber)';
    if (score >= 0.4) return 'var(--c-sun)';
    return 'var(--c-pine)';
  }

  function formatPercent(val: number) {
    return Math.round(val) + '%';
  }
</script>

<svelte:head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
      /* Cyber-Industrial Palette */
      --bg-void: #050505;
      --bg-panel: #0a0a0c;
      --bg-surface: #121216;
      --border-dim: #1d1d24;
      --border-lit: #3a3a46;
      
      --c-text-primary: #e6e6f0;
      --c-text-muted: #84849a;
      
      --c-crimson: #ff2a4d;
      --c-crimson-dim: rgba(255, 42, 77, 0.15);
      
      --c-amber: #ff8c00;
      --c-amber-dim: rgba(255, 140, 0, 0.15);
      
      --c-sun: #ffd700;
      --c-pine: #00e676;
      
      --c-neon-blue: #00f0ff;
      --c-neon-blue-dim: rgba(0, 240, 255, 0.1);

      --font-display: 'Bricolage Grotesque', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    body {
      background-color: var(--bg-void);
      color: var(--c-text-primary);
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
      background-image: 
        radial-gradient(circle at 15% 50%, rgba(255, 42, 77, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.04) 0%, transparent 50%);
      background-attachment: fixed;
    }
  </style>
</svelte:head>

<main class="dashboard {isLoaded ? 'loaded' : ''}">
  {#if isLoaded}
    <header class="header" in:fly={{ y: -40, duration: 800, easing: cubicOut }}>
      <div class="logo-area">
        <div class="sigil"></div>
        <h1>EPSS TRIAGE</h1>
      </div>
      <div class="meta-strip">
        <span class="mono">TGT: {scanData.image}</span>
        <span class="mono">SYS: ONLINE</span>
        <span class="mono">LAST SCAN: {new Date(scanData.scannedAt).toLocaleTimeString()}</span>
      </div>
    </header>

    <div class="grid">
      <!-- LEITMOTIF METRICS -->
      <section class="metrics">
        <div class="metric-card" in:fly={{ y: 20, duration: 600, delay: 100 }}>
          <div class="metric-label">TOTAL VULNERABILITIES</div>
          <div class="metric-value">{Math.floor($countTotal)}</div>
          <div class="metric-graph subtle"></div>
        </div>

        <div class="metric-card critical" in:fly={{ y: 20, duration: 600, delay: 200 }}>
          <div class="metric-label">ACTIONABLE CRITICALS</div>
          <div class="metric-value" style="color: var(--c-crimson)">
            {Math.floor($countCritical)}
          </div>
          <div class="metric-desc">CVSS + EPSS ≥ 0.8</div>
        </div>

        <div class="metric-card reduction" in:fly={{ y: 20, duration: 600, delay: 300 }}>
          <div class="metric-label">ALERT FATIGUE REDUCTION</div>
          <div class="metric-value" style="color: var(--c-neon-blue)">
            {formatPercent($countReduction)}
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width: {$countReduction}%"></div>
          </div>
        </div>
      </section>

      <!-- CONTROL PANEL -->
      <section class="controls" in:fly={{ y: 20, duration: 600, delay: 400 }}>
        <input 
          type="text" 
          bind:value={searchQuery} 
          placeholder="// Search CVE or Package..." 
          class="search-input"
        />
        
        <div class="filters">
          <button class:active={selectedSeverity === null} onclick={() => selectedSeverity = null}>ALL</button>
          <button class:active={selectedSeverity === 'critical'} onclick={() => selectedSeverity = 'critical'}>CRITICAL</button>
          <button class:active={selectedSeverity === 'high'} onclick={() => selectedSeverity = 'high'}>HIGH</button>
          <button class:active={selectedSeverity === 'downranked'} onclick={() => selectedSeverity = 'downranked'}>DOWNRANKED</button>
        </div>
      </section>

      <!-- DATA DATA TABLE -->
      <section class="data-view" in:fly={{ y: 20, duration: 600, delay: 500 }}>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>VULN ID</th>
                <th>COMPOSITE</th>
                <th>CVSS</th>
                <th>EPSS</th>
                <th>REACH</th>
                <th>PACKAGE</th>
                <th>FIX</th>
              </tr>
            </thead>
            <tbody>
              {#each filteredVulns as vuln (vuln.id)}
                {@const isDownranked = vuln.cvss >= 7.0 && vuln.score < 0.6}
                <tr 
                  in:scale={{ start: 0.98, duration: 300, easing: cubicOut }}
                  class="vuln-row"
                  class:hovered={hoveredVuln === vuln.id}
                  class:downranked={isDownranked}
                  onmouseenter={() => hoveredVuln = vuln.id}
                  onmouseleave={() => hoveredVuln = null}
                >
                  <td class="id-col">
                    <span class="cve-id">{vuln.id}</span>
                    {#if isDownranked}
                      <span class="badge ghost">DEPRIOTIZED</span>
                    {/if}
                  </td>
                  <td>
                    <div class="score-pill" style="--pill-color: {getSeverityColor(vuln.score)}; background: {getSeverityColor(vuln.score)}22; border-color: {getSeverityColor(vuln.score)}">
                      {(vuln.score * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td class="mono dim">{vuln.cvss.toFixed(1)}</td>
                  <td class="mono dim">{(vuln.epss * 100).toFixed(1)}%</td>
                  <td>
                    <div class="reach-indicator" style="opacity: {Math.max(0.3, vuln.reachability)}">
                      {#if vuln.reachability === 1.0} DIRECT
                      {:else if vuln.reachability > 0} TRANSITIVE
                      {:else} NONE {/if}
                    </div>
                  </td>
                  <td class="pkg-col">{vuln.pkg}</td>
                  <td class="mono {vuln.fix ? 'fix-avail' : 'fix-none'}">
                    {vuln.fix || 'NO FIX'}
                  </td>
                </tr>
              {/each}
              
              {#if filteredVulns.length === 0}
                <tr in:fade>
                  <td colspan="7" class="empty-state">NO MATCHING DATA FOUND IN MATRIX</td>
                </tr>
              {/if}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  {/if}
</main>

<style>
  /* Base structural styling */
  main {
    min-height: 100vh;
    padding: 2rem;
    font-family: var(--font-display);
    box-sizing: border-box;
  }

  .grid {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  /* Header - Brutalist & Technical */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid var(--border-lit);
    max-width: 1400px;
    margin: 0 auto 2rem;
  }

  .logo-area {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .sigil {
    width: 24px;
    height: 24px;
    background: var(--c-neon-blue);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    animation: pulse-glow 4s infinite alternate;
  }

  @keyframes pulse-glow {
    0% { box-shadow: 0 0 10px var(--c-neon-blue); filter: drop-shadow(0 0 5px var(--c-neon-blue)); }
    100% { box-shadow: 0 0 20px var(--c-neon-blue); filter: drop-shadow(0 0 15px var(--c-neon-blue)); }
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
    line-height: 1;
    letter-spacing: -0.04em;
    background: linear-gradient(180deg, #fff, #888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .meta-strip {
    display: flex;
    gap: 2rem;
    font-size: 0.8rem;
    color: var(--c-text-muted);
  }

  .mono {
    font-family: var(--font-mono);
    letter-spacing: 0.05em;
  }

  /* Metrics Cards - Spatial composition & grid-breaking */
  .metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .metric-card {
    background: var(--bg-panel);
    border: 1px solid var(--border-dim);
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
  }

  .metric-card:hover {
    border-color: var(--border-lit);
  }

  .metric-label {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--c-text-muted);
    margin-bottom: 1rem;
  }

  .metric-value {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    font-feature-settings: "tnum";
    letter-spacing: -0.02em;
  }

  .metric-desc {
    margin-top: 1rem;
    font-size: 0.85rem;
    font-family: var(--font-mono);
    color: var(--c-text-muted);
  }

  /* Specific card details */
  .metric-card.critical {
    border-top: 3px solid var(--c-crimson);
  }

  .metric-card.reduction {
    border-top: 3px solid var(--c-neon-blue);
    background: linear-gradient(180deg, var(--c-neon-blue-dim) 0%, transparent 100%);
  }

  .progress-track {
    height: 4px;
    background: var(--border-lit);
    margin-top: 1.5rem;
    width: 100%;
  }

  .progress-fill {
    height: 100%;
    background: var(--c-neon-blue);
    position: relative;
  }
  
  .progress-fill::after {
    content: '';
    position: absolute;
    right: 0;
    top: -3px;
    width: 2px;
    height: 10px;
    background: #fff;
  }

  /* Controls Section */
  .controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-panel);
    border: 1px solid var(--border-dim);
    padding: 1rem;
  }

  .search-input {
    background: transparent;
    border: none;
    color: var(--c-text-primary);
    font-family: var(--font-mono);
    font-size: 1rem;
    width: 300px;
    outline: none;
  }

  .search-input::placeholder {
    color: var(--border-lit);
  }

  .filters {
    display: flex;
    gap: 0.5rem;
  }

  .filters button {
    background: transparent;
    border: 1px solid var(--border-dim);
    color: var(--c-text-muted);
    padding: 0.5rem 1rem;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .filters button:hover {
    border-color: var(--c-text-muted);
    color: var(--c-text-primary);
  }

  .filters button.active {
    background: var(--c-text-primary);
    color: var(--bg-void);
    border-color: var(--c-text-primary);
    font-weight: bold;
  }

  /* Data Table - Industrial aesthetic */
  .data-view {
    background: var(--bg-panel);
    border: 1px solid var(--border-dim);
    overflow: hidden;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }

  th {
    padding: 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--c-text-muted);
    border-bottom: 1px solid var(--border-dim);
    background: var(--bg-surface);
  }

  td {
    padding: 1rem;
    border-bottom: 1px solid var(--border-dim);
    font-size: 0.95rem;
  }

  .vuln-row {
    transition: background-color 0.2s ease;
  }

  .vuln-row:hover {
    background: var(--bg-surface);
  }

  .vuln-row.downranked {
    opacity: 0.6;
  }
  
  .vuln-row.downranked:hover {
    opacity: 1;
  }

  .cve-id {
    font-weight: 600;
    font-family: var(--font-mono);
  }

  .badge {
    font-size: 0.65rem;
    padding: 0.2rem 0.4rem;
    border-radius: 2px;
    margin-left: 0.5rem;
    font-weight: bold;
    letter-spacing: 0.05em;
  }

  .badge.ghost {
    background: transparent;
    border: 1px solid var(--c-text-muted);
    color: var(--c-text-muted);
  }

  .score-pill {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border: 1px solid;
    font-family: var(--font-mono);
    font-weight: bold;
    font-size: 0.85rem;
    box-shadow: 0 0 10px rgba(0,0,0,0.5) inset;
    text-shadow: 0 0 8px var(--pill-color);
  }

  .dim {
    color: var(--c-text-muted);
  }

  .reach-indicator {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.05em;
  }

  .pkg-col {
    font-weight: 600;
  }

  .fix-avail {
    color: var(--c-pine);
  }

  .fix-none {
    color: var(--c-crimson);
  }

  .empty-state {
    text-align: center;
    padding: 4rem !important;
    font-family: var(--font-mono);
    color: var(--c-text-muted);
    letter-spacing: 0.1em;
  }
</style>
