# Import Area
try:
    import time, sys
    from getpass import getpass
    from generator.Passwordgenerator import Password
    from generator.Hashgenerator import Hashgenerator
    from config.Configuration import Configuration, buildmenu, configure
except ImportError as e:
    print(f"ImportError -> {e}")
    sys.exit(1)

class Main:
    master_key_buffer: str | None = None

    @staticmethod
    def start() -> None:
        Configuration.clear()
        print(Configuration.get('dialog', 'main', 'selection'))

        buildmenu(
            {
                Configuration.get('dialog', 'main', 'generate_pass'): lambda: Main.generatepassword(),
                Configuration.get('dialog', 'main', 'generate_hash'): lambda: Main.generatehash(),
                Configuration.get('dialog', 'main', 'configuration'): lambda: Main.settings(),
                Configuration.get('dialog', 'main', 'exit'): lambda: sys.exit(0)
            },
            start=1
        )

    @staticmethod
    def generatehash() -> None:
        while True:
            Configuration.clear()

            print(Configuration.get('dialog','hash','confirmation'))
            choice = int(
                input(
                    f"(1) {Configuration.get('dialog','main','yes')}\n"
                    f"(2) {Configuration.get('dialog','main','no')}\n"
                    f"(3) {Configuration.get('dialog','hash','clear')}\n"
                    f" --> "
                )
            )

            match choice:
                case 1:
                    calc: int = int(
                        input(
                            f"{Configuration.get('dialog','hash','calculations')}\n"
                            f" --> "
                        )
                    )

                    mess: str = input(
                        f"{Configuration.get('dialog','hash','message')}\n"
                        " --> "
                    )

                    Main.master_key_buffer = Hashgenerator.gethash(calculations=calc,message=mess)
                    break
                case 2:
                    break
                case 3:
                    Main.master_key_buffer = None
                    break
                case _:
                    raise ValueError("[Main:generatehash]")

    @staticmethod
    def generatepassword() -> None:
        blank = ''

        master_was_none: bool = Main.master_key_buffer is None
        safe_mode: bool = Configuration.get('config', 'safe_mode')
        key_number: int = Configuration.get('config', 'key_number')

        read = getpass if safe_mode else input
        print_parameter = lambda key: Configuration.get('dialog','main','read') + Configuration.get('dialog','password',key)

        context: str = read(f"{print_parameter('context')} --> ")

        key1: str | None = read(f"{print_parameter('key1')} --> ")\
            if key_number >= 3 else blank

        key2: str | None = read(f"{print_parameter('key2')} --> ")\
            if key_number >= 4 else blank

        key3: str | None = read(f"{print_parameter('key3')} --> ")\
            if key_number == 5 else blank

        master_key: str = read(f"{print_parameter('master_key')} --> ") if Main.master_key_buffer is None\
            else Main.master_key_buffer

        password = Password(
            ctx=context,
            k1=key1,
            k2=key2,
            k3=key3,
            mtr=master_key
        ).process()[:Configuration.get('config','pass_limit')]

        print_password = lambda: print(
            f"\n{Configuration.get('dialog', 'main', 'delivery')}\n"
            f"\n{password}\n"
            f"\n{Configuration.get('dialog','main','length')}{len(password)}\n"
        )

        if safe_mode:
            while True:
                confirmation = input(
                    f"{Configuration.get('dialog','password','print_confirmation')}\n"
                    f" --> "
                )

                confirmation = True if confirmation in ['y','s'] else (False if confirmation == 'n' else None)

                if confirmation:
                    print_password()
                elif not confirmation:
                    break
                else:
                    continue

                break
        else:
            print_password()

        Configuration.copy(password)

        if master_was_none:
            Main.master_key_buffer = None
        elif not master_was_none and not safe_mode:
            print(
                f"Hash:\n"
                f"{master_key}\n"
            )

        time.sleep(1.5)
        input(Configuration.get('dialog','main','continue'))

    @staticmethod
    def settings():
        configure()

if __name__ == '__main__':
    while True:
        try:
            Main.start()

        except StopIteration:
            continue

        except KeyboardInterrupt:
            print("\n" + Configuration.get('dialog', 'warning', 'program_finalized'))
            time.sleep(1)
            sys.exit(0)

        except ValueError as e:
            print(f"{e} ValueError -> ", Configuration.get('dialog', 'error', 'value_error'))
            time.sleep(3)

        except Exception as e:
            print(f"Exception -> {e}")
            time.sleep(3)