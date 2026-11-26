"""Delay between retry attempts."""


def compute_delay(attempt, base=0.5, cap=8.0):
    """Exponential delay in seconds for a zero-based attempt, capped at `cap`."""
    return min(cap, base * 2 ** attempt)
