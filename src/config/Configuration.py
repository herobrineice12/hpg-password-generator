############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

try:
    import sys, os, platform, time
    from typing import Callable, Any, Literal
except ImportError as e:
    print(f"[Configuration] ImportError -> {e}")
    sys.exit(1)

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class _System:
    import json, shutil, subprocess, pyperclip, ctypes

    SYS: str = sys.platform
    OS: str = os.name
    PLAT: str = platform.system()

    CFG: dict = {}
    DLG: dict = {}
    RNT: dict = {}

    CONF_PATH: str

    @staticmethod
    def initialize():
        _System.CFG = _System.loaddata("src/data/preferences.json")
        _System.DLG = _System.loaddata("src/data/dialog.json")

    @staticmethod
    def save() -> None:
        with open(_System.CONF_PATH,'w') as file:
            _System.json.dump(_System.CFG,file,indent=4)

    @staticmethod
    def saveandexit() -> None:
        _System.save()
        raise StopIteration

    @staticmethod
    def loadlibrary(*path: str, file: str) -> ctypes.CDLL:
        from ctypes import CDLL

        try:
            windows_keys: dict[str,list] = {
                "sys": ["win32", "cygwin", "msys"],
                "os": ["nt"],
                "plat": ["Windows"]
            }

            linux_keys: dict[str,list] = {
                "sys": ["linux", "linux2"],
                "os": ["posix"],
                "plat": ["Linux"]
            }

            bsd_keys: dict[str,list] = {
                "sys": ["freebsd", "freebsd7", "freebsd8", "freebsdN", "openbsd6"],
                "os": ["posix"],
                "plat": ["FreeBSD", "OpenBSD"]
            }

            mac_keys: dict[str,list] = {
                "sys": ["darwin"],
                "os": ["posix"],
                "plat": ["Darwin"]
            }

            def _checksystem(keys) -> bool:
                return _System.SYS in keys['sys'] and _System.OS in keys['os'] and _System.PLAT in keys['plat']

            is_packaged: bool = getattr(sys,'frozen',False)

            if is_packaged:
                base_path: str = sys._MEIPASS
            else:
                base_path: str = os.path.join(os.path.abspath(__file__),"..","..")

            load_lib: Callable = lambda *p, f: CDLL(os.path.join(base_path,*p,f))

            if _checksystem(windows_keys):
                lib: CDLL = load_lib(path,f=f"{file}.dll")
            elif _checksystem(linux_keys) or _checksystem(bsd_keys):
                lib: CDLL = load_lib(path,f=f"{file}.so")
            elif _checksystem(mac_keys):
                lib: CDLL = load_lib(path,f=f"{file}.dylib")
            else:
                raise SystemError

            return lib

        except FileNotFoundError:
            print(f"[_System:loadlib] FileNotFoundError -> {e} not found")
            sys.exit(1)

        except SystemError:
            print(f"[_System:loadlib] SystemError -> {Configuration.get('dialog','error','system_error')}")
            sys.exit(1)

    @staticmethod
    def loaddata(path: str) -> dict:
        try:
            is_packaged: bool = getattr(sys,'frozen',False)
            is_preference: bool = "preferences" in path

            def load_file(file_location):
                with open(file_location,'r') as file: return _System.json.load(file)

            if is_packaged:
                base_path: str = sys._MEIPASS

                if is_preference:
                    pref = "preferences.json"
                    file_path: str = os.path.abspath(__file__)
                    local_pref: str = os.path.join(file_path,pref)

                    portable_doesnt_exist: bool = not os.path.exists(local_pref)

                    if portable_doesnt_exist:
                        _System.shutil.copy(os.path.join(base_path,path),file_path)
                        _System.CONF_PATH = local_pref

                    return load_file(local_pref)

                file_path = os.path.join(base_path,path)
                return load_file(file_path)

            if is_preference:
                _System.CONF_PATH = path

            return load_file(path)

        except FileNotFoundError as e:
            print(f"[_System:loaddata] FileNotFoundError -> {e} not found")
            sys.exit(1)

        except _System.json.JSONDecodeError:
            print("[_System:loaddata] JSONDecodeError -> Decoding error on json")
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

    load_library: _System.ctypes.CDLL = lambda *p,f: _System.loadlibrary(p,file=f)

    save_and_exit: None = lambda: _System.saveandexit()

    clear: None = lambda: _System.clear()
    copy: None = lambda s: _System.copy(s)

    throw: None = lambda ex: _System.throw(ex)

    getlang: str = lambda: _System.CFG['config']['pref_lang']

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

            if is_dialog:
                information: Any = _System.DLG
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
    def setsafe(value: bool) -> None:
        Configuration.set('config', 'safe_mode',value=value)

    @staticmethod
    def setkeys(value: int) -> None:
        Configuration.set('config', 'key_number', value=value)

    @staticmethod
    def setbase(value: str) -> None:
        Configuration.set('config', 'pref_base', value=value)

    @staticmethod
    def setlimit(value: int) -> None:
        Configuration.set('config', 'pass_limit', value=value)

    @staticmethod
    def setlang(value: str) -> None:
        Configuration.set('config', 'pref_lang', value=value)

    @staticmethod
    def setalgorithms(algo_type: Literal['key_hasher','pass_hasher'], value: str) -> None:
        Configuration.set('config', 'algorithm', algo_type, value=value)

    @staticmethod
    def setparameters(algo_type: Literal['key_hasher','pass_hasher'], hasher: str, attribute: str, value: Any) -> None:
        Configuration.set('config', 'algorithm', 'parameters', algo_type, hasher, attribute, value=value)


############## ############## ##############
#                CLASS END                 #
############## ############## ##############

# Load files when imported
_System.initialize()