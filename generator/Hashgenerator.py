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
                    iterations=iteractions,
                    dklen=128
                )
            )

    @staticmethod
    def _generatehash(start: int = 0,rounds: int = 10**4,limit: int = 10**6) -> str:
        import secrets

        hash_message: str = ''
        startszero = start == 0

        passlimit = lambda: start + rounds > limit

        while passlimit() or startszero:
            start = secrets.randbits(33)
            startszero = start == 0
            passlimit()

        if not start & 1:
            start += 1

        limit = start + limit

        candidates = [i for i in range(start,limit,2)
                      if i % 3 != 0 and i % 5 != 0 and i % 7 != 0]

        with Pool() as pool:
            results = pool.map(Hashgenerator._isprime,candidates)

        for num, isprime in zip(candidates,results):
            if isprime:
                hash_message += str(num)

        return hash_message

    @staticmethod
    def _isprime(num: int) -> bool:
        square: int = math.isqrt(num)

        for i in range(3,square+1,2):
            if num % i == 0:
                return False
        else:
            return True