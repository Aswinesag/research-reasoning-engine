class LLMError(Exception):
    pass

class LLMTimeoutError(LLMError):
    pass

class LLMOutputValidationError(LLMError):
    pass