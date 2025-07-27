class ApiResponse(dict):
    def __init__(self, success, code, data=None, error=None, message=None):
        super(ApiResponse, self).__init__()
        self['success'] = success
        self['code'] = code

        if data is not None:
            self['data'] = data

        if error is not None:
            self['error'] = error

        if message is not None:
            self['message'] = message
