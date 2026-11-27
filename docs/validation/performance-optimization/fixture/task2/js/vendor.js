/* Readable stub of the production vendor bundle (carousel + analytics SDK, ~380 KB minified). */
(function () {
  window.Carousel = {
    init: function (root, options) {
      var slides = root.querySelectorAll("blockquote");
      var index = 0;
      slides[0].classList.add("active");
      setInterval(function () {
        slides[index].classList.remove("active");
        index = (index + 1) % slides.length;
        slides[index].classList.add("active");
      }, options.interval);
    }
  };
  window.Analytics = {
    track: function (name) {
      navigator.sendBeacon && navigator.sendBeacon("/collect", JSON.stringify({ event: name }));
    }
  };
})();
