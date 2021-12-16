from classic.app import errors


class AuthenticationError(Exception):
    ...


class AuthenticationIsNotAvailable(errors.AppError):
    msg_template = 'Authentication is not available, resource is [{resource_name}]'
    code = 'classic.auth.authentication_is_not_available'


class PermissionDenied(errors.AppError):
    msg_template = 'Permission denied, resource is [{resource_name}]'
    code = 'classic.auth.permission_denied'
