(function () {
  const STREAMLIT_APP_URL = "https://chat-resume-nvv8lep4dmcvw2uf3qjtth.streamlit.app/"; 
  const fab = document.getElementById("chatFab");
  const modal = document.getElementById("chatModal");
  const closeBtn = document.getElementById("chatClose");
  const frameContainer = document.getElementById("chatFrameContainer");

  let iframeCreated = false;
  let embedTimeout;

  function createIframe() {
    frameContainer.innerHTML = '<div class="loader">Loading chat…<div style="margin-top:8px"><a id="openInNewTab" href="' + STREAMLIT_APP_URL + '" target="_blank" rel="noopener">Open in a new tab</a></div></div>';

    const iframe = document.createElement('iframe');
    iframe.className = 'chat-iframe';
    iframe.src = STREAMLIT_APP_URL;
    iframe.loading = 'eager';
    iframe.title = 'AI Chat with Amitangshu';

    // If the iframe successfully loads, replace loader with iframe
    iframe.addEventListener('load', () => {
      clearTimeout(embedTimeout);
      frameContainer.innerHTML = '';
      frameContainer.appendChild(iframe);
    });

    // Append the iframe (loader stays visible until load)
    frameContainer.appendChild(iframe);

    // If no load within 6s, assume embedding blocked; show prominent fallback
    embedTimeout = setTimeout(() => {
      frameContainer.innerHTML = '<div class="loader">Embedding blocked or stalled — <a href="' + STREAMLIT_APP_URL + '" target="_blank" rel="noopener">Open chat in a new tab</a></div>';
    }, 6000);

    iframeCreated = true;
  }

  function openModal() {
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden','false');
    if (!iframeCreated) createIframe();
  }

  function closeModal() {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden','true');
  }

  fab.addEventListener('click', () => { modal.style.display === 'flex' ? closeModal() : openModal(); });
  closeBtn.addEventListener('click', closeModal);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
})();
