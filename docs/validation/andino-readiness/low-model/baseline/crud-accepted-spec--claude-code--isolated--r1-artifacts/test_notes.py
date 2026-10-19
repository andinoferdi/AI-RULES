import importlib
import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        # Reloading gives each test a fresh store, so ids start at 1 again.
        importlib.reload(notes)

    def test_first_id_is_one(self):
        self.assertEqual(notes.add_note("buy milk"), 1)

    def test_ids_increase_by_one(self):
        notes.add_note("buy milk")
        self.assertEqual(notes.add_note("walk dog"), 2)

    def test_list_is_empty_for_new_store(self):
        self.assertEqual(notes.list_notes(), [])

    def test_list_returns_id_title_tuples_ordered_by_id(self):
        notes.add_note("buy milk")
        notes.add_note("walk dog")
        self.assertEqual(notes.list_notes(), [(1, "buy milk"), (2, "walk dog")])

    def test_update_changes_title_and_keeps_id(self):
        notes.add_note("buy milk")
        notes.update_note(1, "buy oat milk")
        self.assertEqual(notes.list_notes(), [(1, "buy oat milk")])

    def test_update_unknown_id_raises_key_error(self):
        notes.add_note("buy milk")
        with self.assertRaises(KeyError):
            notes.update_note(99, "walk dog")
        self.assertEqual(notes.list_notes(), [(1, "buy milk")])

    def test_delete_removes_only_that_note(self):
        notes.add_note("buy milk")
        notes.add_note("walk dog")
        notes.delete_note(1)
        self.assertEqual(notes.list_notes(), [(2, "walk dog")])

    def test_delete_unknown_id_raises_key_error(self):
        notes.add_note("buy milk")
        with self.assertRaises(KeyError):
            notes.delete_note(99)
        self.assertEqual(notes.list_notes(), [(1, "buy milk")])

    def test_ids_are_not_reused_after_delete(self):
        notes.add_note("buy milk")
        notes.delete_note(1)
        self.assertEqual(notes.add_note("walk dog"), 2)


if __name__ == "__main__":
    unittest.main()
