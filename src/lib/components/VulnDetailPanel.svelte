<script lang="ts">
  import { fade } from 'svelte/transition';

  export let vuln: any;
  export let onClose: () => void;

  let activeTab = 'radar';

  // Compute SVG radar positions manually for a fun maximalist graph
  // Points: CVSS, EPSS, Reachability
  function getScorePath() {
    // Basic math mapping [0..1] metrics onto a triangle SVG
    const cx = 150, cy = 150, r = 100;
    
    // Convert CVSS to 0-1
    const p1 = vuln.cvss / 10.0;
    const p2 = vuln.epss;
    const p3 = vuln.reachability;

    const x1 = cx;
    const y1 = cy - (r * p1);

    const x2 = cx + (r * p2 * Math.cos(Math.PI / 6));
    const y2 = cy + (r * p2 * Math.sin(Math.PI / 6));

    const x3 = cx - (r * p3 * Math.cos(Math.PI / 6));
    const y3 = cy + (r * p3 * Math.sin(Math.PI / 6));

    return `${x1},${y1} ${x2},${y2} ${x3},${y3}`;
  }

  function handleCopy() {
    const payload = JSON.stringify(vuln, null, 2);
    // Real implementation would use navigator.clipboard
    console.log("Copied to clipboard:", payload);
    alert('JSON PAYLOAD COPIED TO CLIPBOARD');
  }
</script>

<div class="panel-header">
  <div class="h-top">
    <h2>CVE_INSPECT</h2>
    <button class="close-btn" onclick={onClose}>[X]</button>
  </div>
  <div class="h-bot">
    <div class="mega-id">{vuln.id}</div>
    <div class="pkg-box">PKG_TARGET // <span>{vuln.pkg}</span></div>
  </div>
</div>

<div class="tabs">
  <button class:active={activeTab === 'radar'} onclick={() => activeTab = 'radar'}>RADAR_CHART</button>
  <button class:active={activeTab === 'json'} onclick={() => activeTab = 'json'}>RAW_JSON</button>
  <button class:active={activeTab === 'yaml'} onclick={() => activeTab = 'yaml'}>K8S_POLICY</button>
</div>

<div class="panel-content">
  {#if activeTab === 'radar'}
    <div class="chart-view" in:fade>
      <!-- Pure SVG Data Viz -->
      <div class="svg-container">
        <svg viewBox="0 0 300 300" width="100%" height="100%">
          <!-- Base Grid -->
          <polygon points="150,50 236.6,200 63.4,200" fill="none" stroke="var(--ink-faint)" stroke-width="1"/>
          <polygon points="150,100 193.3,175 106.7,175" fill="none" stroke="var(--ink-faint)" stroke-width="1"/>
          <line x1="150" y1="150" x2="150" y2="50" stroke="var(--ink-faint)" />
          <line x1="150" y1="150" x2="236.6" y2="200" stroke="var(--ink-faint)" />
          <line x1="150" y1="150" x2="63.4" y2="200" stroke="var(--ink-faint)" />
          
          <!-- Data Shape -->
          <polygon points={getScorePath()} fill="var(--accent-vermilion)" fill-opacity="0.2" stroke="var(--accent-vermilion)" stroke-width="3"/>
          
          <!-- Labels -->
          <text x="150" y="35" text-anchor="middle" class="svg-lbl">CVSS</text>
          <text x="250" y="210" text-anchor="start" class="svg-lbl">EPSS</text>
          <text x="50" y="210" text-anchor="end" class="svg-lbl">REACH</text>
        </svg>
      </div>

      <div class="data-breakdown">
        <div class="d-row">
          <span class="d-lbl">COMPOSITE SCORE</span>
          <span class="d-val focus">{(vuln.score * 100).toFixed(2)}%</span>
        </div>
        <div class="d-row">
          <span class="d-lbl">CVSS INTENSITY</span>
          <span class="d-val">{vuln.cvss.toFixed(1)} / 10.0</span>
        </div>
        <div class="d-row">
          <span class="d-lbl">EXPLOIT PROBABILITY</span>
          <span class="d-val">{(vuln.epss * 100).toFixed(4)}%</span>
        </div>
        <div class="d-row">
          <span class="d-lbl">RUNTIME REACHABILITY</span>
          <span class="d-val">{(vuln.reachability * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  {:else if activeTab === 'json'}
    <div class="code-view" in:fade>
      <button class="action-float" onclick={handleCopy}>COPY</button>
      <pre><code>{JSON.stringify(vuln, null, 2)}</code></pre>
    </div>
  {:else if activeTab === 'yaml'}
    <div class="code-view" in:fade>
      <pre><code>apiVersion: epss.triage.dev/v1
kind: PolicyExemption
metadata:
  name: {vuln.id.toLowerCase()}-exemption
spec:
  identifier: "{vuln.id}"
  reason: "EPSS Likelihood {(vuln.epss*100).toFixed(1)}%"
  expires_at: "2026-12-31"</code></pre>
    </div>
  {/if}

  <div class="action-strip">
    <div class="resolution" class:warn={!vuln.fix}>
      <div><strong>RESOLUTION_TARGET:</strong></div>
      <div class="fix-val">{vuln.fix || 'NO SYSTEM FIX AVAILABLE. APPLY WAF RULE.'}</div>
    </div>
  </div>
</div>

<style>
  .panel-header {
    padding: 2rem;
    background: var(--ink-main);
    color: var(--bg-paper);
    border-bottom: var(--border-thick);
  }

  .h-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
  }

  .h-top h2 { margin: 0; font-family: var(--font-mono); font-size: 0.8rem; letter-spacing: 0.2em; }
  
  .close-btn { 
    background: transparent; 
    border: none; 
    color: var(--accent-vermilion); 
    font-size: 1.2rem; 
    font-weight: 800; 
    cursor: pointer;
    font-family: var(--font-mono);
  }

  .mega-id {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 4.5vw, 3rem);
    font-weight: 800;
    line-height: 1;
    margin-bottom: 1rem;
    color: var(--accent-chartreuse);
    overflow-wrap: anywhere;
    word-break: break-word;
  }

  .pkg-box {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: #888;
  }
  
  .pkg-box span { color: var(--bg-paper); }

  .tabs {
    display: flex;
    border-bottom: var(--border-thin);
  }

  .tabs button {
    flex: 1;
    padding: 1rem;
    background: var(--bg-surface);
    border: none;
    border-right: var(--border-thin);
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 0.8rem;
    cursor: pointer;
    min-width: 0;
    overflow-wrap: anywhere;
  }

  .tabs button:last-child { border-right: none; }
  
  .tabs button.active {
    background: var(--accent-chartreuse);
    color: var(--ink-main);
  }

  .panel-content {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    min-height: 500px;
    min-width: 0;
  }

  .svg-container {
    width: 100%;
    max-width: 300px;
    margin: 0 auto 3rem auto;
  }

  .svg-lbl {
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 700;
    fill: var(--ink-main);
  }

  .d-row {
    display: flex;
    justify-content: space-between;
    gap: 0.8rem;
    flex-wrap: wrap;
    border-bottom: 1px dotted var(--ink-faint);
    padding: 1rem 0;
    font-family: var(--font-mono);
  }

  .d-lbl { font-size: 0.8rem; font-weight: 600; }
  .d-val { font-size: 1.25rem; font-weight: 800; }
  .d-val.focus { color: var(--accent-vermilion); font-size: 1.75rem; }

  .code-view {
    position: relative;
    background: var(--ink-main);
    color: var(--accent-chartreuse);
    padding: 2rem;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    overflow-x: auto;
    height: 400px;
  }

  .code-view pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .action-float {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--accent-chartreuse);
    color: var(--ink-main);
    border: none;
    padding: 0.25rem 0.75rem;
    font-family: var(--font-mono);
    font-weight: 700;
    cursor: pointer;
  }

  .action-strip {
    margin-top: auto;
    padding-top: 3rem;
  }

  .resolution {
    background: var(--bg-paper);
    padding: 1.5rem;
    border: 2px dashed var(--ink-main);
    font-family: var(--font-mono);
  }

  .warn { border-color: var(--accent-vermilion); color: var(--accent-vermilion); }
  
  .fix-val {
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 0.5rem;
    overflow-wrap: anywhere;
    word-break: break-word;
  }

  @media (max-width: 640px) {
    .panel-header {
      padding: 1rem;
    }

    .panel-content {
      padding: 1rem;
      min-height: auto;
    }

    .tabs button {
      font-size: 0.7rem;
      padding: 0.7rem 0.3rem;
    }

    .d-val {
      font-size: 1rem;
    }

    .d-val.focus {
      font-size: 1.2rem;
    }

    .code-view {
      font-size: 0.75rem;
      height: 320px;
      padding: 1rem;
    }

    .fix-val {
      font-size: 1.1rem;
    }
  }
</style>
