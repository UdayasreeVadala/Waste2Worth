class ContractError(ValueError):
    def __init__(self, code, message, field=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field

    def to_dict(self):
        error = {"code": self.code, "message": self.message}
        if self.field:
            error["field"] = self.field
        return {"error": error}

