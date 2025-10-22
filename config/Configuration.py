# Import Area
try:
    import sys, os, time
    from typing import Callable, Any, Literal
except Exception as e:
    print(f"Exception -> {e}")
    sys.exit(1)

class _System:
    import subprocess, json, pyperclip

    CFG: dict = {}
    path: str

    @staticmethod
    def save() -> None:
        with open(_System.path,'w') as file:
            _System.json.dump(_System.CFG,file,indent=4)

    @staticmethod
    def load(path="config/config.json"):
        try:
            _System.path = path

            if getattr(sys, 'frozen', False):
                base_path: str = getattr(sys, '_MEIPASS', sys.path[0])
                _System.path = os.path.join(base_path, _System.path)

            with open(_System.path, 'r') as file:
                _System.CFG = _System.json.load(file)

        except FileNotFoundError:
            print("config.json not found at " + _System.path)
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
            _System.subprocess.run(
                ['termux-clipboard-set'],
                input=string.encode(),
                check=True
           )
        else:
            _System.pyperclip.copy(string)

class Configuration:
    clear = lambda: _System.clear()
    copy = lambda string: _System.copy(string)

    getlang: Callable[[],str] = lambda: _System.CFG['config']['pref_lang']

    @staticmethod
    def get(*args: str) -> Any:
        try:
            import base64

            message: Any = _System.CFG

            if 'pref_base' and 'decoder' in args:
                for item in args[:-1]:
                    message = message[item]

                match message:
                    case 'b85':
                        return lambda s: base64.b85encode(s).decode()
                    case 'b64u':
                        return lambda s: base64.urlsafe_b64encode(s).decode()
                    case 'b64':
                        return lambda s: base64.b64encode(s).decode()
                    case 'b16':
                        return lambda s: base64.b16encode(s).decode()
                    case _:
                        raise Exception(Configuration.get('dialog', 'error', 'selection_error') + message)
            else:
                for item in args:
                    message = message[item]

            if 'dialog' in args:
                return message[Configuration.getlang()]

            return message
        except KeyError as e:
            print(f"KeyError -> {Configuration.get('dialog','error','key_error')}{e}")
            time.sleep(10)

    @staticmethod
    def set(*config: str, value: Any) -> None:
        setting = _System.CFG['config']
        for item in config[:-1]:
            setting = setting.setdefault(item, {})
        setting[config[-1]] = value

    @staticmethod
    def setsafe() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','safe_mode'))
            print(Configuration.get('dialog','configuration','safe','set_safe'))
            choice = input(" ---> ")

            match choice:
                case '0':
                    _System.save()
                    break
                case _ if choice.lower() in ['y','s']:
                    Configuration.set('safe_mode',value=True)
                case _ if choice.lower() == 'n':
                    Configuration.set('safe_mode',value=False)
                case _:
                    raise ValueError("[Configuration:setsafe]")

    @staticmethod
    def setkeys() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','key_number'))
            print(Configuration.get('dialog','configuration','key','set_key'))
            choice: int = int(
                input(" --> ")
            )

            match choice:
                case  0:
                    _System.save()
                    break
                case _ if choice in range(2,6):
                    Configuration.set('key_number',value=choice)
                case _:
                    raise ValueError("[Configuration:setkeys]")

    @staticmethod
    def setbase() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','pref_base'))
            print(Configuration.get('dialog','configuration','base','set_base'))
            choice: int = int(
                input(
                    "(1) Base85\n"
                    "(2) Base64url\n"
                    "(3) Base64\n"
                    "(4) Base16\n"
                    " --> "
                )
            )

            match choice:
                case 0:
                    _System.save()
                    break
                case 1:
                    Configuration.set('pref_base',value='b85')
                case 1:
                    Configuration.set('pref_base',value='b64u')
                case 3:
                    Configuration.set('pref_base',value='b64')
                case 4:
                    Configuration.set('pref_base',value='b16')
                case _:
                    raise ValueError("[Configuration:setbase]")

    @staticmethod
    def setlimit() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','pass_limit'))
            print(Configuration.get('dialog','configuration','limit','set_limit'))
            choice: int = int(
                input(" --> ")
            )

            match choice:
                case 0:
                    _System.save()
                    break
                case _ if choice in range(1,257):
                    Configuration.set('pass_limit',value=choice)
                case _:
                    raise ValueError("[Configuration:setlimit]")

    @staticmethod
    def setlang() -> None:
        while True:
            Configuration.clear()

            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','pref_lang'))
            print(Configuration.get('dialog','configuration','language','set_language'))
            choice: int = int(
                input(
                    f"(1) {Configuration.get('dialog','configuration','language','english')}\n"
                    f"(2) {Configuration.get('dialog','configuration','language','portuguese')}\n"
                    f" --> "
                )
            )

            match choice:
                case 0:
                    _System.save()
                    break
                case 1:
                    Configuration.set('pref_lang',value='eng')
                case 2:
                    Configuration.set('pref_lang',value='pt-br')
                case _:
                    raise ValueError("[Configuration:setlang]")

    @staticmethod
    def setalgorithms() -> None:
        while True:
            Configuration.clear()
            print(Configuration.get('dialog','configuration','menu','current'),
                  Configuration.get('config','algorithm'))
            print(Configuration.get('dialog','configuration','algorithm','menu'))
            choice: int = int(
                input(
                    f"(1) {Configuration.get('dialog','configuration','algorithm_parameters','keys_algo')}\n"
                    f"(2) {Configuration.get('dialog','configuration','algorithm_parameters','pass_algo')}\n"
                    f"(3) {Configuration.get('dialog','main','edit')}\n"
                    f" --> "
                )
            )

            match choice:
                case 0:
                    _System.save()
                    break
                case 1:
                    while True:
                        Configuration.clear()
                        print(Configuration.get('dialog','configuration','menu','current'),
                              Configuration.get('config','algorithm')[0])
                        print(Configuration.get('dialog','configuration','algorithm','set_key'))
                        choice: int = int(
                            input(
                                "(1) blake\n"
                                "(2) hmac\n"
                                "(3) argon\n"
                                " --> "
                            )
                        )

                        option: str = [None,'blake','hmac','argon'][choice]
                        hasher: str = Configuration.get('config','algorithm')[1]

                        match choice:
                            case 0:
                                _System.save()
                                break
                            case _ if choice in range(1,len(option)):
                                Configuration.set('algorithm',value=[option,hasher])
                            case _:
                                raise ValueError("[Configuration:setalgorithms]")
                case 2:
                    while True:
                        Configuration.clear()
                        print(Configuration.get('dialog','configuration','menu','current'),
                              Configuration.get('config','algorithm')[1])
                        print(Configuration.get('dialog','configuration','algorithm','set_hash'))
                        choice: int = int(
                            input(
                                  "(1) argon\n"
                                  "(2) bcrypt\n"
                                  "(3) scrypt\n"
                                  " --> "
                            )
                        )

                        option: str = [None,'argon','bcrypt','scrypt'][choice]
                        key: str = Configuration.get('config','algorithm')[0]

                        match choice:
                            case 0:
                                _System.save()
                                break
                            case _ if choice in range(1,len(option)):
                                Configuration.set('algorithm',value=[key,option])
                            case _:
                                raise ValueError("[Configuration:setalgorithms]")
                case 3:
                    Configuration.setparameters()
                case _:
                    raise ValueError("[Configuration:setalgorithms]")

    @staticmethod
    def setparameters() -> None:
        ## Inner auxiliary method declaration
        def _modifyparameters(hash_type: Literal['key_hasher','pass_hasher']) -> None:
            while True:
                hasher = Configuration.get('config','algorithm')[0] if hash_type == 'key_hasher'\
                    else Configuration.get('config','algorithm')[1]
                attribute_dict = Configuration.get('config','algorithm_parameters',hash_type,hasher)

                items = list(attribute_dict.keys())

                for i, key in enumerate(items,start=1):
                    print(f'({i}) {key}')

                choice: int = int(input(" --> "))

                match choice:
                    case 0:
                        _System.save()
                        break
                    case _ if choice in range(1,len(items)+1):
                        selectioned_item = items[choice-1]
                        attribute = attribute_dict[selectioned_item]
                        var_type = type(attribute)

                        try:
                            raw_input_value = input(
                                f"{Configuration.get('dialog','configuration','menu','current')} "
                                f"{Configuration.get('config','algorithm_parameters',hash_type,hasher,selectioned_item)}\n"
                                f"{Configuration.get('dialog', 'main', 'read')}{selectioned_item}\n"
                                f" --> "
                            )

                            if raw_input_value == '0': break

                            value = var_type(raw_input_value)
                        except ValueError:
                            print(Configuration.get('dialog','error','type_error'))
                            time.sleep(1)
                        else:
                            Configuration.set('algorithm_parameters',hash_type,hasher,selectioned_item,value=value)

        ## Method functionality

        while True:
            Configuration.get('dialog','configuration','algorithm_parameters','set_algo_parameters')
            choice = int(
                input(
                    f"(1) {Configuration.get('dialog','configuration','algorithm_parameters','key_hasher')}\n"
                    f"(2) {Configuration.get('dialog','configuration','algorithm_parameters','pass_hasher')}\n"
                    " --> "
                )
            )

            print(Configuration.get('dialog','warning','knowledge_limit'))

            match choice:
                case 0:
                    _System.save()
                    break
                case 1:
                    _modifyparameters('key_hasher')
                case 2:
                    _modifyparameters('pass_hasher')
                case _:
                    raise ValueError("Configuration:setparameters")

############## Class end ##############

def buildmenu(options: dict[str,Callable[[],None]], start: int = 0) -> None:
    items = list(options.keys())

    for i, label in enumerate(items,start=start):
        print(f"({i}) {label}")

    choice = int(input(" --> "))
    back_option = choice == 0 and start == 0

    if back_option:
        raise StopIteration

    index_selecionado = choice - start
    selected_option = items[index_selecionado]

    action = options[selected_option]
    action()

def configure() -> None:
    while True:
        Configuration.clear()
        try:
            buildmenu(
                {
                    Configuration.get('dialog','main','back') : lambda: None,
                    Configuration.get('dialog','configuration', 'safe', 'safe_setting'): lambda: Configuration.setsafe(),
                    Configuration.get('dialog','configuration','key','key_setting'): lambda: Configuration.setkeys(),
                    Configuration.get('dialog','configuration', 'base', 'base_setting'): lambda: Configuration.setbase(),
                    Configuration.get('dialog','configuration', 'limit', 'limit_setting'): lambda: Configuration.setlimit(),
                    Configuration.get('dialog','configuration','language','language_setting'): lambda: Configuration.setlang(),
                    Configuration.get('dialog','configuration','algorithm','algo_setting'): lambda: Configuration.setalgorithms(),
                    Configuration.get('dialog','main','exit') : lambda: sys.exit(0)
                },
                start=0
            )

        except StopIteration:
            break

        except ValueError as e:
            print(f"{e} ValueError -> ", Configuration.get('dialog', 'error', 'value_error'))
            time.sleep(3)

        except Exception as e:
            print(f"Exception -> {e}")
            time.sleep(3)

# Load when imported
_System.load()