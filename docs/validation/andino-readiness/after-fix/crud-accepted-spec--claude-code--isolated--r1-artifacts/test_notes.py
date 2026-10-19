import importlib
import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        # Fresh module state per test: empty store, ids restart at 1.
        importlib.reload(notes)

    def test_add_note_returns_ids_starting_at_1(self):
        self.assertEqual(notes.add_note("first"), 1)
        self.assertEqual(notes.add_note("second"), 2)

    def test_list_notes_empty(self):
        self.assertEqual(notes.list_notes(), [])

    def test_list_notes_returns_id_title_tuples_ordered_by_id(self):
        notes.add_note("a")
        notes.add_note("b")
        notes.add_note("c")
        self.assertEqual(notes.list_notes(), [(1, "a"), (2, "b"), (3, "c")])

    def test_list_notes_stays_ordered_after_delete_and_add(self):
        notes.add_note("a")
        notes.add_note("b")
        notes.delete_note(1)
        notes.add_note("c")
        self.assertEqual(notes.list_notes(), [(2, "b"), (3, "c")])

    def test_update_note_changes_title(self):
        note_id = notes.add_note("old")
        notes.update_note(note_id, "new")
        self.assertEqual(notes.list_notes(), [(note_id, "new")])

    def test_update_unknown_id_raises_key_error(self):
        notes.add_note("a")
        with self.assertRaises(KeyError):
            notes.update_note(99, "x")
        self.assertEqual(notes.list_notes(), [(1, "a")])

    def test_delete_note_removes_it(self):
        keep = notes.add_note("keep")
        gone = notes.add_note("gone")
        notes.delete_note(gone)
        self.assertEqual(notes.list_notes(), [(keep, "keep")])

    def test_delete_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            notes.delete_note(1)

    def test_deleted_id_is_unknown_afterwards(self):
        note_id = notes.add_note("a")
        notes.delete_note(note_id)
        with self.assertRaises(KeyError):
            notes.delete_note(note_id)
        with self.assertRaises(KeyError):
            notes.update_note(note_id, "b")


if __name__ == "__main__":
    unittest.main()
