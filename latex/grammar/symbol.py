from abc import ABC, abstractmethod
import sys

class SymbolFactory:
    @staticmethod
    def create_instances(class_names):
        ns = sys.modules["grammar"]
        # print(f"names: {class_names}")
        return [getattr(ns, name)() for name in class_names]


class Symbol(ABC):
    @abstractmethod
    def expand(self, context=None):
        raise NotImplementedError("You must implement this method.")
    
    @abstractmethod
    def has_expanded(self):
        raise NotImplementedError("You must implement this method.")
    
    def __str__(self):
        return type(self).__name__
    
    
