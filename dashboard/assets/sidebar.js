(function () {
  function isMobile() {
    return window.matchMedia("(max-width: 992px)").matches;
  }

  function closeMobileSidebar(sidebar) {
    sidebar.classList.remove("mobile-open");
  }

  function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    if (isMobile()) {
      sidebar.classList.remove("collapsed");
      sidebar.classList.toggle("mobile-open");
    } else {
      sidebar.classList.remove("mobile-open");
      sidebar.classList.toggle("collapsed");
    }
  }

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("#sidebar-toggle");
    var sidebar = document.getElementById("sidebar");

    if (toggle) {
      event.preventDefault();
      toggleSidebar();
      return;
    }

    if (
      sidebar &&
      isMobile() &&
      sidebar.classList.contains("mobile-open") &&
      !event.target.closest("#sidebar")
    ) {
      closeMobileSidebar(sidebar);
    }
  });

  document.addEventListener("click", function (event) {
    var navLink = event.target.closest("#sidebar .nav-item");
    var sidebar = document.getElementById("sidebar");
    if (navLink && sidebar && isMobile()) {
      closeMobileSidebar(sidebar);
    }
  });

  window.addEventListener("resize", function () {
    var sidebar = document.getElementById("sidebar");
    if (!sidebar) return;
    if (!isMobile()) {
      sidebar.classList.remove("mobile-open");
    } else {
      sidebar.classList.remove("collapsed");
    }
  });
})();
