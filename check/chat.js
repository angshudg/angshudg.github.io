(function () {
  const STREAMLIT_APP_URL =
    "https://chat-resume-nvv8lep4dmcvw2uf3qjtth.streamlit.app";

  const fab = document.getElementById("chatFab");
  const modal = document.getElementById("chatModal");
  const closeBtn = document.getElementById("chatClose");
  const frameContainer = document.getElementById("chatFrameContainer");
  const openInNewTabLink = document.getElementById("openInNewTab");

  let iframeCreated = false;

  function openModal() {
    modal.style.display = "flex";
    modal.setAttribute("aria-hidden", "false");

    if (!iframeCreated) {
      const iframe = document.createElement("iframe");
      iframe.className = "chat-iframe";
      iframe.src = STREAMLIT_APP_URL;
      iframe.loading = "eager";
      iframe.title = "AI Chat with Amitangshu";

      frameContainer.innerHTML = "";
      frameContainer.appendChild(iframe);

      openInNewTabLink.href = STREAMLIT_APP_URL;

      iframeCreated = true;
    }
  }

  function closeModal() {
    modal.style.display = "none";
    modal.setAttribute("aria-hidden", "true");
  }

  fab.addEventListener("click", () => {
    if (modal.style.display === "flex") {
      closeModal();
    } else {
      openModal();
    }
  });

  closeBtn.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });
})();
