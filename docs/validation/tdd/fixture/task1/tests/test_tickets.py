import unittest
from datetime import datetime

from garage.clock import FixedClock
from garage.tickets import TicketDesk
from tests.helpers import RecordingSms


class CloseTicketTest(unittest.TestCase):
    def setUp(self):
        self.clock = FixedClock(datetime(2026, 11, 2, 8, 0))
        self.sms = RecordingSms()
        self.desk = TicketDesk(self.clock, self.sms)

    def test_closing_charges_the_stay_and_texts_a_receipt(self):
        ticket = self.desk.open_ticket("B 1234 XY", "car", "0812-1111-2222")
        self.clock.advance(hours=1, minutes=30)

        closed = self.desk.close_ticket(ticket.id)

        self.assertEqual(closed.fee, 8_500)
        self.assertEqual(self.sms.sent, [(
            "0812-1111-2222",
            "Terima kasih. B 1234 XY parkir 1 jam 30 menit, biaya Rp 8.500.")])

    def test_a_ticket_closes_once(self):
        ticket = self.desk.open_ticket("B 1234 XY", "car", "0812-1111-2222")
        self.desk.close_ticket(ticket.id)
        with self.assertRaises(ValueError):
            self.desk.close_ticket(ticket.id)


if __name__ == "__main__":
    unittest.main()
