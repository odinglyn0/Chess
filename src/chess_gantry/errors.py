

class GantryError(Exception):
    pass


class ConfigurationError(GantryError):
    pass


class ValidationError(GantryError):
    pass


class StateError(GantryError):
    pass


class PlanningError(GantryError):
    pass


class SerialProtocolError(GantryError):
    pass


class PendingTransactionError(GantryError):
    pass
