import { useState, useEffect } from 'react'

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  if (json.ok === false) {
    throw new Error(json.error ? json.error.message : 'Unknown error');
  }
  return json.data;
}

function App() {
  const [notes, setNotes] = useState([]);
  const [actions, setActions] = useState([]);
  const [noteQuery, setNoteQuery] = useState('');
  const [actionFilter, setActionFilter] = useState('all'); // all, pending, completed

  const loadNotes = async (q = '') => {
    try {
      let url = '/notes/';
      if (q) url += `?q=${encodeURIComponent(q)}`;
      const data = await fetchJSON(url);
      setNotes(data.items);
    } catch (e) {
      console.error(e);
    }
  };

  const loadActions = async (filter = 'all') => {
    try {
      let url = '/action-items/';
      if (filter === 'pending') url += '?completed=false';
      if (filter === 'completed') url += '?completed=true';
      const data = await fetchJSON(url);
      setActions(data.items);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadNotes(noteQuery);
  }, [noteQuery]);

  useEffect(() => {
    loadActions(actionFilter);
  }, [actionFilter]);

  const handleCreateNote = async (e) => {
    e.preventDefault();
    const form = e.target;
    const title = form.title.value;
    const content = form.content.value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    form.reset();
    loadNotes(noteQuery);
  };

  const handleCreateAction = async (e) => {
    e.preventDefault();
    const form = e.target;
    const description = form.description.value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    form.reset();
    loadActions(actionFilter);
  };

  const handleCompleteAction = async (id) => {
    await fetchJSON(`/action-items/${id}/complete`, { method: 'PUT' });
    loadActions(actionFilter);
  };

  const handleBulkComplete = async () => {
    const pendingIds = actions.filter(a => !a.completed).map(a => a.id);
    if (pendingIds.length === 0) return;
    
    await fetchJSON('/action-items/bulk-complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_ids: pendingIds }),
    });
    loadActions(actionFilter);
  };

  const handleDeleteNote = async (id) => {
      await fetchJSON(`/notes/${id}`, { method: 'DELETE' });
      loadNotes(noteQuery);
  };

  return (
    <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>Modern Software Dev Starter (React)</h1>

      <section style={{ marginBottom: '3rem' }}>
        <h2>Notes</h2>
        <div style={{ marginBottom: '1rem' }}>
          <input 
            type="text" 
            placeholder="Search notes..." 
            value={noteQuery}
            onChange={(e) => setNoteQuery(e.target.value)}
            style={{ padding: '0.5rem', width: '100%' }}
          />
        </div>
        
        <form onSubmit={handleCreateNote} style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
          <input name="title" placeholder="Title" required style={{ flex: 1, padding: '0.5rem' }} />
          <input name="content" placeholder="Content" required style={{ flex: 2, padding: '0.5rem' }} />
          <button type="submit" style={{ padding: '0.5rem 1rem' }}>Add</button>
        </form>

        <ul style={{ listStyle: 'none', padding: 0 }}>
          {notes.map(note => (
            <li key={note.id} style={{ padding: '0.5rem', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
              <div>
                <strong>{note.title}</strong>: {note.content}
                <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.2rem' }}>
                    {note.tags && note.tags.map(t => <span key={t.id} style={{marginRight: '0.5rem', background: '#e0e0e0', padding: '2px 6px', borderRadius: '4px'}}>#{t.name}</span>)}
                </div>
              </div>
              <button onClick={() => handleDeleteNote(note.id)} style={{ color: 'red', border: 'none', background: 'none', cursor: 'pointer' }}>Delete</button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Action Items</h2>
        <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
          <button onClick={() => setActionFilter('all')} disabled={actionFilter === 'all'}>All</button>
          <button onClick={() => setActionFilter('pending')} disabled={actionFilter === 'pending'}>Pending</button>
          <button onClick={() => setActionFilter('completed')} disabled={actionFilter === 'completed'}>Completed</button>
          <button onClick={handleBulkComplete} style={{ marginLeft: 'auto' }}>Complete All Visible</button>
        </div>

        <form onSubmit={handleCreateAction} style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
          <input name="description" placeholder="Description" required style={{ flex: 1, padding: '0.5rem' }} />
          <button type="submit" style={{ padding: '0.5rem 1rem' }}>Add</button>
        </form>

        <ul style={{ listStyle: 'none', padding: 0 }}>
          {actions.map(action => (
            <li key={action.id} style={{ padding: '0.5rem', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ textDecoration: action.completed ? 'line-through' : 'none', color: action.completed ? '#999' : 'inherit' }}>
                {action.description}
              </span>
              {!action.completed && (
                <button onClick={() => handleCompleteAction(action.id)}>Complete</button>
              )}
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}

export default App
