from abc import ABC, abstractmethod


class AbstractServices(ABC):
    @abstractmethod
    async def create_one():
        raise NotImplementedError

    @abstractmethod
    async def read_one_by_property():
        raise NotImplementedError

    @abstractmethod
    async def read_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_property():
        raise NotImplementedError
