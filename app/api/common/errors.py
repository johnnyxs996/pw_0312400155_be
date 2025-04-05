from typing import Optional

from fastapi import status


class GenericException(Exception):
    def __init__(
        self,
        status_code: Optional[int] = 500,
        message: Optional[str] = None,
        type: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.type = type or self.__class__.__name__


class InvalidCredentialsError(GenericException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Sono state inserite delle credenziali errate.")


class OperationAmountTooLargeError(GenericException):
    def __init__(self, available_amount: float):
        super().__init__(
            status_code=400,
            message=f"Importo non disponibile. L'importo massimo disponibile è: {available_amount}")


class ResourceAlreadyInStatusError(GenericException):
    def __init__(self, status: str):
        super().__init__(
            status_code=400,
            message=f"Risorsa già in stato {status}.")


class ResourceNotFoundError(GenericException):
    def __init__(self, resource_id: str):
        super().__init__(
            status_code=404,
            message=f'Risorsa con id "{resource_id}" non trovata.')


class DuplicateKeyError(GenericException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message="Esiste già una risorsa con lo stesso identificativo.")
