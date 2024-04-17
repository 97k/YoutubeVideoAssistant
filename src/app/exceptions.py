class HuggingFaceInferenceException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LLMTasksPandasError(Exception):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class LLMNotProvidedException(Exception):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)


class EmbeddingModelNotProvided(Exception):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)
