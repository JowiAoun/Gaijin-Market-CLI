# --- Classes
class Item:
    """
    Class representing an item from the Gaijin market.
    """

    def __init__(self, name, price_buy, price_sell, quantity_buy, quantity_sell) -> None:
        self.name: str = name
        self.price_buy: float = price_buy
        self.price_sell: float = price_sell
        self.quantity_buy: int = quantity_buy
        self.quantity_sell: int = quantity_sell
        self.profit: float = (0.85 * price_sell) - price_buy
        self.roi: float = (self.profit / price_buy) * 100
        self.link: str = "" #! Define this if necessary, remove excess writing
