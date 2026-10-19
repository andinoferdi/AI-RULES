import itertools

_notes = {}
_ids = itertools.count(1)


def add_note(title):
    """Store a note under a new id and return that id."""
    note_id = next(_ids)
    _notes[note_id] = title
    return note_id


def list_notes():
    """Return (id, title) tuples ordered by id."""
    return sorted(_notes.items())


def update_note(note_id, title):
    """Change the title of an existing note. Raise KeyError for an unknown id."""
    if note_id not in _notes:
        raise KeyError(note_id)
    _notes[note_id] = title


def delete_note(note_id):
    """Remove an existing note. Raise KeyError for an unknown id."""
    del _notes[note_id]
