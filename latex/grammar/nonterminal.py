from __future__ import annotations
import random
import sys
from abc import ABC
from roman import toRoman, fromRoman
from grammar.symbol import Symbol, SymbolFactory

# class NonterminalFactory:
#     @staticmethod
#     def create_instances(class_names):
#         current_module = sys.modules[__name__]
#         return [getattr(current_module, name)() for name in class_names]

class Nonterminal(Symbol):
    def __init__(self, rules):
        self.rules = rules
        self.children = None

    def expand(self):
        children = random.choice(zip(*self.rules))
        self.children = [child.expand() for child in SymbolFactory.create_instances(children)]
        return self

    def has_expanded(self):
        return self.children is not None

    

class S(Nonterminal):
    rules = [
        (("Head", "Body"), 1.0),
        (("Head", "Body", "Footer"), 0.0)
    ]

    def __init__(self):
        # instance attributes
        super().__init__(S.rules)

    def __str__(self):
        return "S"
    
    def get_leaves(self):
        if self.has_expanded():
            pass
            #TODO: get stuff from the terminals

    
class Head(Nonterminal):
    rules = [
        (("Experience",), 1.0)
    ]
    def __init__(self):
        super().__init__(Head.rules)

class Body(Nonterminal):
    rules = [
        (("Experience"), 1.0)
    ]
    def __init__(self):
        super().__init__(Body.rules)


    #sequence of subheadings

class Experience(Nonterminal):
    rules = []
    latex = '''
        \\section{\\textbf{Experience}}
        \\vspace{-0.4mm}
        \resumeSubHeadingListStart
            %s
        \resumeSubHeadingListEnd
        \vspace{-6mm}
    '''
    # ExperienceSubHeadings
    #latex % expsubheading.to_latex()
    def __init__(self):
        super().__init__(Experience.rules)


class ExperienceSubheading(Nonterminal):
    count = 0
    rules = [
        (("ExperienceDetails", "ExperienceItemList"), 1.0)
    ]

    #ExpSub -> JobDeets(Term) JobAchievements(Nonterm)
    #JobAchievements -> item *

    latex = '''
         \resumeSubheading
            {{Company A}}{City, Country}
            {Job Title A}{Month Year - Month Year}
            \resumeItemListStart
                \item Developed [specific achievement] achieving [specific metric] in [specific area]
                \item Implemented [technology/method], enhancing [specific aspect] by [specific percentage]
                \item Conducted analysis on [specific data], identifying [key findings]
                \item Presented findings at [specific event], receiving [specific recognition]
            \resumeItemListEnd 
    '''
    
    def __init__(self):
        ExperienceSubheading.count += 1
        self.id = ExperienceSubheading.count

    #f"company{toRoman(self.id)}"
        

    




class Footer(Nonterminal):
    pass




        
    