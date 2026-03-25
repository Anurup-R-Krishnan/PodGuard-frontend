<script lang="ts">
  import { fly } from 'svelte/transition';
  import { expoOut } from 'svelte/easing';

  export let targetImage: string;
  export let scanDate: string;

  let formattedDate = new Date(scanDate).toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  }).toUpperCase();
</script>

<header class="masthead" in:fly={{ y: -20, duration: 1000, easing: expoOut }}>
  <div class="top-meta">
    <div class="meta-section">
      <span class="label">EDITION</span>
      <span class="val">VOL. 01 / EPSS</span>
    </div>
    <div class="meta-section primary">
      <span class="label">TARGET_ARCHITECTURE</span>
      <span class="val target-flash">{targetImage}</span>
    </div>
    <div class="meta-section align-right">
      <span class="label">INTELLIGENCE DATE</span>
      <span class="val">{formattedDate}</span>
    </div>
  </div>

  <h1 class="mega-title">
    <span class="outline">THREAT</span><br />
    INTELLIGENCE
  </h1>

  <div class="sub-masthead">
    <p>Contextualized exploit predictions powered by the FIRST EPSS Model & Runtime Determinism.</p>
    <div class="barcode">
      ||█|||█||██|||█|██||█|█|█|
    </div>
  </div>
</header>

<style>
  .masthead {
    border-bottom: var(--border-thick);
    padding: 2rem 0;
    margin-bottom: 2rem;
  }

  .top-meta {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    border-top: var(--border-thin);
    border-bottom: var(--border-thin);
  }

  .meta-section {
    padding: 0.75rem 1rem;
    display: flex;
    flex-direction: column;
    border-right: var(--border-thin);
  }

  .meta-section:last-child {
    border-right: none;
  }

  .meta-section.align-right {
    text-align: right;
    align-items: flex-end;
  }

  .meta-section.primary {
    background: var(--bg-inverted);
    color: var(--bg-paper);
  }

  .label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    opacity: 0.7;
    margin-bottom: 0.25rem;
  }

  .val {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    font-weight: 700;
  }

  .target-flash {
    color: var(--accent-chartreuse);
  }

  .mega-title {
    font-family: var(--font-display);
    font-size: clamp(4rem, 11vw, 12rem);
    font-weight: 800;
    line-height: 0.85;
    margin: 3rem 0;
    text-transform: uppercase;
    letter-spacing: -0.04em;
  }

  .outline {
    color: transparent;
    -webkit-text-stroke: 2px var(--ink-main);
  }

  .sub-masthead {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-family: var(--font-mono);
    font-size: 1.1rem;
    font-weight: 500;
    border-top: var(--border-thin);
    padding-top: 1rem;
  }

  .sub-masthead p {
    margin: 0;
    max-width: 60%;
  }

  .barcode {
    font-size: 2.5rem;
    line-height: 1;
    letter-spacing: -2px;
  }

  @media (max-width: 800px) {
    .top-meta {
      grid-template-columns: 1fr;
    }
    .meta-section {
      border-right: none;
      border-bottom: var(--border-thin);
    }
    .meta-section:last-child {
      border-bottom: none;
    }
    .meta-section.align-right {
      text-align: left;
      align-items: flex-start;
    }
    .mega-title {
      font-size: clamp(3.5rem, 15vw, 6rem);
    }
    .sub-masthead {
      flex-direction: column;
      align-items: flex-start;
      gap: 1.5rem;
    }
    .sub-masthead p {
      max-width: 100%;
    }
  }
</style>
