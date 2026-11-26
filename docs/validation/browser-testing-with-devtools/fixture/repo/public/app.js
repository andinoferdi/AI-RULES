// Taskboard client. Plain ES module, no build step.

const state = { tasks: [], openCount: 0 };

const openList = document.querySelector('#open-list');
const doneList = document.querySelector('#done-list');
const openCountEl = document.querySelector('#open-count');
const searchInput = document.querySelector('#search');
const results = document.querySelector('#results');
const resultList = document.querySelector('#result-list');
const filterBtn = document.querySelector('#filter-btn');
const addBtn = document.querySelector('#add-btn');
const dialog = document.querySelector('#add-dialog');
const addForm = document.querySelector('#add-form');
const cancelBtn = document.querySelector('#cancel-add');

async function loadTasks() {
  const res = await fetch('/api/tasks');
  state.tasks = await res.json();
  state.openCount = state.tasks.filter((task) => !task.done).length;
  render();
}

function taskItem(task) {
  const li = document.createElement('li');
  li.className = 'task';
  const label = document.createElement('label');
  const box = document.createElement('input');
  box.type = 'checkbox';
  box.checked = task.done;
  box.addEventListener('change', () => toggleTask(task, box.checked));
  const title = document.createElement('span');
  title.textContent = task.title;
  label.append(box, title);
  li.append(label);
  return li;
}

function render() {
  openList.replaceChildren(...state.tasks.filter((task) => !task.done).map(taskItem));
  doneList.replaceChildren(...state.tasks.filter((task) => task.done).map(taskItem));
  openCountEl.textContent = String(state.openCount);
}

async function toggleTask(task, done) {
  task.done = done;
  state.openCount += done ? -1 : 1;
  render();
  const res = await fetch(`/api/tasks/${task.id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done }),
  });
  if (!res.ok) {
    throw new Error(`Update failed with status ${res.status}`);
  }
}

searchInput.addEventListener('input', async () => {
  const query = searchInput.value.trim();
  if (!query) {
    results.hidden = true;
    return;
  }
  const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  const found = await res.json();
  resultList.replaceChildren(...found.map((task) => {
    const li = document.createElement('li');
    li.className = 'task';
    li.textContent = task.title;
    return li;
  }));
  results.hidden = false;
});

filterBtn.addEventListener('click', () => {
  document.body.classList.toggle('hide-done');
  filterBtn.classList.toggle('active');
});

addBtn.addEventListener('click', () => {
  dialog.hidden = false;
});

cancelBtn.addEventListener('click', () => {
  dialog.hidden = true;
});

addForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const title = new FormData(addForm).get('title');
  const res = await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  if (res.ok) {
    dialog.hidden = true;
    addForm.reset();
    await loadTasks();
  }
});

loadTasks();
