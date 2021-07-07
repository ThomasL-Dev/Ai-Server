

class RequestObject:

    def __init__(self, kernel, name: str, sender: str, input: str, timestamp: str, type: str):

        self.name = name
        self.sender = sender
        self.input = input
        self.timestamp = timestamp
        self.type = type


    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'name={self.name!r}, '
                f'sender={self.sender!r}, '
                f'input={self.input!r}, '
                f'timestamp={self.timestamp!r}, '
                f'type={self.type!r}'
                f')'
                )