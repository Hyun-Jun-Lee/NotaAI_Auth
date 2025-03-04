from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any

class BaseRepository(ABC):
    
    @abstractmethod
    def save(self, entity: Any) -> Any:
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
    def get_by_id(self, id: int) -> Optional[Any]:
        """
        ID로 엔티티를 조회합니다.
        """
        pass
