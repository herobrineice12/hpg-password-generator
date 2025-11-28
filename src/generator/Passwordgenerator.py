# Import Area
try:
    import sys, hashlib, bcrypt
    import argon2.low_level as argon
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from argon2.low_level import Type
    from config.Configuration import Configuration
except ImportError as e:
    print(f"ImportError -> {e}")
    sys.exit(1)

class Password:
    _context: str
    _key1: str
    _key2: str
    _key3: str
    _master: str

    def __init__(self, ctx: str, k1: str, k2: str, k3: str, mtr: str):
        self._context = ctx
        self._key1 = k1
        self._key2 = k2
        self._key3 = k3
        self._master = mtr

    def process(self) -> str:
        _key_hasher = self.Encoder.getkeyhasher()

        keys = [self._key1, self._key2, self._key3]
        key_bytes = b''.join(_key_hasher(key) for key in keys)

        supersalt = hashlib.pbkdf2_hmac(
            hash_name="sha3_512",
            password=key_bytes,
            salt=_key_hasher(self._context),
            iterations=Password._getintfromsignature('herobrineice12'),
            dklen=64
        )

        _pass_hasher = self.Encoder.getpasshasher()

        password = _pass_hasher(key=self._master,salt=supersalt)

        decoder = Configuration.get('config','pref_base','decoder')
        limit = Configuration.get('config','pass_limit')

        return decoder(password)[:limit]

    @staticmethod
    def _getintfromsignature(signature: str):
        _bytes = hashlib.sha3_256(signature.encode()).digest()
        return int.from_bytes(_bytes[:12],'big') % 12 ** 5

    # Subclasses

    class Encoder:
        @staticmethod
        def getkeyhasher():
            hasher = Configuration.get('config','algorithm','key_hasher')

            def _blake_mixer(key: str='') -> bytes:
                passw = key.encode()
                salt = hashlib.sha256(key.encode()).digest()

                return PBKDF2HMAC(
                    algorithm=hashes.BLAKE2b(64),
                    length=64,
                    salt=salt,
                    iterations=Configuration.get('config','algorithm','parameters','key_hasher','blake','iteration')
                ).derive(passw)


            def _hmac_mixer(key: str='') -> bytes:
                passw = key.encode()
                salt = hashlib.sha256(key.encode()).digest()

                return hashlib.pbkdf2_hmac(
                    hash_name='sha512',
                    password=passw,
                    salt=salt,
                    iterations=Configuration.get('config','algorithm','parameters','key_hasher','hmac','iteractions'),
                    dklen=Configuration.get('config','algorithm','parameters','key_hasher','hmac','dklen')
                )

            def _argon_mixer(key: str='') -> bytes:
                passw = key.encode()
                salt = hashlib.sha256(key.encode()).digest()

                return argon.hash_secret_raw(
                    secret=passw,
                    salt=salt,
                    time_cost=Configuration.get('config','algorithm','parameters','key_hasher','argon','time_cost'),
                    memory_cost=Configuration.get('config','algorithm','parameters','key_hasher','argon','memory_cost'),
                    parallelism=Configuration.get('config','algorithm','parameters','key_hasher','argon','parallelism'),
                    hash_len=Configuration.get('config','algorithm','parameters','key_hasher','argon','hash_len'),
                    type=Type.ID
                )

            match hasher:
                case 'blake':
                    return _blake_mixer
                case 'argon':
                    return _argon_mixer
                case 'hmac':
                    return _hmac_mixer
                case _:
                    raise AttributeError('[Password:Encoder:getkeyhasher]')

        @staticmethod
        def getpasshasher():
            hasher = Configuration.get('config','algorithm','pass_hasher')

            def _argon_mixer(key: str='',salt: bytes=''.encode()):
                passw = key.encode()

                return argon.hash_secret_raw(
                    secret=passw,
                    salt=salt,
                    time_cost=Configuration.get('config','algorithm','parameters','pass_hasher','argon','time_cost'),
                    memory_cost=Configuration.get('config','algorithm','parameters','pass_hasher','argon','memory_cost'),
                    parallelism=Configuration.get('config','algorithm','parameters','pass_hasher','argon','parallelism'),
                    hash_len=256,
                    type=Type.ID
                )

            def _bcrypt_mixer(key: str='',salt: bytes=''.encode()):
                passw = key.encode()

                return bcrypt.kdf(
                    password=passw,
                    salt=salt,
                    rounds=Configuration.get('config','algorithm','parameters','pass_hasher','bcrypt','rounds'),
                    desired_key_bytes=256
                )

            def _scrypt_mixer(key: str='',salt: bytes=''.encode()):
                passw = key.encode()

                return hashlib.scrypt(
                    password=passw,
                    salt=salt,
                    n=Configuration.get('config','algorithm','parameters','pass_hasher','scrypt','n'),
                    r=Configuration.get('config','algorithm','parameters','pass_hasher','scrypt','r'),
                    p=Configuration.get('config','algorithm','parameters','pass_hasher','scrypt','p'),
                    maxmem=Configuration.get('config','algorithm','parameters','pass_hasher','scrypt','maxmem'),
                    dklen=256
                )

            match hasher:
                case 'argon':
                    return _argon_mixer
                case 'bcrypt':
                    return _bcrypt_mixer
                case 'scrypt':
                    return _scrypt_mixer
                case _:
                    raise AttributeError("[Password:Encoder:getpasshasher]")
