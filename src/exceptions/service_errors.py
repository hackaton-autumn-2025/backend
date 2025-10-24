class ServiceError(Exception):
    pass


class EntityNotFoundError(ServiceError):
    entity_name = "Сущность"

    def __init__(self, id: int | None = None, name: str | None = None):
        if id and name:
            message = f"{self.entity_name} с id {id} и названием {name} не найдена"
        elif id:
            message = f"{self.entity_name} с id {id} не найдена"
        elif name:
            message = f"{self.entity_name} с названием {name} не найдена"
        else:
            message = f"{self.entity_name} не найдена"

        super().__init__(message)


class EntityAlreadyExistError(ServiceError):
    entity_name = "Сущность"

    def __init__(self, id: int | None = None, name: str | None = None):
        if id and name:
            message = f"{self.entity_name} с id {id} и названием {name} уже существует"
        elif id:
            message = f"{self.entity_name} с id {id} уже существует"
        elif name:
            message = f"{self.entity_name} с названием {name} уже существует"
        else:
            message = f"{self.entity_name} уже существует"

        super().__init__(message)
