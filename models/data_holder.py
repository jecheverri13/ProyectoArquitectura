from __future__ import annotations

from typing import Generic, TypeVar, Any
from enum import Enum


T = TypeVar("T")


class DataHolderBusyException(Exception):
    pass


class DataHolderStatus(Enum):
    IDLE = 0
    BUSY = 1


class DataHolder(Generic[T]):
    def __init__(self, data: T | None):
        self.data = data
        self.initial_data = data
        self.status = DataHolderStatus.IDLE
        self.locker = None

    def get_data(self) -> T | None:
        return self.data

    def set_data(self, data: T | None, locker: Any) -> None:
        print(f"Setting data: {data} (locker: {locker}), current locker: {self.locker}")

        if (
            self.locker is not None
            and self.locker != locker
            and self.status == DataHolderStatus.BUSY
        ):
            raise DataHolderBusyException

        self.data = data

    def unlock(self, locker: Any):
        if self.locker != locker:
            raise DataHolderBusyException

        self.locker = None
        self.status = DataHolderStatus.IDLE

    def lock(self, locker: Any):
        if self.locker is not None:
            raise DataHolderBusyException

        self.locker = locker
        self.status = DataHolderStatus.BUSY
