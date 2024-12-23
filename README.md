# CP-CSC-NPC-CV-Generator

(Cal Poly Computer Science Non-Player Character Curriculum Vitae)

## About

The CP-CSV-NPC-CV-Generator is a React web app that generates a resume representing a fictitious Computer Science student from California Polytechnic State University San Luis Obispo circa 2024.  This happens in a few stages:
* A Probabilistic Context-Free Grammar expands a start nonterminal symbol into a parse tree elaborating the sections, whose leaves are fields in the resume.
* Various datasets are sampled to fill in the personal information and other attributes with data representative of the Cal Poly Computer Science student body.
* An LLM API call generates a self-summary based on all the data available so far.
* A DFS of the parse tree produces a complete LaTeX document, which is compiled with [LaTeX.Online](https://latexonline.cc).

## Dependencies

Python (3.9.20 or later)

### Python packages

Flask (3.1.0) 

Flask-Cors (5.0.0) 

python-dotenv (1.0.1) 

groq (0.13.0) 

Numpy (1.26.2)

Pandas (2.1.3)

NLTK (3.8.1)



### Standard Python libraries

os, uuid, random, json, subprocess

## Execution

To run, cd into the `backend` directory and run `app.py` by typing

```python app.py```

Then open a browser and navigate to `localhost:3000`.


**Note:** Overview generation requires `GROQ_API_KEY` to be present in the OS environment. If it's not present, a random self-summary will be selected
from a list of pre-generated texts.

**Also Note:** The [laton script](https://github.com/aslushnikov/latex-online), provided, needs to have execute permissions enabled if it doesn't already.

