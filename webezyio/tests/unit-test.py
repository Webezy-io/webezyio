# TODO add unit tests for all CLI and core modules
from webezyio.cli.prompter import QConfirm, QText, ask_user_question,QList,inquirer_errors
def test_architect():
    pass

def test_builder():
    pass

def test_cli():
    pass

def test_prompter():
    list = QList('test_list','Some test user input from list',[('Display 1','value1'),('Display 2','value2')])
    text = QText('test_text','Some test user input from text')
    confirm = QConfirm('test_confirm','Some test user input from confirm',default=True)
    text_validate = QText('test_text_validation','Some test user input from text with validation',validate_yes_value)
    
    print(ask_user_question(questions=[list,text,confirm,text_validate]))

def validate_yes_value(answers,current):
    if 'yes' not in current:
      raise inquirer_errors.ValidationError('', reason='Sorry, not have "yes" in user input.')
    return True

if __name__ == '__main__':

    test_prompter()