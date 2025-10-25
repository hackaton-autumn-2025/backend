from src.exceptions.service_errors import EntityNotFoundError


class HistoryNotFoundError(EntityNotFoundError):
    entity_name = "История"

