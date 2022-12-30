# TODO add unit tests for all CLI and core modules
from webezyio.commons.helpers import Graph
from webezyio.cli.prompter import QCheckbox, QConfirm, QText, ask_user_question,QList,inquirer_errors
def test_architect():
    pass

def test_builder():
    pass

def test_cli():
    pass

def test_prompter():
    list = QList('test_list','Some test user input from list',[('Display 1','value1'),('Display 2','value2')])
    text = QText('test_text','Some test user input from text',default='test')
    confirm = QConfirm('test_confirm','Some test user input from confirm',default=True)
    checkbox = QCheckbox('test_checkbox','Some test user input from checkbox',choices=[('Display 1','value1'),('Display 2','value2')],color='danger')
    list_ignore = QList('test_list_ignore','Some test user input from list that should be ignored',choices=[('Display 1','value1'),('Display 2','value2')],ignore=lambda x: x["test_confirm"])
    # text_validate = QText('test_text_validation','Some test user input from text with validation',validate_yes_value)
    
    print(ask_user_question(questions=[list,text,confirm,checkbox,list_ignore]))


def validate_yes_value(answers,current):
    if 'yes' not in current:
      raise inquirer_errors.ValidationError('', reason='Sorry, not have "yes" in user input.')
    return True

def test_topological_sort():

    test_msgs = [
        {"fullName": "a","fields":[{"messageType":"b"},{"messageType":"c"}]},
        {"fullName": "b","fields":[{"messageType":"e"}]},
        {"fullName": "c","fields":[{"messageType":"d"}]},
        {"fullName": "d","fields":[]},
        {"fullName": "e","fields":[{"messageType":"g"}]},
        {"fullName": "f","fields":[{"messageType":'h'}]},
        {"fullName": "g","fields":[]},
        {"fullName": "h","fields":[{"messageType":'a'}]}
    ]

    nodes = []

    g = Graph(test_msgs)
    # for m in test_msgs:
    #     list_of_msgs = []
    #     for f in m.get('fields'):
    #         if f.get('messageType') is not None:
    #             list_of_msgs.append(f.get('messageType'))
        
    #     if len(list_of_msgs) > 0:
    #         for msg in list_of_msgs:
    #             g.addEdge(m.get('fullName'),msg)
    #     else:
    #         g.addEdge(m.get('fullName'),None)

    # for msg in test_msgs:
    #     if msg.get('fullName') not in list(map(lambda n: n.get('fullName'),nodes)):
    #         nodes.append(msg)
    #     for msgT in [m for m in msg.get('fields') if m.get('messageType') is not None and m.get('messageType') not in list(map(lambda n: n.get('fullName'),nodes))]:
    #         nodes.append(next((m for m in test_msgs if m.get('fullName') == msgT.get('messageType')),None))

    # g = Graph()
    # for n in nodes:
    #     addedNode = False
    #     for f in [tf for tf in n.get('fields') if tf.get('messageType') is not None]:
    #         print(n.get('fullName'),'->',f.get('messageType'))
    #         addedNode = True
    #         g.addEdge(n.get('fullName'),f.get('messageType'))
    #     if addedNode == False:
    #         print('Added node',n.get('fullName'))
    #         g.addEdge(n.get('fullName'),None)
    #     for f in msg.get('fields'):
    #     g.addEdge(msg.get('fullName'),)
    print(g.topologicalSort())

if __name__ == '__main__':

    test_topological_sort()

