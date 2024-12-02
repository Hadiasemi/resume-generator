from grammar.terminal import Terminal
from grammar.nonterminal import Nonterminal
import random
from grammar.symbol import SymbolFactory
import latex_formats as lf


class ExperienceSection(Nonterminal):
    rules = [(("Experience",) * i, 1 / 3) for i in range(1, 4)]
    latex = lf.latex["ExperienceSection"]
    
    def __init__(self):
        super().__init__(ExperienceSection.rules, ExperienceSection.latex)

    def expand(self, context=None):
        if not context:
            context = {}
        
        child_types = random.choices(*zip(*self.rules))[0]
        self.children = SymbolFactory.create_instances(child_types)
        
        dates = ["September 2017 - Decembter 2017", "September 2018 - December 2018", "September 2019 - December 2019", "September 2020 - December 2020"]
        for i, child in enumerate(self.children):
            cur_context = context.copy()
            cur_context['date'] = dates[i]
            child.expand(cur_context)
            
        return self
        
class Experience(Nonterminal):
    rules = [
        (("CompanyName", "JobTitle", "DateRange", "GeographicalInfo", "ExperienceTasks"), 1.0)
    ]
    latex = lf.latex["Experience"]
    
    def __init__(self):
        super().__init__(Experience.rules, Experience.latex)
        
    def to_latex(self):
        if self.has_expanded(): 
            return self.latex % tuple([child.to_latex() for child in self.children])
        else:
            raise Exception(f"{self} must be expanded first")
        
class ExperienceTasks(Nonterminal):
    def __init__(self):
        super().__init__(
            [(('ExperienceTask',) * j, 0.2) for j in range(1, 5)], r'%s'
        )
        
    def to_latex(self):
        if self.has_expanded():
            return "\n".join([f"\\item {child.to_latex()}" for child in self.children])
    
class ExperienceTask(Terminal):
    def __init__(self):
        self.value = None
        
    def expand(self, context=None):
        self.value = "Did a thing"
        return self

class CompanyName(Terminal):
    COMPANY_MAP = {
        "Google": "https://www.google.com",
        "Apple, Inc.": "https://www.apple.com"
    }
    
    def __init__(self):
        self.value = None
        
    def expand(self, context=None):
        company = random.choice(list(self.COMPANY_MAP.keys()))
        self.value = r'''%s [\href{%s}{\faIcon{globe}}]''' % (company, self.COMPANY_MAP[company])
        return self
    
class JobTitle(Terminal):
    def __init__(self):
        self.value = None
        
    def expand(self, context=None):
        self.value = "Software Engineer"
        return self
    
class DateRange(Terminal):
    def __init__(self):
        self.value = None
        
    def expand(self, context=None):
        context = context or {}
        self.value = context.get("date") or "June 2022 - Present"
        return self