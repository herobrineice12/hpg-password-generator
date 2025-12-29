############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

try:
    import sys, os, time
    from getpass import getpass
    from typing import Any, Literal
    from src.Main import Main
    from src.config.Configuration import Configuration
except ImportError as e:
    print(f"[Interface] ImportError -> {e}")
    sys.exit(1)

############## ############## ##############
#         FUNCTIONALITY DEFINITION         #
############## ############## ##############

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

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class Interface:

    ############## ############## ##############
    #             CLASS DEFINITION             #
    ############## ############## ##############

    class MainMenu:
        @staticmethod
        def main():
            Configuration.clear()
            print(Configuration.get('dialog', 'main', 'selection'))

            buildmenu(
                {
                    # Enter Password Creation Menu
                    Configuration.get('dialog', 'main', 'generate_pass'):
                        lambda: Configuration.handle(Interface.MainMenu.passgen, "Interface:MainMenu:passgen"),
                    # Enter Hash Generation Menu
                    Configuration.get('dialog', 'main', 'generate_hash'):
                        lambda: Configuration.handle(Interface.MainMenu.hashgen, "Interface:MainMenu:hashgen"),
                    # Enter Configuration Menu
                    Configuration.get('dialog', 'main', 'configuration'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.settings, "Main:ConfigurationMenu:settings"),
                    # Exit Application
                    Configuration.get('dialog', 'main', 'exit'):
                        lambda: sys.exit(0)
                },
                start=1
            )

        @staticmethod
        def passgen():
            blank = '\0'
            key_number: int = Configuration.get('config', 'key_number')
            safe_mode: bool = Configuration.get('config', 'safe_mode')

            master_was_none: bool = Main.master_buffer is None

            read = getpass if safe_mode else input

            ask_parameter = lambda \
                key: f"{Configuration.get('dialog', 'main', 'read')} {Configuration.get('dialog', 'password', key)}"

            context: str = read(f"{ask_parameter('context')} --> ")

            key1: str | None = read(f"{ask_parameter('key1')} --> ") \
                if key_number >= 3 else blank

            key2: str | None = read(f"{ask_parameter('key2')} --> ") \
                if key_number >= 4 else blank

            key3: str | None = read(f"{ask_parameter('key3')} --> ") \
                if key_number == 5 else blank

            master_key: str = read(f"{ask_parameter('master_key')} --> ") if Main.master_buffer is None \
                else Main.master_buffer

            password: str = Main.generatepassword(context, key1, key2, key3, master_key)

            print_password = lambda: print(
                f"\n{Configuration.get('dialog', 'main', 'delivery')}\n"
                f"\n{password}\n"
                f"\n{Configuration.get('dialog', 'main', 'length')} {len(password)}\n"
            )

            if safe_mode:
                while True:
                    confirmation = input(
                        f"{Configuration.get('dialog', 'password', 'print_confirmation')}\n"
                        f" --> "
                    )

                    confirmation = True if confirmation in ['y', 's', 'д'] else (
                        False if confirmation in ['n', 'н'] else None)

                    if confirmation:
                        print_password()
                    elif not confirmation:
                        break
                    else:
                        continue

                    break
            else:
                print_password()

            on_docker_envirorement: bool = os.path.exists("/.dockerenv")

            if not on_docker_envirorement:
                Configuration.copy(password)

            if master_was_none:
                Main.master_buffer = None
            elif not master_was_none and not safe_mode:
                print(
                    f"Hash:\n"
                    f"{master_key}\n"
                )

            time.sleep(1.5)
            input(Configuration.get('dialog', 'main', 'continue'))
            raise StopIteration
        
        @staticmethod
        def hashgen():

            ############## ############## ##############
            #            AUXILIARY METHODS             #
            ############## ############## ##############

            def _hashgeneration() -> None:
                calculations = lambda message: int(input(message))

                calc: int = Configuration.call(
                    calculations,
                    "Main:generatehash:_hashgeneration",
                    f"{Configuration.get('dialog', 'hash', 'calculations')}\n --> "
                )

                bit_missflow = 3 > calc or calc > 32

                if bit_missflow:
                    print(Configuration.get('dialog', 'warning', 'bit_missflow'))
                    return

                mess: str = input(
                    f"{Configuration.get('dialog', 'hash', 'message')}\n --> "
                )

                Main.master_buffer = Main.generatehash(bits=calc, message=mess)
                raise StopIteration

            def _clearhash() -> None:
                Main.master_buffer = None

            ############## ############## ##############
            #           METHOD FUNCTIONALITY           #
            ############## ############## ##############

            Configuration.clear()

            print(Configuration.get('dialog', 'hash', 'confirmation'))

            buildmenu(
                {
                    None:
                        lambda: Configuration.save_and_exit(),

                    Configuration.get('dialog', 'main', 'yes'):
                        lambda: Configuration.handle(_hashgeneration, "Main:generatehash:_hashgeneration"),

                    Configuration.get('dialog', 'main', 'no'):
                        lambda: Configuration.throw(StopIteration),

                    Configuration.get('dialog', 'hash', 'clear'):
                        lambda: _clearhash()
                }
            )

    class ConfigurationMenu:
        @staticmethod
        def settings() -> None:
            Configuration.clear()
            print(Configuration.get('dialog', 'configuration', 'menu', 'main'))

            buildmenu(
                {
                    # Go Back To The Main Menu
                    Configuration.get('dialog', 'main', 'back'):
                        lambda: Configuration.throw(StopIteration),
                    # Safe Mode Configuration
                    Configuration.get('dialog', 'configuration', 'safe', 'safe_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.safeset, "Interface:ConfigurationMenu:safeset"),
                    # Key Quantity Configuration
                    Configuration.get('dialog', 'configuration', 'key', 'key_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.keyset, "Interface:ConfigurationMenu:keyset"),
                    # Base Type Configuration
                    Configuration.get('dialog', 'configuration', 'base', 'base_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.baseset, "Interface:ConfigurationMenu:baseset"),
                    # Password Length Configuration
                    Configuration.get('dialog', 'configuration', 'limit', 'limit_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.limitset, "Interface:ConfigurationMenu:limitset"),
                    # Language Preference Configuration
                    Configuration.get('dialog', 'configuration', 'language', 'language_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.langset, "Interface:ConfigurationMenu:langset"),
                    # Algorithm Related Configuration
                    Configuration.get('dialog', 'configuration', 'algorithm', 'algorithm_setting'):
                        lambda: Configuration.handle(Interface.ConfigurationMenu.algoset, "Interface:ConfigurationMenu:algoset"),
                    # Exit Application
                    Configuration.get('dialog', 'main', 'exit'):
                        lambda: sys.exit(0)
                }
            )
        
        @staticmethod
        def safeset():
            Configuration.clear()
            print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                  Configuration.get('config', 'safe_mode'))

            print(Configuration.get('dialog', 'configuration', 'safe', 'set_safe'))
            buildmenu(
                {
                    None: lambda: Configuration.save_and_exit(),
                    Configuration.get('dialog', 'main', 'yes'): lambda: Configuration.setsafe(True),
                    Configuration.get('dialog', 'main', 'no'): lambda: Configuration.setsafe(False)
                }
            )
            
        @staticmethod
        def keyset():
            Configuration.clear()
            print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                  Configuration.get('config', 'key_number'))
            print(Configuration.get('dialog', 'configuration', 'key', 'set_key'))
            choice: int = int(
                input(" --> ")
            )

            match choice:
                case 0:
                    Configuration.save_and_exit()
                case _ if choice in range(2, 6):
                    Configuration.setkeys(choice)
                case _:
                    raise ValueError
                
        @staticmethod
        def baseset():
            Configuration.clear()
            print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                  Configuration.get('config', 'pref_base'))
            print(Configuration.get('dialog', 'configuration', 'base', 'set_base'))

            buildmenu(
                {
                    None: lambda: Configuration.save_and_exit(),
                    "Base85": lambda: Configuration.setbase('b85'),
                    "Base64": lambda: Configuration.setbase('b64'),
                    "Base64url": lambda: Configuration.setbase('b64u'),
                    "Base16": lambda: Configuration.setbase('b16')
                }
            )
            
        @staticmethod
        def limitset():
            Configuration.clear()
            print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                  Configuration.get('config', 'pass_limit'))
            print(Configuration.get('dialog', 'configuration', 'limit', 'set_limit'))
            choice: int = int(
                input(" --> ")
            )

            match choice:
                case 0:
                    Configuration.save_and_exit()
                case _ if choice in range(1, 257):
                    Configuration.setlimit(choice)
                case _:
                    raise ValueError
                
        @staticmethod
        def langset():
            Configuration.clear()

            print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                  Configuration.get('config', 'pref_lang'))
            print(Configuration.get('dialog', 'configuration', 'language', 'set_language'))

            buildmenu(
                {
                    None: lambda: Configuration.save_and_exit(),
                    Configuration.get('dialog', 'configuration', 'language', 'english'):
                        lambda: Configuration.setlang('eng'),
                    Configuration.get('dialog', 'configuration', 'language', 'portuguese'):
                        lambda: Configuration.setlang('pt-br'),
                    Configuration.get('dialog', 'configuration', 'language', 'russian'):
                        lambda: Configuration.setlang('rus')
                }
            )
            
        @staticmethod
        def algoset():
            ############## ############## ##############
            #            AUXILIARY METHODS             #
            ############## ############## ##############

            def _modifyalgorithms(algo: Literal['key_hasher', 'pass_hasher'], menu: dict):
                Configuration.clear()

                set_hasher = 'set_key' if algo == 'key_hasher' else ('set_hash' if algo == 'pass_hasher' else None)

                print(Configuration.get('dialog', 'configuration', 'menu', 'current'),
                      Configuration.get('config', 'algorithm', algo))
                print(Configuration.get('dialog', 'configuration', 'algorithm', set_hasher))

                buildmenu(
                    menu
                )

            ############## ############## ##############
            #           METHOD FUNCTIONALITY           #
            ############## ############## ##############

            while True:
                Configuration.clear()

                hashes = [
                    Configuration.get('config', 'algorithm', 'key_hasher'),
                    Configuration.get('config', 'algorithm', 'pass_hasher')
                ]

                print(Configuration.get('dialog', 'configuration', 'menu', 'current'), hashes)
                print(Configuration.get('dialog', 'configuration', 'algorithm', 'menu'))
                buildmenu(
                    {
                        None:
                            lambda: Configuration.save_and_exit(),

                        Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'keys_algo'):
                            lambda: Configuration.handle(
                                _modifyalgorithms,
                                "Interface:ConfigurationMenu:algoset:_modifyalgorithms",
                                'key_hasher',
                                {
                                    None: lambda: Configuration.save_and_exit(),
                                    "Blake2b": lambda: Configuration.setalgorithms('key_hasher','blake'),
                                    "HMAC": lambda: Configuration.setalgorithms('key_hasher', 'hmac'),
                                    "Argon2": lambda: Configuration.setalgorithms('key_hasher', 'argon')
                                }
                            ),

                        Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'pass_algo'):
                            lambda: Configuration.handle(
                                _modifyalgorithms,
                                "Interface:ConfigurationMenu:setalgo:_modifyalgorithms",
                                'pass_hasher',
                                {
                                    None: lambda: Configuration.save_and_exit(),
                                    "Argon2": lambda: Configuration.setalgorithms('pass_hasher', 'argon'),
                                    "Bcrypt": lambda: Configuration.setalgorithms('pass_hasher', 'bcrypt'),
                                    "Scrypt": lambda: Configuration.setalgorithms('pass_hasher', 'scrypt')
                                }
                            ),

                        Configuration.get('dialog', 'main', 'edit'):
                            lambda: Configuration.handle(Interface.ConfigurationMenu.parmset, "Interface:ConfigurationMenu:parmset")
                    },
                    start=0
                )
        
        @staticmethod
        def parmset():

            ############## ############## ##############
            #            AUXILIARY METHODS             #
            ############## ############## ##############

            def _listparameters(algo_type: Literal['key_hasher', 'pass_hasher']) -> None:
                hasher: str = Configuration.get('config', 'algorithm', algo_type)
                param: dict = Configuration.get('config', 'algorithm', 'parameters', algo_type, hasher)
                parameters: list = list(param.keys())

                attribute: str = getfromparameters(parameters)

                current_value = Configuration.get('config', 'algorithm', 'parameters', algo_type, hasher, attribute)

                value = Configuration.call(
                    _modifyparameters,
                    "Interface:ConfigurationMenu:parmset:_modifyparameters",
                    attribute,
                    current_value
                )

                if value is not None:
                    Configuration.setparameters(algo_type, hasher, attribute, value=value)

            def _modifyparameters(attribute: str, current_value: Any):
                vartype = type(current_value)

                print(f"{Configuration.get('dialog', 'configuration', 'menu', 'current')} {current_value}")
                print(f"{Configuration.get('dialog', 'main', 'read')}{attribute}")
                raw_value = input(" --> ")

                if raw_value == "0": raise StopIteration

                return vartype(raw_value)

            ############## ############## ##############
            #           METHOD FUNCTIONALITY           #
            ############## ############## ##############

            Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'set_algo_parameters')

            buildmenu(
                {
                    None:
                        lambda: Configuration.save_and_exit(),
                    Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'key_hasher'):
                        lambda: Configuration.handle(_listparameters, "Interface:ConfigurationMenu:parmset:_listparameters","key_hasher"),
                    Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'pass_hasher'):
                        lambda: Configuration.handle(_listparameters, "Interface:ConfigurationMenu:parmset:_listparameters","pass_hasher")
                }
            )