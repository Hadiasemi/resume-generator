# from __future__ import annotations
import random
from roman import toRoman, fromRoman
from grammar.symbol import Symbol, SymbolFactory
import latex_formats as lf
from abc import ABC
# from collections import ChainMap


class Nonterminal(Symbol, ABC):
    def __init__(self, rules, latex):
        self.rules = rules
        self.latex = latex
        self.children = None

    #Nonterminals do not need to override expand
    def expand(self, context=None):
        # print(f"rules: {self.rules}")
        child_types = random.choices(*zip(*self.rules))[0]
        self.children = [child.expand(context) for child in SymbolFactory.create_instances(child_types)]
        return self

    def has_expanded(self):
        return self.children is not None
    
    #sometimes need to override this
    def to_latex(self):
        print(f"{self}")
        if self.has_expanded():
            print(str(self), self.children)
            return self.latex % ("\n".join(child.to_latex() for child in self.children),)
        else:
            raise Exception(f"{self} must be expanded first")
        
    def jsonify(self):
        return {
            str(self): [child.jsonify() for child in self.children]
        }


class S(Nonterminal):
    rules = [
        # (("Head", "Body"), 1.0),
        # (("Head", "Body", "Footer"), 0.0)
        (("Head", "Body"), 1.0)
    ]
    latex = lf.latex["S"]

    def __init__(self):
        # instance attributes
        super().__init__(S.rules, S.latex)
    
    
    