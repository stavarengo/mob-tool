from abc import ABC, abstractmethod


class GitWrapperAbstract(ABC):

    @abstractmethod
    def is_dirty(self) -> bool:
        pass
