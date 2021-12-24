from werkzeug.exceptions import HTTPException


class UnknownError(HTTPException):
    code = 400


class DataFormatError(HTTPException):
    code = 422


class AuthError(HTTPException):
    code = 401


class UserExistsError(HTTPException):
    code = 403


class UserFollowError(HTTPException):
    code = 403


class PostExistsError(HTTPException):
    code = 403


class AccessError(HTTPException):
    code = 403
