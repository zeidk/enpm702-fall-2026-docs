/* Remember whether the left section navigation is collapsed.
 *
 * The theme supplies the button (.primary-toggle), a hidden checkbox
 * (#pst-primary-sidebar-checkbox) and the click handler that flips it.
 * my.css makes that work on desktop. This file adds the memory.
 *
 * Only desktop state is stored. Below 960px the same checkbox means the
 * opposite thing (checked = drawer open), so persisting it there would
 * reopen the drawer on every page and flip the meaning on desktop.
 */
(function () {
  "use strict";

  var KEY = "pst-primary-sidebar-collapsed";
  var WIDE = "(min-width: 960px)";
  var root = document.documentElement;

  function isWide() {
    return window.matchMedia(WIDE).matches;
  }

  function stored() {
    try {
      return localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false; // private mode, blocked storage: fall back to shown
    }
  }

  // Apply before first paint so the sidebar does not appear and then vanish.
  if (stored()) {
    root.classList.add("pst-primary-collapsed");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var box = document.getElementById("pst-primary-sidebar-checkbox");
    var btn = document.querySelector(".primary-toggle");
    if (!box || !btn) {
      return;
    }

    // Sync the checkbox to the restored state, desktop only.
    if (isWide()) {
      box.checked = root.classList.contains("pst-primary-collapsed");
    }

    // The theme's own handler flips box.checked on click, so read it
    // after that handler has run rather than predicting the new value.
    btn.addEventListener("click", function () {
      window.setTimeout(function () {
        if (!isWide()) {
          return;
        }
        root.classList.toggle("pst-primary-collapsed", box.checked);
        try {
          localStorage.setItem(KEY, box.checked ? "1" : "0");
        } catch (e) {
          /* storage unavailable: the toggle still works for this page */
        }
      }, 0);
    });
  });
})();
