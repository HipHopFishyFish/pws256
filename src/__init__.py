"""
This is used to verify passwords with custom hash functions (or sha256 by default)

--- pws256/

>>> import pws256
>>> pw = pws256.Password("password")
>>> pw.verify("password")
True
>>> pw.verify("pasword")
False
>>> pw.hsh_func
<built-in function openssl_sha256>
>>> pw2 = pws256.Password(
...    raw = "password",
...    hsh_func = lambda x : "".join(reversed(x)),
...    hsh_enter = str,
...    hsh_after = None
...)
...
>>> pw2.verify("password")
True
>>> pw2.hashed
"drowssap"
>>>
"""

import hashlib as hl
import secrets
from typing import TypeVar


class _Password:
    def __init__(self, hashed, hsh_func, hsh_enter, hsh_after, salt):
        self.hashed = hashed
        self.hsh_enter = hsh_enter
        self.hsh_func = hsh_func
        self.hsh_after = hsh_after
        self.salt = salt

    def validate(self, other: str):
        print(hl.sha256(other.encode()).hexdigest(), self.salt)
        encoded = self.hsh_func(((self.salt + other) if self.hsh_enter == str else (self.salt + other).encode()))
        if self.hsh_after:
            encoded = eval("encoded" + self.hsh_after, dict({"encoded": encoded}))

        return encoded == self.hashed
    


class Password(_Password):
    def __init__(self, raw: str, hsh_func=hl.sha256, hsh_enter: str | bytes = bytes, hsh_after = ".hexdigest()"):
        salt = secrets.token_hex(40)
        encoded = hsh_func(((salt + raw) if hsh_enter == str else (salt + raw).encode()))
        if hsh_after:
            encoded = eval("encoded" + hsh_after, dict({"encoded": encoded}))


        super().__init__(encoded, hsh_func, hsh_enter, hsh_after, salt) # Initialise _Password with the result of the password

    

def defaultpass(raw: str):
    return _Password(hl.sha256(raw.encode()).hexdigest(), hl.sha256, str, ".hexdigest()")


PwsType = TypeVar("PwsType", Password, _Password)


if __name__ == "__main__":
    print("Using password: \"hello\" with sha256")
    pw = Password("hello")
    print("It is " + str(pw.validate("hello")) + " that the password is \"hello\".")
    print("Using password: \"hello\" with reversed")
    reverse = lambda x : "".join(reversed(x))
    pw = Password("hello", reverse, str, None)
    print("It is " + str(pw.validate("hello")) + " that the password is \"hello\".")