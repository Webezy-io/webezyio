import time
import logging
from webezyio.architect.commands import GetWebezyJson,SaveWebezyJson
from webezyio.architect.recievers import Core
from webezyio.architect.interfaces import IUndoRedo

class CoreInvoker:
    """The Invoker Class"""

    def __init__(self,path):
        logging.debug("Invoker class __init__")
        self._commands = {}
        self._history = [] 
        self._path = path
        self._webezy_json = {}
        
    @property
    def history(self):
            """Return all records in the History list"""
            return self._history

    def register(self, command_name, command):
        """All commands are registered in the Invoker Class"""
        self._commands[command_name] = command

    def execute(self, command_name, *args):
        """Execute a pre defined command and log in history"""
        if command_name in self._commands.keys():
            response = self._commands[command_name].execute(self._path,args)
            self._history.append((time.time(), command_name, args,response))
        else:
            logging.error(f"Command [{command_name}] not recognised")

class Webezy(IUndoRedo):
    def __init__(self,path=None):
        logging.debug("Archi class __init__ | path to project -> {0}".format(path))
        self._core = Core()
        self._core_invoker = CoreInvoker(path)
        self.init_core()
        self._commands = {}
        self._hooks = {}
        self._webezy_json = {}
        self._history_position = 0
        self._get_webezy_json()
        temp_webezy = self._webezy_json.copy()
        self._history = [(temp_webezy, "INIT", (path,))]
        self._unsaved_changes = False

    def init_core(self):
        self._core_invoker.register('GetWebezyJson',GetWebezyJson(self._core))
        self._core_invoker.register('SaveWebezyJson',SaveWebezyJson(self._core))

    def _get_webezy_json(self):
        self._core_invoker.execute('GetWebezyJson')
        self._webezy_json = self._core_invoker.history[-1][-1]

    def registerCommand(self, command_name, command):
        """All commands are registered in the Invoker Class"""
        self._commands[command_name] = command

    def registerHook(self, command_name, hook_name, hook, type='before'):
        """All hooks are registered in the Invoker Class"""
        if self._hooks.get(command_name) is None:
            self._hooks[command_name] = {'before':{},'after':{}}
        
        self._hooks[command_name][type][hook_name] = hook

    def before_execute(self, command_name,*args):
        hook_map = self._hooks.get(command_name)
        if hook_map is not None:
            for hook in hook_map.get('before'):
                logging.debug("Running before hook")
                hook_map['before'][hook].execute('before',command_name,args)

    def after_execute(self, command_name,*args):
        hook_map = self._hooks.get(command_name)
        if hook_map is not None:
            for hook in hook_map.get('after'):
                logging.debug("Running after hook")
                hook_map['after'][hook].execute('after',command_name,args)

    def execute(self, command_name, *args,**kwargs):
        if command_name in self._commands.keys():
            logging.info(f"[EXCUTE] {command_name}")
            if self._history_position != 0 and self._unsaved_changes == False:
                self._get_webezy_json()
            # else:
                # self._webezy_json = self._history[self._history_position][0]
            self._history_position += 1
            self.before_execute(command_name,args)
            self._commands[command_name].execute(self._webezy_json,args,kwargs)
            self.after_execute(command_name,args)
            self._unsaved_changes = True
            if len(self._history) == self._history_position:
                # This is a new event in hisory
                temp = self._webezy_json.copy()
                self._history.append((temp, command_name, args,kwargs))
            else:
                # This occurs if there was one of more UNDOs and then a new
                # execute command happened. In case of UNDO, the history_position
                # changes, and executing new commands purges any history after
                # the current position"""
                self._history = self._history[:self._history_position+1]
                self._history[self._history_position] = {
                    time.time(): [command_name, args]
                }
        else:
            logging.error(f"Command [{command_name}] not recognised")

    def undo(self):
        """Undo a command if there is a command that can be undone.
        Update the history psoition so that further UNDOs or REDOs
        point to the correct index"""
        if self._history_position > 0:
            self._history_position -= 1
            logging.info(f"[UNDO] {self._history_position} / {len(self.history)}")
            self._webezy_json = self.history[self._history_position][0]
            # self._commands[
            #     self._history[self._history_position][1]
            # ].execute(self._history[self._history_position][0],self._history[self._history_position][2])
        else:
            logging.warning("nothing to undo")

    def redo(self):
        """Perform a REDO if the history_position is less than the end of the history list"""
        if self._history_position + 1 < len(self._history):
            self._history_position += 1
            logging.info(f"[REDO] {self._history_position} / {len(self.history)}")
            self._commands[
                self._history[self._history_position][1]
            ].execute(self._history[self._history_position][0],self._history[self._history_position][2])
        else:
            logging.warning("nothing to REDO")

    def save(self,webezyJson=True):
        """Saving current state"""
        current_state = self._webezy_json
        logging.info(f"[SAVE] {current_state}")
        self._unsaved_changes = False
        self._core_invoker.execute('SaveWebezyJson',current_state)

    @property
    def history(self):
        return self._history

    @property
    def commands(self):
        return self._commands

    @property
    def hooks(self):
        return self._hooks

    @property
    def webezyJson(self):
        return self._webezy_json