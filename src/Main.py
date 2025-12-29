############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

try:
    import time, sys, os
    from getpass import getpass
    from config.Configuration import Configuration
    from generator.Passwordgenerator import Password
    from generator.Hashgenerator import Hashgenerator
except ImportError as e:
    print(f"[Main] ImportError -> {e}")
    sys.exit(1)

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class Main:
    master_buffer: str | None = None

    @staticmethod
    def generatepassword(context: str, key1: str, key2: str, key3: str, master_key: str) -> str:
        return Password(context,key1,key2,key3,master_key)\
            .process()[:Configuration.get('config','pass_limit')]

    @staticmethod
    def generatehash(bits: int, message: str) -> str:
        return Hashgenerator.gethash(bits, message)

############## ############## ##############
#                CLASS END                 #
############## ############## ##############

if __name__ == '__main__':
    from src.config.Interface import Interface
    Configuration.handle(Interface.MainMenu.main,"Interface:MainMenu:main")
