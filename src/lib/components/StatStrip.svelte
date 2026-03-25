<script lang="ts">
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { expoOut } from 'svelte/easing';

  export let total: number;
  export let critical: number;
  export let reduction: number;

  const countTotal = tweened(0, { duration: 1200, easing: expoOut });
  const countCritical = tweened(0, { duration: 1600, easing: expoOut });
  const countReduction = tweened(0, { duration: 2000, easing: expoOut });

  onMount(() => {
    countTotal.set(total);
    countCritical.set(critical);
    countReduction.set(reduction);
  });
</script>

<section class="stat-strip">
  <div class="stat-block">
    <div class="stat-header">01 // RAW EXPOSURE</div>
    <div class="stat-value">{Math.floor($countTotal)}</div>
    <div class="stat-desc">Identified static CVEs crossing the dependency tree.</div>
  </div>

  <div class="stat-block highlight">
    <div class="stat-header">02 // ACTIONABLE</div>
    <div class="stat-value">{Math.floor($countCritical)}</div>
    <div class="stat-desc">Critical composite risk requiring immediate patching.</div>
  </div>

  <div class="stat-block">
    <div class="stat-header">03 // EPSS FATIGUE REDUCTION</div>
    <div class="stat-value secondary">{Math.floor($countReduction)}%</div>
    <div class="stat-desc">False-positive noise reduced by EPSS contextual analysis.</div>
  </div>
</section>

<style>
  .stat-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-bottom: var(--border-thick);
    margin-bottom: 2rem;
  }

  .stat-block {
    padding: 2rem;
    border-right: var(--border-thin);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .stat-block:last-child {
    border-right: none;
  }

  .stat-block.highlight {
    background: var(--accent-vermilion);
    color: var(--bg-paper);
  }

  .stat-header {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 2rem;
  }

  .stat-value {
    font-family: var(--font-display);
    font-size: clamp(4rem, 6vw, 6rem);
    font-weight: 800;
    line-height: 0.9;
    letter-spacing: -0.05em;
    margin-bottom: 1rem;
  }

  .stat-value.secondary {
    color: var(--accent-cerulean);
  }

  .stat-desc {
    font-size: 1rem;
    font-weight: 500;
    max-width: 80%;
  }

  .highlight .stat-desc {
    color: rgba(255,255,255,0.9);
  }

  @media (max-width: 800px) {
    .stat-strip {
      grid-template-columns: 1fr;
    }
    .stat-block {
      border-right: none;
      border-bottom: var(--border-thin);
    }
    .stat-block:last-child {
      border-bottom: none;
    }
  }
</style>
