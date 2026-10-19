_notes = {}
_next_id = 1


def add_note(title):
    global _next_id
    note_id = _next_id
    _notes[note_id] = title
    _next_id += 1
    return note_id


def list_notes():
    return sorted(_notes.items())


def update_note(note_id, title):
    if note_id not in _notes:
        raise KeyError(note_id)
    _notes[note_id] = title


def delete_note(note_id):
    del _notes[note_id]
