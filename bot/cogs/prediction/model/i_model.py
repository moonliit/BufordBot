from abc import ABC, abstractmethod
from typing import Dict

class IModel(ABC):
    label_mapping: Dict[int, str]

    @abstractmethod
    def predict(self, text: str) -> Dict[str, float]:
        pass