class ProjectAlreadyExistsError(Exception):
    """ Raised when a project is already initialized. """


class ServiceAlreadyExistsError(Exception):
    """ Raised when a service already exists. """


class ServiceDoesNotExistError(Exception):
    """ Raised when a service does not exists. """
