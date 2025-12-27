############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

try:
    import sys, os, time, shutil
    from typing import Callable, Any, Literal
    from config.Interface import Interface
except Exception as e:
    print(f"Exception -> {e}")
    sys.exit(1)

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class _System:
    import subprocess, json, pyperclip

    CFG: dict = {}
    DLG: dict = {}
    RNT: dict = {}

    CONF_PATH: str

    @staticmethod
    def initialize():
        _System.CFG = _System.load("src/data/preferences.json")
        _System.DLG = _System.load("src/data/dialog.json")

    @staticmethod
    def save() -> None:
        with open(_System.CONF_PATH,'w') as file:
            _System.json.dump(_System.CFG,file,indent=4)

    @staticmethod
    def saveandexit() -> None:
        _System.save()
        raise StopIteration

    @staticmethod
    def load(path: str) -> dict:
        try:
            is_packaged: bool = getattr(sys,'frozen',False)
            is_preference: bool = "preferences" in path

            def load_file(file_location):
                with open(file_location,'r') as file: return _System.json.load(file)

            if is_packaged:
                base_path = sys._MEIPASS

                if is_preference:
                    pref = "preferences.json"
                    file_path: str = os.path.abspath(__file__)
                    local_pref: str = os.path.join(file_path,pref)

                    portable_doesnt_exist: bool = not os.path.exists(local_pref)

                    if portable_doesnt_exist:
                        shutil.copy(os.path.join(base_path,path),file_path)
                        _System.CONF_PATH = local_pref

                    return load_file(local_pref)

                file_path = os.path.join(base_path,path)
                return load_file(file_path)

            if is_preference:
                _System.CONF_PATH = path

            return load_file(path)

        except FileNotFoundError as e:
            print(f"{e} not found")
            sys.exit(1)

        except _System.json.JSONDecodeError:
            print("Decoding error on json")
            sys.exit(1)

    @staticmethod
    def clear() -> None:
        _System.subprocess.call('clear')

    @staticmethod
    def copy(string: str) -> None:
        is_termux = os.path.isdir('/storage/emulated/0/')

        if is_termux:
            _System.subprocess.run(['termux-clipboard-set'],input=string.encode(),check=True)
        else:
            _System.pyperclip.copy(string)

    @staticmethod
    def throw(error) -> None:
        raise error

    @staticmethod
    def handle(func: Callable, identificator: str ='', *args: Any, **kwargs: Any) -> None:
        while True:
            try:
                func(*args,**kwargs)

            except StopIteration:
                break

            except ValueError:
                print(f"[{identificator}] ValueError -> {Configuration.get('dialog', 'error', 'value_error')}")
                time.sleep(3)

            except AttributeError as e:
                print(f"[{identificator}] AttributeError -> {Configuration.get('dialog','error','attribute_error')} {e}")
                time.sleep(3)
                sys.exit(1)

            except KeyboardInterrupt:
                print(Configuration.get('dialog','warning','program_finalized'))
                time.sleep(3)
                sys.exit(0)

            except SystemError as e:
                print(f"[{identificator}] SystemError -> {e}")
                time.sleep(5)
                sys.exit(1)

    @staticmethod
    def call(func: Callable[...,Any], identificator: str = '', *args: Any, **kwargs: Any) -> Any:
        while True:
            try:
                return func(*args, **kwargs)

            except StopIteration:
                break

            except ValueError as e:
                print(f"[{identificator}] ValueError -> {Configuration.get('dialog', 'error', 'value_error')}")
                time.sleep(3)

            except AttributeError as e:
                print(f"[{identificator}] AttributeError -> {Configuration.get('dialog','error','attribute_error')} {e}")
                time.sleep(3)
                sys.exit(1)

            except KeyboardInterrupt:
                print(Configuration.get('dialog', 'warning', 'program_finalized'))
                time.sleep(1)
                sys.exit(0)

            except SystemError as e:
                print(f"[{identificator}] SystemError -> {e}")
                time.sleep(5)
                sys.exit(1)

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class Configuration:

    ############## ############## ##############
    #             WRAPPER VARIABLES            #
    ############## ############## ##############

    save_and_exit: None = lambda: _System.saveandexit()

    clear: None = lambda: _System.clear()
    copy: None = lambda s: _System.copy(s)

    throw: None = lambda ex: _System.throw(ex)

    getlang: Callable[[],str] = lambda: _System.CFG['config']['pref_lang']

    ############## ############## ##############
    #              CLASS METHODS               #
    ############## ############## ##############

    @staticmethod
    def handle(function: Callable, identificator: str, *args, **kwargs) -> None:
        _System.handle(function,identificator,*args,**kwargs)

    @staticmethod
    def call(function: Callable, identificator: str, *args, **kwargs) -> Any:
        return _System.call(function,identificator,*args,**kwargs)

    @staticmethod
    def get(*args: str) -> Any:
        try:
            import base64

            is_dialog: bool = 'dialog' in args
            is_runtime: bool = 'runtime' in args

            if is_dialog:
                information: Any = _System.DLG
            elif is_runtime:
                information: Any = _System.RNT
            else:
                information: Any = _System.CFG

                if 'pref_base' and 'decoder' in args:
                    for item in args[:-1]:
                        information = information[item]

                    match information:
                        case 'b85':
                            return lambda s: base64.b85encode(s).decode()
                        case 'b64u':
                            return lambda s: base64.urlsafe_b64encode(s).decode()
                        case 'b64':
                            return lambda s: base64.b64encode(s).decode()
                        case 'b16':
                            return lambda s: base64.b16encode(s).decode()
                        case _:
                            raise KeyError(f"{Configuration.get('dialog', 'error', 'selection_error')} {information}")

            for item in args:
                information = information[item]

            if is_dialog:
                return information[Configuration.getlang()]

            return information
        except KeyError as e:
            print(f"KeyError -> {Configuration.get('dialog','error','key_error')} {e}")
            time.sleep(10)

    @staticmethod
    def set(*path: str, value: Any) -> None:
        setting: dict

        if 'config' in path:
            setting = _System.CFG['config']

            for item in path[:-1]:
                setting = setting.setdefault(item, {})

            setting[path[-1]] = value
        elif 'runtime' in path:
            setting = _System.RNT['runtime']

            for item in path[:-1]:
                setting = setting.setdefault(item, {})

            setting[path[-1]] = value

    @staticmethod
    def setsafe() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','safe_mode'))

            print(Configuration.get('dialog','configuration','safe','set_safe'))
            Interface.buildmenu(
                {
                    None: lambda: _System.saveandexit(),
                    Configuration.get('dialog','main','yes'): lambda: Configuration.set('config','safe_mode',value=True),
                    Configuration.get('dialog','main','no'): lambda: Configuration.set('config','safe_mode',value=False)
                }
            )

    @staticmethod
    def setkeys() -> None:
        Configuration.clear()
        print(Configuration.get('dialog','configuration','menu','current'),
              Configuration.get('config','key_number'))
        print(Configuration.get('dialog','configuration','key','set_key'))
        choice: int = int(
            input(" --> ")
        )

        match choice:
            case  0:
                _System.saveandexit()
            case _ if choice in range(2,6):
                Configuration.set('config','key_number',value=choice)
            case _:
                raise ValueError

    @staticmethod
    def setbase() -> None:
        Configuration.clear()
        print(Configuration.get('dialog','configuration','menu','current'),
              Configuration.get('config','pref_base'))
        print(Configuration.get('dialog','configuration','base','set_base'))

        Interface.buildmenu(
            {
                None: lambda: _System.saveandexit(),
                "Base85": lambda: Configuration.set('config','pref_base',value='b85'),
                "Base64": lambda: Configuration.set('config','pref_base',value='b64'),
                "Base64url": lambda: Configuration.set('config','pref_base',value='b64u'),
                "Base16": lambda: Configuration.set('config','pref_base',value='b16')
            }
        )

    @staticmethod
    def setlimit() -> None:
        Configuration.clear()
        print(Configuration.get('dialog','configuration','menu','current'),
              Configuration.get('config','pass_limit'))
        print(Configuration.get('dialog','configuration','limit','set_limit'))
        choice: int = int(
            input(" --> ")
        )

        match choice:
            case 0:
                _System.saveandexit()
            case _ if choice in range(1,257):
                Configuration.set('config','pass_limit',value=choice)
            case _:
                raise ValueError

    @staticmethod
    def setlang() -> None:
        Configuration.clear()

        print(Configuration.get('dialog','configuration','menu','current'),
              Configuration.get('config','pref_lang'))
        print(Configuration.get('dialog','configuration','language','set_language'))

        Interface.buildmenu(
            {
                None: lambda: _System.saveandexit(),
                Configuration.get('dialog','configuration','language','english'): lambda: Configuration.set('config','pref_lang',value='eng'),
                Configuration.get('dialog','configuration','language','portuguese'): lambda: Configuration.set('config','pref_lang',value='pt-br'),
                Configuration.get('dialog','configuration','language','russian'): lambda: Configuration.set('config','pref_lang',value='rus')
            }
        )

    @staticmethod
    def setalgorithms() -> None:
        
        ############## ############## ##############
        #            AUXILIARY METHODS             #
        ############## ############## ##############

        def _modifyalgorithms(algo: Literal['key_hasher','pass_hasher'], menu: dict):
            Configuration.clear()

            set_hasher = 'set_key' if algo == 'key_hasher' else ('set_hash' if algo == 'pass_hasher' else None)

            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','algorithm',algo))
            print(Configuration.get('dialog','configuration','algorithm',set_hasher))

            Interface.buildmenu(
                menu
            )

        ############## ############## ##############
        #           METHOD FUNCTIONALITY           #
        ############## ############## ##############

        while True:
            Configuration.clear()

            hashes = [
                Configuration.get('config','algorithm','key_hasher'),
                Configuration.get('config','algorithm','pass_hasher')
            ]

            print(Configuration.get('dialog','configuration','menu','current'),hashes)
            print(Configuration.get('dialog','configuration','algorithm','menu'))
            Interface.buildmenu(
                {
                    None:
                        lambda: Configuration.save_and_exit(),

                    Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'keys_algo'):
                        lambda: _System.handle(
                            _modifyalgorithms,
                            "Configuration:setalgo:_modifyalgorithms",
                            'key_hasher',
                            {
                                None: lambda: Configuration.save_and_exit(),
                                "Blake2b": lambda: Configuration.set('config','algorithm','key_hasher',value='blake'),
                                "HMAC": lambda: Configuration.set('config','algorithm','key_hasher',value='hmac'),
                                "Argon2": lambda: Configuration.set('config','algorithm','key_hasher',value='argon')
                            }
                        ),

                    Configuration.get('dialog', 'configuration', 'algorithm_parameters', 'pass_algo'):
                        lambda: _System.handle(
                            _modifyalgorithms,
                            "Configuration:setalgo:_modifyalgorithms",
                            'pass_hasher',
                            {
                                None: lambda: Configuration.save_and_exit(),
                                "Argon2": lambda: Configuration.set('config','algorithm', 'pass_hasher', value='argon'),
                                "Bcrypt": lambda: Configuration.set('config','algorithm', 'pass_hasher', value='bcrypt'),
                                "Scrypt": lambda: Configuration.set('config','algorithm', 'pass_hasher', value='scrypt')
                            }
                        ),

                    Configuration.get('dialog', 'main', 'edit'):
                        lambda: Configuration.handle(Configuration.setparameters,"Configuration:setparameters")
                },
                start=0
            )


    @staticmethod
    def setparameters() -> None:

        ############## ############## ##############
        #            AUXILIARY METHODS             #
        ############## ############## ##############
        
        def _listparameters(algo_type: Literal['key_hasher','pass_hasher']) -> None:
            hasher: str = Configuration.get('config','algorithm',algo_type)
            param: dict = Configuration.get('config','algorithm','parameters',algo_type,hasher)
            parameters: list = list(param.keys())

            attribute: str = Interface.getfromparameters(parameters)

            current_value = Configuration.get('config','algorithm','parameters',algo_type,hasher,attribute)

            value = _System.call(
                _modifyparameters,
                "Configuration:setparameters:_modifyparameters",
                attribute,
                current_value
            )

            if value is not None:
                Configuration.set('config','algorithm','parameters',algo_type,hasher,attribute,value=value)

        def _modifyparameters(attribute: str, current_value: Any):
            vartype = type(current_value)

            print(f"{Configuration.get('dialog','configuration','menu','current')} {current_value}")
            print(f"{Configuration.get('dialog','main','read')}{attribute}")
            raw_value = input(" --> ")

            if raw_value == "0": raise StopIteration

            return vartype(raw_value)

        ############## ############## ##############
        #           METHOD FUNCTIONALITY           #
        ############## ############## ##############

        Configuration.get('dialog','configuration','algorithm_parameters','set_algo_parameters')

        Interface.buildmenu(
            {
                None:
                    lambda: _System.saveandexit(),

                Configuration.get('dialog','configuration','algorithm_parameters','key_hasher'):
                    lambda: Configuration.handle(_listparameters,"Configuration:setparameters:_listparameters","key_hasher"),

                Configuration.get('dialog','configuration','algorithm_parameters','pass_hasher'):
                    lambda: Configuration.handle(_listparameters,"Configuration:setparameters:_listparameters","pass_hasher")
            }
        )

############## ############## ##############
#                CLASS END                 #
############## ############## ##############

# Load files when imported
_System.initialize()