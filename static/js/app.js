// Small Alpine helpers shared across the app. Alpine auto-initialises any
// markup htmx swaps in later, so nothing here needs to be re-wired manually.

document.addEventListener("alpine:init", () => {
  Alpine.store("theme", {
    dark: localStorage.getItem("theme") === "dark",

    init() {
      this.apply();
    },

    toggle() {
      this.dark = !this.dark;
      localStorage.setItem("theme", this.dark ? "dark" : "light");
      this.apply();
    },

    apply() {
      document.documentElement.classList.toggle("dark", this.dark);
    },
  });

  Alpine.data("dropdown", () => ({
    open: false,
  }));

  Alpine.data("toast", (level = "info", timeout = 4000) => ({
    show: false,
    level,
    init() {
      // let the enter transition play on the next tick
      requestAnimationFrame(() => (this.show = true));
      if (timeout > 0) {
        setTimeout(() => (this.show = false), timeout);
      }
    },
  }));

  // Lightweight image preview used on the "add / edit book" form.
  Alpine.data("imagePreview", (initialUrl = "") => ({
    previewUrl: initialUrl,
    onChange(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      if (this.previewUrl && this.previewUrl.startsWith("blob:")) {
        URL.revokeObjectURL(this.previewUrl);
      }
      this.previewUrl = URL.createObjectURL(file);
    },
  }));
});

// Surface a toast automatically if an htmx request fails outright, since the
// server can't inject a "response failed" message into a response it never sent.
document.body.addEventListener("htmx:responseError", () => {
  announce("Something went wrong. Please try again.", "error");
});

document.body.addEventListener("htmx:sendError", () => {
  announce("Network error — check your connection and try again.", "error");
});

function announce(text, level) {
  const region = document.getElementById("toast-region");
  if (!region) return;

  const wrapper = document.createElement("div");
  wrapper.innerHTML = `
    <div
      x-data="toast('${level}')"
      x-init="init()"
      x-show="show"
      x-transition:enter="transition ease-out duration-300"
      x-transition:enter-start="opacity-0 translate-y-2"
      x-transition:enter-end="opacity-100 translate-y-0"
      x-transition:leave="transition ease-in duration-200"
      x-transition:leave-start="opacity-100"
      x-transition:leave-end="opacity-0"
      class="pointer-events-auto flex items-start gap-3 rounded-xl border border-rose-200 bg-white px-4 py-3 text-sm text-rose-700 shadow-lg dark:border-rose-500/30 dark:bg-slate-900 dark:text-rose-300"
    >
      <span>${text}</span>
      <button type="button" @click="show = false" class="ml-auto text-rose-400 hover:text-rose-600">&times;</button>
    </div>
  `;
  region.appendChild(wrapper.firstElementChild);
}
