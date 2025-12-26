async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  if (json.ok === false) {
    throw new Error(json.error ? json.error.message : 'Unknown error');
  }
  return json.data; // Unwrap the envelope
}

async function loadNotes(query = '') {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  
  let url = '/notes/';
  if (query) {
    url = `/notes/?q=${encodeURIComponent(query)}`;
  }
  
  const response = await fetchJSON(url);
  // Now response is PaginatedResponse object (items, total, etc.)
  const notes = response.items;
  
  for (const n of notes) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    list.appendChild(li);
  }
}

let currentActionItems = [];

async function loadActions(completed = null) {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  
  let url = '/action-items/';
  if (completed !== null) {
    url += `?completed=${completed}`;
  }
  
  const response = await fetchJSON(url);
  // Response is PaginatedResponse
  const items = response.items;
  currentActionItems = items;

  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions(completed);
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

// Bulk complete handler
document.addEventListener('DOMContentLoaded', () => {
  const bulkBtn = document.getElementById('bulk-complete-btn');
  if (bulkBtn) {
    bulkBtn.addEventListener('click', async () => {
      const pendingIds = currentActionItems
        .filter(item => !item.completed)
        .map(item => item.id);
      
      if (pendingIds.length === 0) return;

      await fetchJSON('/action-items/bulk-complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_ids: pendingIds }),
      });
      // Reload current view
      // Determine current filter from UI state is hard without saving it, 
      // but simplistic reload works:
      loadActions(); 
    });
  }
});

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  document.getElementById('note-search').addEventListener('input', (e) => {
    loadNotes(e.target.value);
  });

  loadNotes();
  loadActions();
});
