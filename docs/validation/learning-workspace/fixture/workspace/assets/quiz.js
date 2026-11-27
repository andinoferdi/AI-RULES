// Usage: <fieldset data-answer="b" data-why="..."> with radio inputs valued a-d and a <p class="feedback"> inside.
document.querySelectorAll('.quiz fieldset').forEach(function (set) {
  set.addEventListener('change', function (event) {
    var feedback = set.querySelector('.feedback');
    var correct = event.target.value === set.dataset.answer;
    feedback.className = 'feedback ' + (correct ? 'ok' : 'bad');
    feedback.textContent = correct ? 'Benar. ' + (set.dataset.why || '') : 'Belum tepat. Coba lagi.';
  });
});
