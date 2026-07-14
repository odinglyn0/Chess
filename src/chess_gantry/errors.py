"""Project-specific exception types."""


class GantryError(Exception):
    """Base class for expected gantry errors."""


class ConfigurationError(GantryError):
    """Raised when configuration is missing or unsafe."""


class ValidationError(GantryError):
    """Raised when JSON input or persistent state is invalid."""


class StateError(GantryError):
    """Raised when a move does not agree with the stored board state."""


class PlanningError(GantryError):
    """Raised when a collision-free motion path cannot be generated."""


class SerialProtocolError(GantryError):
    """Raised when Marlin reports an error or fails to acknowledge a command."""


class PendingTransactionError(GantryError):
    """Raised when a previous move has not been reconciled."""
