import pandas as pd
import numpy as np
import re
import ftfy
import emoji

def clean_text(text):
    """
    Cleans special characters, emojis, and non-alphanumerics
    while keeping code and math formulas intact.
    """
    if not isinstance(text, str):
        return text
    
    text = ftfy.fix_text(text)  # Fix encoding issues
    
    # Preserve code blocks and formulas
    code_snippets = re.findall(r"```.*?```", text, re.DOTALL)
    for i, snippet in enumerate(code_snippets):
        text = text.replace(snippet, f"[CODE_SNIPPET_{i}]")
    
   # Preserve LaTeX formulas
    latex_formulas = re.findall(r"\$.*?\$", text, re.DOTALL)  # Inline LaTeX
    for i, formula in enumerate(latex_formulas):
        text = text.replace(formula, f"[LATEX_FORMULA_{i}]")

    latex_display_formulas =  re.findall(r"\$\$.*?\$\$", text, re.DOTALL)  # Display LaTeX
    for i, formula in enumerate(latex_display_formulas):
        text = text.replace(formula, f"[LATEX_DISPLAY_FORMULA_{i}]")

    # Remove emojis and replace them with their description
    text = emoji.demojize(text, language='en') #call before you remove characters

    # Remove non-alphanumeric characters (except math symbols and programming characters)
    text = re.sub(r"[^\w\s\.,;:{}\(\)\[\]<>#@%+\-*/=\'\"!|]", "", text)   
    # Restore LaTeX formulas
    for i, formula in enumerate(latex_formulas):
        text = text.replace(f"[LATEX_FORMULA_{i}]", formula)

    for i, formula in enumerate(latex_display_formulas):
        text = text.replace(f"[LATEX_DISPLAY_FORMULA_{i}]", formula)

    # Restore code snippets
    for i, snippet in enumerate(code_snippets):
        text = text.replace(f"[CODE_SNIPPET_{i}]", snippet)
    
    return text
