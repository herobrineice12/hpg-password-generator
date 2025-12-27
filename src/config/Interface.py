############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

from typing import Any

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class Interface:
    @staticmethod
    def buildmenu(menu: dict, start: int = 0) -> None:
        items = list(menu.keys())

        for i, label in enumerate(items,start):
            if label is None:
                continue
            print(f"({i}) {label}")
        else:
            choice = int(input(" --> "))

        index = choice - start
        selected_item = items[index]

        option = menu[selected_item]
        option()

    @staticmethod
    def getfromparameters(parameters: list) -> Any:
        items: list = [None] + parameters

        for i, parameter in enumerate(items):
            if parameter is None:
                continue
            print(f"({i}) {parameter}")
        else:
            choice = int(input(" --> "))

        if choice == 0: raise StopIteration

        selected_item = items[choice]

        return selected_item