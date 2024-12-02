
from grammar.nonterminal import Nonterminal
from grammar.terminal import Terminal
import random
import latex_formats as lf
from collections import ChainMap
from data_factory import NameDataFactory

class Head(Nonterminal):
    rules = [
        (("Title", "PhoneEmail", "LinkedInGitHub", "GeographicalInfoField"), 1.0)
    ]
    latex = lf.latex["Head"]
    def __init__(self):
        super().__init__(Head.rules, Head.latex)

class Title(Nonterminal):
    rules = [
        (("FullName",), 1.0)
    ]
    latex = lf.latex["Title"]
    def __init__(self):
        super().__init__(Title.rules, Title.latex)



class PhoneEmail(Nonterminal):
    rules = [
       (("Phone", "Email"), 0.5),
       (("Email", "Phone"), 0.5),
    ]
    latex = lf.latex["PhoneEmail"]
    def __init__(self):
        super().__init__(PhoneEmail.rules, PhoneEmail.latex)

    def to_latex(self):
        if self.has_expanded():
            assert(len(self.children) == 2)
            # print(f"type: {self}")
            # print(f"children: {self.children}")
            # c1, c2 = self.children
            # values = ChainMap(c1.get(), c2.get())
            # return self.latex % (values[str(c1)], values[str(c2)])
            return self.latex % tuple(child.to_latex() for child in self.children)
        else:
            raise Exception(f"{self} must be expanded first")

   


class LinkedInGitHub(Nonterminal):
    rules = [
        (("LinkedInField", "GitHubField"), 0.5),
        (("GitHubField", "LinkedInField"), 0.5),
    ]
    latex = lf.latex["LinkedInGitHub"]
    def __init__(self):
        super().__init__(LinkedInGitHub.rules, LinkedInGitHub.latex)

    def to_latex(self):
        if self.has_expanded():
            assert(len(self.children) == 2)
            return self.latex % (self.children[0].to_latex(), self.children[1].to_latex())
        else:
            raise Exception(f"{self} must be expanded first")


class LinkedInField(Nonterminal):
    rules = [
        (("LinkedIn",), 1.0)
    ]
    latex = lf.latex["LinkedInField"]
    def __init__(self):
        super().__init__(LinkedInField.rules, LinkedInField.latex)

    # def to_latex(self):
    #     if self.has_expanded():
    #         values = self.children[0].value
    #         return self.latex % (values["href"], values[str(self.children[0])])
    #     else:
    #         raise Exception(f"{self} must be expanded first")


class GitHubField(Nonterminal):
    rules = [
        (("GitHub",), 1.0)
    ]
    latex = lf.latex["GitHubField"]
    def __init__(self):
        super().__init__(GitHubField.rules, GitHubField.latex)

    # def to_latex(self):
    #     if self.has_expanded():
    #         assert(len(self.children) == 1)
    #         c = self.children[0]
    #         values = c.get()
    #         return self.latex % (values["href"], values[str(c)])
    #     else:
    #         raise Exception(f"{self} must be expanded first")

class GeographicalInfoField(Nonterminal):
    rules = [
        (("GeographicalInfo",), 1.0)
    ]
    latex = lf.latex["GeographicalInfoField"]
    def __init__(self):
        super().__init__(GeographicalInfoField.rules, GeographicalInfoField.latex)

    

class FullName(Terminal):
    # data_factory = NameDataFactory()
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        # self.value = FullName.data_factory.generate(None)
        self.value = "Matthew Chak"
        return self

    # def expand(self, context=None):
    #     """TODO: Replace with name generator module"""
    #     letters = 'abcdefghijklmnopqrstuvwxyz'
    #     fn_length = random.randint(5,10)
    #     ln_length = random.randint(5,15)
    #     self.value = {
    #         "FullName" : "".join(random.choice(letters) for _ in range(fn_length)).capitalize() + " " + \
    #             "".join(random.choice(letters) for _ in range(ln_length)).capitalize()
              
    #     }
    #     return self

class GitHub(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        """TODO: 2 options
        1. replace each field with a call to an info generator
        2. register the class in a central DataFactory that generates the fields once it has ALL instances
        Option 2 is better for interdependent fields.
        """
        # self.value = {
        #     "href" : "https://github.com/iLykTurtlz",
        #     "GitHub" : "iLykTurtlz"
        # }
        self.value = "iLykTurtlz"
        return self
        


class LinkedIn(Terminal):
    """TODO: generate LinkedIn fields in expand"""
    def __init__(self):
        self.value = None
    
    def expand(self, context=None):
        # self.value = {
        #     "href" : "https://www.linkedin.com/in/paul-jarski-a4a04386/",
        #     "LinkedIn" : "paul-jarski-a4a04386"
        # }
        self.value = "dontgohere"
        return self
         
         


class Phone(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        #TODO: make area code statistically representative, NOT all Bay Area
        area_code = [4,1,5]
        last_four = [random.randint(0,9) for _ in range(4)]
        formats = ["({}) 555-{}", "{}-555-{}", "+1 {}-555-{}", "1-{}-555-{}"]
        #TODO: add format weights
        number = random.choice(formats).format("".join(str(num) for num in area_code), "".join(str(num) for num in last_four))
        self.value = number
        return self


class Email(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        # self.value = {"Email" : "pjarski@calpoly.edu"}
        self.value = "pjarski@calpoly.edu"
        return self
    


class GeographicalInfo(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        # """TODO: vary the info string formats"""
        # self.value = {"GeographicalInfo": "San Luis Obispo, CA"}
        self.value = "San Luis Obispo"
        return self