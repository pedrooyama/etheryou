class GasLimitExceeded(Exception):
    MESSAGE = 'Exceeds block gas limit'

    def __init__(self):
        super().__init__('Gas limit Exceeded: Raise its value in Ganache')
