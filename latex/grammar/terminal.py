# from roman import toRoman, fromRoman
from grammar.symbol import Symbol, SymbolFactory
from abc import ABC, abstractmethod

class Terminal(Symbol, ABC):
    def expand(self, context=None):
        return self
    
    def has_expanded(self):
        return self.value is not None
    
    def to_latex(self):
        return self.value
    
    def jsonify(self):
        return self




