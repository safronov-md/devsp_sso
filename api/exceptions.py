from fastapi import HTTPException


class ProblemBadRequest(HTTPException):
    def __init__(self, detail: str = "Bad Request", status_code: int = 400):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=status_code, detail=detail)


class ProblemNotFound(HTTPException):
    def __init__(self, detail: str = "Resource wasn't found", status_code: int = 404):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=status_code, detail=detail)


class ProblemUnauthorized(HTTPException):
    def __init__(self, detail: str = "Unauthorized", status_code: int = 401):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=status_code, detail=detail)
