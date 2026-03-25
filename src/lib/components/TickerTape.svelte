<script>
  // Simple CSS scrolling ticker tape for a maximalist magazine feel
  const messages = [
    "EPSS MODEL UPDATED 04:00Z //",
    "CVE-2024-3094 XZ BACKDOOR EXPLOIT PROBABILITY DECREASED //",
    "NEW KEV ENTRIES DETECTED: 12 //",
    "LOG4SHELL REACHES 3-YEAR ANNIVERSARY //",
    "GLOBAL THREAT INDEX: ELEVATED //",
    "ZERO-DAY OBSERVED IN WILD, AWAITING NVD ENTRY //"
  ];

  let displayString = messages.join('     ') + '     ' + messages.join('     ');
</script>

<div class="ticker-wrapper">
  <div class="ticker-track">
    <div class="ticker-text">{displayString}</div>
    <div class="ticker-text">{displayString}</div>
  </div>
</div>

<style>
  .ticker-wrapper {
    width: 100%;
    background: var(--ink-main);
    color: var(--accent-chartreuse);
    padding: 0.5rem 0;
    overflow: hidden;
    position: relative;
    border-bottom: var(--border-thick);
    white-space: nowrap;
    display: flex;
  }

  .ticker-track {
    display: flex;
    width: 200%;
    animation: marquee 40s linear infinite;
  }

  .ticker-text {
    width: 100%;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.1em;
  }

  @keyframes marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }
</style>
