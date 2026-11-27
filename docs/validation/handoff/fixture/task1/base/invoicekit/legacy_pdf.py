"""Old PDF title helper, still used by the archive job."""


def title(invoice):
    return f"Invoice {invoice.number}"
