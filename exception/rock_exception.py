

class ParameterError:
    def __init__(self, code):
        self.code = int(code)

    def get_ParameterError(self):
        resp = {
            "meta": {
                "code": self.code,
                "error_type": "ParameterError",
                "error_message": "Parameter Error Occurred.",
            }
        }
        return resp

class UserNotAllowed:
    def __init__(self, code, username):
        self.code = int(code)
        self.username = username


    def get_UserNotAllowed(self):
        resp = {
            "meta": {
                "code": self.code,
                "error_type": "UserNotAllowed",
                "error_message": self.username + "not allowed to access the resource.",
            }
        }
        return resp
