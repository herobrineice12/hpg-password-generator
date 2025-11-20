# Import Area

try:
    import time, sys
    from getpass import getpass
    from generator.Passwordgenerator import Password
    from generator.Hashgenerator import Hashgenerator
    from config.Interface import Interface
    from config.Configuration import Configuration
except ImportError as e:
    print(f"ImportError -> {e}")
    sys.exit(1)

class Main:
    master_buffer: str | None = None

    @staticmethod
    def start() -> None:
        Configuration.clear()
        print(Configuration.get('dialog', 'main', 'selection'))

        Interface.buildmenu(
            {
                Configuration.get('dialog', 'main', 'generate_pass'):
                    lambda: Configuration.handle(Main.generatepassword,"Main:generatepassword"),

                Configuration.get('dialog', 'main', 'generate_hash'):
                    lambda: Configuration.handle(Main.generatehash,"Main:generatehash"),

                Configuration.get('dialog', 'main', 'configuration'):
                    lambda: Configuration.handle(Main.settings,"Main:settings"),

                Configuration.get('dialog', 'main', 'exit'):
                    lambda: sys.exit(0)
            },
            start=1
        )

    @staticmethod
    def generatepassword() -> None:
        blank = ''

        master_was_none: bool = Main.master_buffer is None
        safe_mode: bool = Configuration.get('config', 'safe_mode')
        key_number: int = Configuration.get('config', 'key_number')

        read = getpass if safe_mode else input
        print_parameter = lambda key: f"{Configuration.get('dialog', 'main', 'read')} {Configuration.get('dialog', 'password', key)}"

        context: str = read(f"{print_parameter('context')} --> ")

        key1: str | None = read(f"{print_parameter('key1')} --> ")\
            if key_number >= 3 else blank

        key2: str | None = read(f"{print_parameter('key2')} --> ")\
            if key_number >= 4 else blank

        key3: str | None = read(f"{print_parameter('key3')} --> ")\
            if key_number == 5 else blank

        master_key: str = read(f"{print_parameter('master_key')} --> ") if Main.master_buffer is None\
            else Main.master_buffer

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
            f"\n{Configuration.get('dialog','main','length')} {len(password)}\n"
        )

        if safe_mode:
            while True:
                confirmation = input(
                    f"{Configuration.get('dialog','password','print_confirmation')}\n"
                    f" --> "
                )

                confirmation = True if confirmation in ['y','s'] else (False if confirmation == 'n' else None)

                if confirmation: print_password()
                elif not confirmation: break
                else: continue

                break
        else:
            print_password()

        Configuration.copy(password)

        if master_was_none:
            Main.master_buffer = None
        elif not master_was_none and not safe_mode:
            print(
                f"Hash:\n"
                f"{master_key}\n"
            )

        time.sleep(1.5)
        input(Configuration.get('dialog','main','continue'))
        raise StopIteration

    @staticmethod
    def generatehash() -> None:
        ### Auxiliary methods ###
        def _hashgeneration() -> None:
            calculations = lambda message: int(input(message))

            calc: int = Configuration.call(
                calculations,
                "Main:generatehash:_hashgeneration",
                f"{Configuration.get('dialog', 'hash', 'calculations')}\n --> "
            )

            bit_missflow = calc > 32 or calc < 1

            if bit_missflow:
                print(Configuration.get('dialog','warning','bit_missflow'))
                return

            mess: str = input(
                f"{Configuration.get('dialog','hash','message')}\n --> "
            )

            Main.master_buffer = Hashgenerator.gethash(bits=calc,message=mess)
            raise StopIteration

        def _clearhash() -> None:
            Main.master_buffer = None

        ### Method Functionality ###

        Configuration.clear()

        print(Configuration.get('dialog','hash','confirmation'))

        Interface.buildmenu(
            {
                None:
                    lambda: Configuration.save_and_exit(),

                Configuration.get('dialog','main','yes'):
                    lambda: Configuration.handle(_hashgeneration,"Main:generatehash:_hashgeneration"),

                Configuration.get('dialog','main','no'):
                    lambda: Configuration.throw(StopIteration),

                Configuration.get('dialog','hash','clear'):
                    lambda: _clearhash()
            }
        )

    @staticmethod
    def settings() -> None:
        Configuration.clear()

        print(Configuration.get('dialog','configuration','menu','main'))

        Interface.buildmenu(
            {
                Configuration.get('dialog', 'main', 'back'):
                    lambda: Configuration.throw(StopIteration),

                Configuration.get('dialog', 'configuration', 'safe', 'safe_setting'):
                    lambda: Configuration.handle(Configuration.setsafe,"Configuration:setsafe"),

                Configuration.get('dialog', 'configuration', 'key', 'key_setting'):
                    lambda: Configuration.handle(Configuration.setkeys,"Configuration:setkeys"),

                Configuration.get('dialog', 'configuration', 'base', 'base_setting'):
                    lambda: Configuration.handle(Configuration.setbase,"Configuration:setbase"),

                Configuration.get('dialog', 'configuration', 'limit', 'limit_setting'):
                    lambda: Configuration.handle(Configuration.setlimit,"Configuration:setlimit"),

                Configuration.get('dialog', 'configuration', 'language', 'language_setting'):
                    lambda: Configuration.handle(Configuration.setlang,"Configuration:setlang"),

                Configuration.get('dialog', 'configuration', 'algorithm', 'algorithm_setting'):
                    lambda: Configuration.handle(Configuration.setalgorithms,"Configuration:setalgo"),

                Configuration.get('dialog', 'main', 'exit'):
                    lambda: sys.exit(0)
            }
        )

if __name__ == '__main__':
    Configuration.handle(Main.start,"Main:start")