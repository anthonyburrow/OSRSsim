
class Bank:

    def __init__(self, items: dict = None):
        if items is None:
            items = {}
        self._items = items

        # Remove zero/negative quantities
        self._items = {item: quantity for item, quantity in self._items.items()
                       if quantity > 0}

    def add(self, items=None, *args, **kwargs) -> None:
        if isinstance(items, str):
            self._add_item(items, *args, **kwargs)
        elif isinstance(items, dict):
            self._add_dict(items)
        elif isinstance(items, Bank):
            self._add_bank(items)

    def remove(self, item: str, quantity: int) -> None:
        if not self.contains(item, quantity):
            raise ValueError(f'Bank does not contain {quantity}x {item}')

        new_quantity = self._items[item] - quantity

        if new_quantity <= 0:
            self._items.pop(item)
        else:
            self._items[item] = new_quantity

    def contains(self, item: str, quantity: int = None) -> bool:
        # TODO: Add bank optional argument instead of single item
        if item not in self._items:
            return False

        if quantity is None:
            return True

        in_bank = self._items[item]

        return in_bank >= quantity

    def quantity(self, item: str) -> int:
        if not self.contains(item):
            return 0

        return self._items[item]

    def __str__(self) -> str:
        msg = '  BANK\n'
        for item, quantity in self._items.items():
            msg += f'  {item} {quantity}x\n'

        return msg

    def _add_item(self, item: str, quantity: int = 1) -> None:
        if quantity < 0:
            raise ValueError(f'Tried to add negative {item} to bank')

        if quantity == 0:
            return

        if not self.contains(item):
            self._items[item] = quantity
            return

        self._items[item] += quantity

    def _add_dict(self, items: dict) -> None:
        for item, quantity in items.items():
            self._add_item(item, quantity)

    def _add_bank(self, bank) -> None:
        # Could just make this a __add__, etc dunder
        for item, quantity in bank._items.items():
            self._add_item(item, quantity)
