from models.data_holder import DataHolder
from models.buses.bus import Bus

from typing import TypeVar, Any

T = TypeVar("T")


class Interface(DataHolder[T]):
    def __init__(
        self,
        bus: Bus[T],
    ):
        self.bus = bus

    def set_data(self, data: T or None, locker: Any) -> None:
        self.bus.set_data(data, locker)
        return

    def get_data(self) -> T or None:
        return self.bus.get_data()

    def lock(self, locker=None):
        return self.bus.lock(locker)

    def unlock(self, locker=None):
        return self.bus.unlock(locker)
