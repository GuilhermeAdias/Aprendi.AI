// Comportamentos globais da aplicação Aprendi.AI.

(function () {
  "use strict";

  // Alterna o menu de navegação no mobile.
  const menuBtn = document.getElementById("menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", function () {
      const isHidden = mobileMenu.classList.toggle("hidden");
      menuBtn.setAttribute("aria-expanded", String(!isHidden));
    });
  }
})();
