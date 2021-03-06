class InvalidApiKeyException(Exception):
    def __init__(self):
        super(InvalidApiKeyException, self).__init__()


class InvalidArgumentException(Exception):
    def __init__(self):
        super(InvalidArgumentException, self).__init__()


class InvalidCommandException(KeyError):
    def __init__(self):
        super(InvalidCommandException, self).__init__()
