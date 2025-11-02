from impl import CAPUCCINO_MILK_REQUIRED


class NotEnoughMilkException(Exception):
    pass


class CofeeMachine:
    def __init__(self):
        self.milk = 0

    def add_milk(self, amount: int):
        self.milk += amount

    def buy_cappuccino(self):
        if not self.milk >= CAPUCCINO_MILK_REQUIRED:
            raise NotEnoughMilkException("Not enough resources to make cappuccino")

        self.milk -= CAPUCCINO_MILK_REQUIRED