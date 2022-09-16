from abc import ABCMeta, abstractstaticmethod

class IHook(metaclass=ABCMeta):

    @abstractstaticmethod
    def execute():
        pass