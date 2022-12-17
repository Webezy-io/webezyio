# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# A prompting module for all webezy.io cli prompting tasks

from typing import Any, List, Literal, Tuple
from collections.abc import Callable

import inquirer
from inquirer import errors as inquirer_errors

from webezyio.cli.theme import WebezyTheme

user_prompt_type = Literal["Confirm","List","Text","Checkbox"]


class QList:
    
    def __init__(self, name:str, message:str, choices,validate=None) -> None:
        self.name = name
        self.message = message
        self.choices = choices
        self.validate = validate if validate is not None else True

    def add_choice(self,choice:Tuple[str,str]):
        self.choices.append(choice)

class QConfirm:
    
    def __init__(self, name:str, message:str, default:bool, validate=None) -> None:
        self.name = name
        self.message = message
        self.default = default
        self.validate = validate if validate is not None else True

class QText:

    def __init__(self, name:str, message:str, validate=None) -> None:
        self.name = name
        self.message = message
        self.validate = validate if validate is not None else True

class QCheckbox:

    def __init__(self, name:str, message:str, choices, validate=None) -> None:
        self.name = name
        self.message = message
        self.choices = choices
        self.validate = validate if validate is not None else True

    def add_choice(self,choice:Tuple[str,str]):
        self.choices.append(choice)


def ask_user_question(questions):
    """
    A function to prompt user input questions
    
    Parameters:
    -----------
        question_type: The prompt type see https://python-inquirer.readthedocs.io/en/latest/usage.html#question-types
        questions: List of questions tuples that consist of : 
            * `name` - The answer name see: https://python-inquirer.readthedocs.io/en/latest/usage.html#name
            * `message` - The user prompt message see: https://python-inquirer.readthedocs.io/en/latest/usage.html#message
            * `ignore` - Optional callback function that gets `answers` where answers contains the dict of previous
                answers again and returns a boolean value if to ignore urrent question see: https://python-inquirer.readthedocs.io/en/latest/usage.html#ignore
            * `validate` - Optional attribute that allows the program to check if the answer is valid or not see: https://python-inquirer.readthedocs.io/en/latest/usage.html#validate
    """

    questions_temp = []
    for q in questions:
        dict_obj = vars(q)
        if q.__class__.__name__ == 'QList':
            questions_temp.append(
                inquirer.List(
                    dict_obj.get('name'),
                    message=dict_obj.get('message'),
                    choices=dict_obj.get('choices'),
                    ignore=dict_obj.get('ignore'),
                    validate=dict_obj.get('validate')
                )
            )
        elif q.__class__.__name__ == 'QCheckbox':
            questions_temp.append(
                inquirer.Checkbox(
                    dict_obj.get('name'),
                    message=dict_obj.get('message'),
                    choices=dict_obj.get('choices'),
                    ignore=dict_obj.get('ignore'),
                    validate=dict_obj.get('validate')
                )
            )
        elif q.__class__.__name__ == 'QText':
            questions_temp.append(
                inquirer.Text(
                    dict_obj.get('name'),
                    message=dict_obj.get('message'),
                    ignore=dict_obj.get('ignore'),
                    validate=dict_obj.get('validate')
                )
            )
        elif q.__class__.__name__ == 'QConfirm':
            questions_temp.append(
                inquirer.Confirm(
                    dict_obj.get('name'),
                    message=dict_obj.get('message'),
                    default=dict_obj.get('default'),
                    ignore=dict_obj.get('ignore'),
                    validate=dict_obj.get('validate')
                )
            )
    return inquirer.prompt(questions_temp,theme=WebezyTheme())
