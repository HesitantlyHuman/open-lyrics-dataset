class TooFastError(Exception):
    def __init__(self, response = None, wait = 5, **kwargs):
        super(self, TooFastError).__init__(kwargs)
        self.wait = wait
        self.response = response

    def __str__(self) -> str:
        if not self.response is None:
            return f'Recieved a response of {self.response}, wait {self.wait} seconds'
        else:
            return f'You are going too fast, wait {self.wait} seconds'
