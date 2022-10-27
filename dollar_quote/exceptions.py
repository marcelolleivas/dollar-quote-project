class ServiceException(Exception):
    """
    A base class for domain exceptions related to
    services handling operations.
    """


class ServiceStatusException(ServiceException):
    """
    This exception is raised when trying to get
    data from a third service but the API returned
    an error.
    """

    ...
