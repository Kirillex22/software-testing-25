class AccountDoesnExistExeption(Exception):
    pass


class NotEnoughMoneyException(Exception):
    pass


class ATM:
    def __init__(self):
        self._accounts: dict[str, float]  = {}

    def add_account(self, name: str) -> None:
        if name not in self._accounts:
            self._accounts[name] = 0.0

    def deposit(self, name: str, amount: float) -> None:
        if self._accounts.get(name, None) is None:
            raise AccountDoesnExistExeption("Account does not exist")
        self._accounts[name] += amount

    def withdraw(self, name: str, amount: float) -> None:
        if self._accounts.get(name, None) is None:
            raise AccountDoesnExistExeption("Account does not exist")

        after_transaction = self._accounts[name] - amount
        
        if after_transaction < 0:
            raise NotEnoughMoneyException("Not enough money on account")

        self._accounts[name] = after_transaction

    def get_balance(self, name: str) -> float:
        if self._accounts.get(name, None) is None:
            raise AccountDoesnExistExeption("Account does not exist")
        return self._accounts[name]