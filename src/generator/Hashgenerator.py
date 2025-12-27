############## ############## ##############
#               IMPORT AREA                #
############## ############## ##############

try:
    import sys, hashlib
    from ctypes import *
    from typing import Callable
    from config.Configuration import Configuration
except ImportError as e:
    print(f"ImportError -> {e}")
    sys.exit(1)

############## ############## ##############
#             CLASS DEFINITION             #
############## ############## ##############

class Hashgenerator:
    decoder: Callable[[bytes],str]

    @staticmethod
    def gethash(bits: int | None = 16, message: str | None = None) -> str:
        Hashgenerator.decoder = Configuration.get('config','pref_base','decoder')

        points: dict = Hashgenerator.definepoints(bits)

        candidates: list[int] = Hashgenerator.filtercandidates(points)
        
        return Hashgenerator.decoder(
            hashlib.pbkdf2_hmac(
                hash_name="sha3_512",
                password=Hashgenerator.generatehash(candidates),
                salt=message.encode(),
                iterations=64,
                dklen=128
            )
        )

    @staticmethod
    def definepoints(bits):
        import secrets

        CEIL_LIMIT: int = 2**33

        if not 0 < bits or bits > 33:
            raise ValueError(Configuration.get('dialog','error','value_error'))

        start: int = secrets.randbits(bits)
        rounds: int = secrets.randbits(bits)

        INSTANCE_FLOOR: int = 2 ** (bits - 1)
        INSTANCE_CEIL: int = 2 ** bits + 1

        while (rounds < INSTANCE_FLOOR or rounds < INSTANCE_CEIL) and rounds < CEIL_LIMIT:
            rounds += start

        if start & 1:
            start += 1

        return {
            "start": start,
            "rounds": rounds
        }


    @staticmethod
    def filtercandidates(points: dict):
        candidates = [
            i for i in range(points['start'],points['rounds'],2)
            if all(i % d != 0 for d in (3,5,7))
        ]

        return candidates


    @staticmethod
    def generatehash(candidates: list) -> bytes:
        import os, ctypes

        has_minimun_workload: bool = len(candidates) >= 65_536

        def loadlib(*path,file) -> ctypes.CDLL:
            is_packaged: bool = getattr(sys, 'frozen', False)

            if is_packaged:
                dir_path: str = sys._MEIPASS
            else:
                dir_path: str = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..")
                )

            lib_path: str = os.path.join(dir_path, 'lib')

            system: str = sys.platform
            load_lib: Callable[[str], ctypes.CDLL] = lambda *lb: ctypes.CDLL(os.path.join(lib_path, *lb))

            lib: ctypes.CDLL | None = None

            match system:
                case "windows":
                    lib = load_lib(*path,f"{file}.dll")
                case "linux":
                    lib = load_lib(*path,f"{file}.so")
                case "darwin":
                    lib = load_lib(*path,f"{file}.dylib")
                case _:
                    raise Exception(Configuration.get('dialog', 'error', 'library_error'))           

            return lib

        if has_minimun_workload:
        # Golang + Fortran implementation
            lib = loadlib('go',file='libgo')

            lib.generatePrimes.argtypes = [POINTER(c_int),c_int]
            lib.generatePrimes.restype = c_char_p

            length: int = len(candidates)

            c_array = (c_int * length)(*candidates)
            c_length = c_int(length)

            return lib.generatePrimes(c_array,c_length)
        else:
        # C implementation
            lib = loadlib('c',file='libc')

            lib.generateprimes.argtypes = [POINTER(c_int),c_int]
            lib.generateprimes.restype = c_char_p

            length: int = len(candidates)

            c_array = (c_int * length)(*candidates)
            c_length = c_int(length)

            return lib.generateprimes(c_array,c_length)

            