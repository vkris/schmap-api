class SchmapAPIException(Exception):
    STATUS_MAP= {
            401:  "HTTP 401 Authorization Exception. Check Username and password",
            7000: "Empty Response",
            7001: "Expected JSON response but got HTML response",
            7002: "No request id found in the response",
            7003: "Not a valid JSON",
            7004: "Not a valid request id",
            7005: "No progress for so long time. Quitting",
            1000: "API_BAD_REQUEST",
            1001: "API_MISSING_PARAM",
            1002: "API_ERROR_BAD_PARAM_VALUE ",
            1003: "API_ERROR_ANALYSIS_NOT_FOUND ",
            1004: "API_ERROR_LIST_NOT_FOUND ",
            1005: "API_ERROR_UNRECOGNIZED_REQUEST ",
            1006: "API_ERROR_SANDBOX_DISALLOWED ",
            1007: "API_ERROR_MUST_USE_HTTPS",
            2000: "API_ERROR_TWIT_READ_FAILURE",
            5001: "API_ERROR_USER_NOT_AUTHORIZED",
            6000: "API_ERROR_ANALYSIS_FAILED",
            9000: "API_ERROR_SOFTWARE_ERROR",
            9001: "API_DATABASE_INCONSISTANCY",
            }
    def __init__(self, status=-1):
        self.status = status

    def __str__(self):
        return "%s (%s)" % (self.status, self.STATUS_MAP.get(self.status, 'Unknown error.'))

    def __repr__(self):
        return "%s(status=%s)" % (self.__class__.__name__, self.status)
    
