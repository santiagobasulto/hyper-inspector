class BaseLogger:
    def __init__(self, args):
        self.args = args

    def log(self, request):
        raise NotImplementedError()
