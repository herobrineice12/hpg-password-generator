# Import Area
try:
    import sys, hashlib, math
    from typing import Callable
    from multiprocessing import Pool
    from config.Configuration import Configuration
except ImportError as e:
    print(f"ImportError -> {e}")
    sys.exit(1)

class Hashgenerator:
    decoder: Callable[[bytes],str]

    @staticmethod
    def gethash(calculations: int | None = None, message: str | None = None) -> str:
        Hashgenerator.decoder = Configuration.get('config','pref_base','decoder')

        if message and calculations is None:
            return Hashgenerator.decoder(Hashgenerator._generatehash().encode())
        else:
            bits: int = 2**calculations
            iteractions: int = calculations**2

            return Hashgenerator.decoder(
                hashlib.pbkdf2_hmac(
                    hash_name="sha3_512",
                    password=Hashgenerator._generatehash(bits).encode(),
                    salt=message.encode(),
                    iterations=512,
                    dklen=128
                )
            )

    @staticmethod
    def _generatehash(bits: int = 32,interactions: int = 10**4,limit: int = 10**6) -> str:
        import secrets, os, ctypes

        start: int = secrets.randbits(bits)
        rounds: int = start + interactions

        while rounds > limit:
            start = secrets.randbits(bits)
            rounds = start + interactions

        if not start & 1:
            start += 1

        candidates = [
            i for i in range(start,rounds,2)
            if i % 3 != 0 and i % 5 != 0 and i % 7 != 0
        ]

        dir_path: str = os.path.dirname(__file__)
        for _ in range(2): dir_path = os.path.dirname(dir_path)

        lib_path: str = os.path.join(dir_path,'lib')

        system: str = sys.platform
        loadlib: Callable[[str],ctypes.CDLL] = lambda lb: ctypes.CDLL(os.path.join(lib_path,lb))

        lib = None

        if system == "windows":
            lib = loadlib("libgo.dll")
        elif system == "linux":
            lib = loadlib("libgo.so")
        elif system == "darwin":
            lib = loadlib("libgo.dylib")
        else:
            raise Exception("Not implemented system")

        lib.generatePrimes.argtypes = [ctypes.POINTER(ctypes.c_int),ctypes.c_int]
        lib.generatePrimes.restype = ctypes.c_char_p

        length = len(candidates)
        array = (ctypes.c_int * length)(*candidates)

        return bytes(lib.generatePrimes(array,length)).decode()