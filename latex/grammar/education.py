from grammar.terminal import Terminal
import random

class CalPoly(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        self.value = "California Polytechnic State University, San Luis Obispo"
        return self
class EduInstitution(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        self.value = "Some Other Institution"
        return self

# field?
class EduGeographicalInfo(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        """TODO: vary the info string formats"""
        self.value = "San Luis Obispo, CA"
        return self
    

class CalPolyEduGeographicalInfo(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        """TODO: vary the info string formats"""
        self.value = "San Luis Obispo, CA"
        return self

# TODO: Are these the same? What is htis??  
class EduGeographicalInfoField(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        """TODO: vary the info string formats"""
        self.value = "San Luis Obispo, CA"
        return self


class EduDegreeName(Terminal):
    """TODO: generate DegreeName fields in expand"""
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        self.value = "B.S."
        return self


class EduDate(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        month = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        year = random.randint(2017, 2024)
        date = " ".join([month, str(year)])
        self.value = date
        return self

class EduGPA(Terminal):
    def __init__(self):
        self.value = None

    def expand(self, context=None):
        fourscale = 4.0
        gpa = random.uniform(0.0, 4.0)
        formats = "{}/{}"
        number = formats.format(str(round(gpa, 1)), str(fourscale))
        self.value = number
        return self
