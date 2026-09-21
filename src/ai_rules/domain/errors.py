class AiRulesError(Exception):
    """Base exception for AI-RULES control-plane failures."""


class ValidationError(AiRulesError):
    """Raised when catalog, profile, state, or model data is invalid."""


class UnsafeMutationError(AiRulesError):
    """Raised when a planned mutation would cross a safety boundary."""
