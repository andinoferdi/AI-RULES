import itertools

_notes = {}
_next_id = itertools.count(1)


def add_note(title):
    note_id = next(_next_id)
    _notes[note_id] = title
    return note_id


def list_notes():
    return sorted(_notes.items())


def update_note(note_id, title):
    if note_id not in _notes:
        raise KeyError(note_id)
    _notes[note_id] = title


def delete_note(note_id):
    if note_id not in _notes:
        raise KeyError(note_id)
    del _notes[note_id]
