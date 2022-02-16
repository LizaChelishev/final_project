class FlightTimesException(Exception):
    def __init__(self):
        self.message = f'Sorry the times of the flight you chose don\'t make sense, please choose different time'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
