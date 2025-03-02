from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any, Dict, Union

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        엔티티를 저장하거나 업데이트합니다.
        """
        pass
    
    @abstractmethod
    def delete(self, id: Union[str, int]) -> bool:
        """
        ID로 엔티티를 삭제합니다.
        """
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """
        ID로 엔티티를 조회합니다.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        모든 엔티티를 조회합니다.
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        전체 엔티티 수를 반환합니다.
        """
        pass
    
    @abstractmethod
    def exists(self, id: int) -> bool:
        """
        해당 ID의 엔티티가 존재하는지 확인합니다.
        """
        pass
