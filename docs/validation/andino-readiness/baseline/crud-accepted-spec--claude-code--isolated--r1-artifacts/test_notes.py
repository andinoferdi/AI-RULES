import importlib
import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        importlib.reload(notes)

    def test_add_returns_ids_starting_at_one(self):
        self.assertEqual(notes.add_note("first"), 1)
        self.assertEqual(notes.add_note("second"), 2)

    def test_list_empty(self):
        self.assertEqual(notes.list_notes(), [])

    def test_list_returns_id_title_tuples_ordered_by_id(self):
        notes.add_note("a")
        notes.add_note("b")
        notes.add_note("c")
        self.assertEqual(notes.list_notes(), [(1, "a"), (2, "b"), (3, "c")])

    def test_update_changes_title(self):
        note_id = notes.add_note("draft")
        notes.update_note(note_id, "final")
        self.assertEqual(notes.list_notes(), [(1, "final")])

    def test_delete_removes_note(self):
        notes.add_note("keep")
        doomed = notes.add_note("drop")
        notes.delete_note(doomed)
        self.assertEqual(notes.list_notes(), [(1, "keep")])

    def test_ids_are_not_reused_after_delete(self):
        notes.add_note("a")
        second = notes.add_note("b")
        notes.delete_note(second)
        self.assertEqual(notes.add_note("c"), 3)

    def test_update_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            notes.update_note(99, "x")
        self.assertEqual(notes.list_notes(), [])

    def test_delete_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            notes.delete_note(99)


if __name__ == "__main__":
    unittest.main()
