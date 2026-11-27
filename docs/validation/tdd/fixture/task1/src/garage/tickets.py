"""Tickets issued at the entry gate and closed at the exit gate."""
from dataclasses import dataclass
from datetime import datetime
from itertools import count

from garage.billing import fee_for_stay


@dataclass
class Ticket:
    id: int
    plate: str
    vehicle: str
    phone: str
    entry: datetime
    exit: datetime | None = None
    fee: int | None = None


def rupiah(amount: int) -> str:
    return "Rp " + f"{amount:,}".replace(",", ".")


class TicketDesk:
    def __init__(self, clock, sms):
        self._clock = clock
        self._sms = sms
        self._tickets: dict[int, Ticket] = {}
        self._ids = count(1)

    def open_ticket(self, plate: str, vehicle: str, phone: str) -> Ticket:
        ticket = Ticket(next(self._ids), plate, vehicle, phone, self._clock.now())
        self._tickets[ticket.id] = ticket
        return ticket

    def close_ticket(self, ticket_id: int) -> Ticket:
        ticket = self._tickets[ticket_id]
        if ticket.exit is not None:
            raise ValueError(f"ticket {ticket_id} is already closed")
        ticket.exit = self._clock.now()
        ticket.fee = fee_for_stay(ticket.entry, ticket.exit, ticket.vehicle)
        minutes = int((ticket.exit - ticket.entry).total_seconds() // 60)
        self._sms.send(ticket.phone,
                       f"Terima kasih. {ticket.plate} parkir {minutes // 60} jam "
                       f"{minutes % 60} menit, biaya {rupiah(ticket.fee)}.")
        return ticket
