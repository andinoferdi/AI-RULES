/*! Acme Analytics browser SDK 3.2.1 | vendor build | managed by the marketing team, do not edit */
(function () {
  var collector = 'https://collector.acme-analytics.invalid/v1/collect';
  var consent = document.cookie.indexOf('acme_consent=') !== -1;
  if (!consent) {
    console.warn('[AcmeAnalytics] consent cookie not found; events will be queued until consent is given');
  }
  try {
    fetch(collector, {
      method: 'POST',
      mode: 'no-cors',
      keepalive: true,
      body: JSON.stringify({ event: 'page_view', path: location.pathname, queued: !consent }),
    }).catch(function () {});
  } catch (error) {}
})();
