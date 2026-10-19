import importlib
import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        # Reload so each test starts with an empty store and ids restart at 1.
        importlib.reload(notes)

    def test_add_note_returns_first_id_as_one(self):
        self.assertEqual(notes.add_note("first"), 1)

    def test_add_note_assigns_increasing_ids(self):
        notes.add_note("first")
        self.assertEqual(notes.add_note("second"), 2)

    def test_list_notes_is_empty_for_new_store(self):
        self.assertEqual(notes.list_notes(), [])

    def test_list_notes_returns_id_title_tuples_ordered_by_id(self):
        notes.add_note("first")
        notes.add_note("second")
        self.assertEqual(notes.list_notes(), [(1, "first"), (2, "second")])

    def test_update_note_changes_title(self):
        note_id = notes.add_note("old")
        notes.update_note(note_id, "new")
        self.assertEqual(notes.list_notes(), [(note_id, "new")])

    def test_update_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            notes.update_note(99, "missing")

    def test_delete_note_removes_it(self):
        first = notes.add_note("first")
        second = notes.add_note("second")
        notes.delete_note(first)
        self.assertEqual(notes.list_notes(), [(second, "second")])

    def test_delete_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            notes.delete_note(99)

    def test_deleted_id_is_not_reused(self):
        first = notes.add_note("first")
        notes.delete_note(first)
        self.assertEqual(notes.add_note("second"), 2)


if __name__ == "__main__":
    unittest.main()
