from grammar.nonterminal import Nonterminal
import latex_formats as lf
from collections import ChainMap


class Body(Nonterminal):
    rules = [
        #(("Education", "ExperienceSection"), 1.0)
        (("EducationSection", "ExperienceSection", "ProjectSection"), 1.0)
        # (("EducationSection",), 1.0)
    ]
    latex = lf.latex["Body"]

    def __init__(self):
        super().__init__(Body.rules, Body.latex)

    def expand(self, context=None):
        context = context or {}
        

class EducationSection(Nonterminal):
    rules = [
        (("CalPolyEducation",), 0.5),
        (("CalPolyEducation", "Education"), 0.5)
    ]
    latex = lf.latex["EducationSection"]

    def __init__(self):
        super().__init__(EducationSection.rules, EducationSection.latex)

class CalPolyEducation(Nonterminal):
    rules = [
        (("CalPoly", "CalPolyEduGeographicalInfo", "EduDegreeName", "EduDate", "EduGPA"), 1.0)
    ]
    latex = lf.latex["Education"]

    def __init__(self):
        super().__init__(CalPolyEducation.rules, CalPolyEducation.latex)
    def to_latex(self):
        if self.has_expanded():
            return self.latex % tuple(child.to_latex() for child in self.children)
        else:
            raise Exception(f"{self} must be expanded first")

class Education(Nonterminal):
    rules = [
        (("EduInstitution", "EduGeographicalInfo", "EduDegreeName", "EduDate", "EduGPA"), 1.0)
    ]
    latex = lf.latex["Education"]

    def __init__(self):
        super().__init__(Education.rules, Education.latex)

    def to_latex(self):
        if self.has_expanded():
            return self.latex % tuple(child.to_latex() for child in self.children)
        else:
            raise Exception(f"{self} must be expanded first")

