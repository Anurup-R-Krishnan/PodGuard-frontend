<script lang="ts">
  export let searchQuery: string;
  export let activeFilter: string | null;
  export let sortKey: 'score' | 'cvss' | 'epss' | 'pkg';
  export let sortDesc: boolean;

  function toggleScale(key: typeof sortKey) {
    if (sortKey === key) {
      sortDesc = !sortDesc;
    } else {
      sortKey = key;
      sortDesc = true;
    }
  }

  function triggerExport() {
    alert('FUNCTIONALITY DEMO: Exporting Composite Report to PDF...');
  }
</script>

<div class="control-panel">
  <div class="search-box">
    <span class="search-icon">↘</span>
    <input 
      type="text" 
      bind:value={searchQuery} 
      placeholder="QUERY CVE OR PACKAGE_NAME..." 
    />
  </div>

  <div class="filter-group">
    <span class="lbl">FOCUS:</span>
    <button class:active={activeFilter === null} onclick={() => activeFilter = null}>GLOBAL</button>
    <button class:active={activeFilter === 'priority'} onclick={() => activeFilter = 'priority'}>PRIORITY</button>
    <button class:active={activeFilter === 'ignored'} onclick={() => activeFilter = 'ignored'}>DE-PRIORITIZED</button>
    <button class:active={activeFilter === 'fixable'} onclick={() => activeFilter = 'fixable'}>FIXABLE</button>
  </div>

  <div class="filter-group sort">
    <span class="lbl">INDEX BY:</span>
    <button class="sort-btn" class:active={sortKey === 'score'} onclick={() => toggleScale('score')}>
      COMPOSITE {sortKey === 'score' ? (sortDesc ? '↓' : '↑') : ''}
    </button>
    <button class="sort-btn" class:active={sortKey === 'cvss'} onclick={() => toggleScale('cvss')}>
      CVSS {sortKey === 'cvss' ? (sortDesc ? '↓' : '↑') : ''}
    </button>
    <button class="sort-btn" class:active={sortKey === 'epss'} onclick={() => toggleScale('epss')}>
      EPSS {sortKey === 'epss' ? (sortDesc ? '↓' : '↑') : ''}
    </button>
  </div>

  <div class="actions">
    <button class="export-btn" onclick={triggerExport}>[ EXPORT REPORT.PDF ]</button>
  </div>
</div>

<style>
  .control-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--ink-main);
    color: var(--bg-paper);
    padding: 1rem 2rem;
    margin-bottom: 3rem;
    font-family: var(--font-mono);
    text-transform: uppercase;
  }

  .search-box {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-grow: 1;
    max-width: 400px;
  }

  .search-icon {
    font-size: 1.5rem;
    color: var(--accent-chartreuse);
  }

  .search-box input {
    background: transparent;
    border: none;
    border-bottom: 2px solid var(--ink-faint);
    color: var(--bg-paper);
    font-family: var(--font-mono);
    font-size: 1rem;
    padding: 0.5rem 0;
    width: 100%;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-box input:focus {
    border-color: var(--accent-chartreuse);
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .lbl {
    font-weight: 700;
    color: var(--ink-faint);
    font-size: 0.8rem;
  }

  button {
    background: transparent;
    border: 1px solid transparent;
    color: var(--ink-faint);
    font-family: var(--font-mono);
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.4rem 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  button:hover {
    color: var(--bg-paper);
    border-color: var(--ink-faint);
  }

  button.active {
    background: var(--bg-paper);
    color: var(--ink-main);
    border-color: var(--bg-paper);
  }

  .export-btn {
    border: 1px dashed var(--accent-chartreuse);
    color: var(--accent-chartreuse);
  }

  .export-btn:hover {
    background: var(--accent-chartreuse);
    color: var(--ink-main);
  }

  @media (max-width: 1280px) {
    .control-panel {
      flex-wrap: wrap;
      gap: 1.5rem;
    }
  }
</style>
