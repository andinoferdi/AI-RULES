/* Load every image marked .lazy once the page has finished loading. */
window.addEventListener("load", function () {
  document.querySelectorAll("img.lazy[data-src]").forEach(function (img) {
    img.src = img.dataset.src;
  });
});
