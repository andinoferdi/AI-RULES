# Shelf

The vocabulary of the Northside Tool Library.

## Language

**Tool**:
A kind of thing the library lends, such as "cordless drill".
_Avoid_: product, listing

**Item**:
One physical copy of a **Tool**, with its own barcode.
_Avoid_: unit, asset

**Member**:
A person registered to borrow from the library.
_Avoid_: user, customer, borrower

**Volunteer**:
A person who staffs the desk. A volunteer may also be a **Member**.
_Avoid_: staff, admin

**Loan**:
An **Item** checked out to a **Member**, from checkout until it is returned.
_Avoid_: rental, booking

**Hold**:
A **Member**'s place in the queue for a **Tool** that has no **Item** on the shelf.
_Avoid_: reservation, booking

**Overdue**:
A **Loan** past its due date that has not been returned.
