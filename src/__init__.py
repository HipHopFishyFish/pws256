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
import types
from typing import TypeVar


__all__ = [
    "_Password",
    "Password",
    "defaultpass",
    "PwsType"
]

class CantSetError(Exception): ...

class _Password:
    def __init__(self, hashed, hsh_func, hsh_enter, hsh_after, salt):
        self.hashed = hashed
        self._hsh_enter = hsh_enter
        self._hsh_func = hsh_func
        self._hsh_after = hsh_after
        self.__salt = salt
        self.__salt_settable = False

    @property
    def hsh_func(self):
        return self._hsh_func
    
    @hsh_func.setter
    def hsh_func(self, obj):
        if not isinstance(obj, types.FunctionType):
            raise TypeError(
                f"obj must be a function, not {obj.__class__.__name__}"
            )
        self._hsh_func = obj

    @property
    def salt(self):
        return self.__salt
    
    @salt.setter
    def salt(self, val):
        if not self.__salt_settable:
            raise CantSetError(
                "You can't set the salt value"
            )
        else:
            self.__salt = val
    
    @property
    def hsh_after(self):
        return self._hsh_after
    
    @hsh_after.setter
    def hsh_after(self, obj):
        if not isinstance(obj, str):
            raise TypeError(
                f"obj must be of type 'str', not '{obj.__class__.__name__}'"
            )
        
    def salt_settable(self, which: bool = None):
        if which != None:
            if not isinstance(which, bool):
                raise TypeError(
                    f"which must be of type bool, not {which.__class__.__name__}"
                )
            self.__salt_settable = which
        return self.__salt_settable

    

    def validate(self, other: str):
        "Validate a password using the hsh_func entered on creation"
        print(hl.sha256(other.encode()).hexdigest(), self.salt)
        encoded = self.hsh_func(((self.salt + other) if self._hsh_enter == str else (self.salt + other).encode()))
        if self.hsh_after:
            encoded = eval("encoded" + self.hsh_after, dict({"encoded": encoded})) # Add hsh_after e.g. hashlib.sha256(b"hello").hexdigest()

        return encoded == self.hashed
    
    def __repr__(self):
        hsh_after = "" if self._hsh_after == None else self._hsh_after
        return f"<<PWS256 PASSWORD: {self._hsh_func.__name__}(obj: {self._hsh_enter.__name__}){hsh_after}>>"
    


class Password(_Password):
    def __init__(self, raw: str, hsh_func=hl.sha256, hsh_enter: str | bytes = bytes, hsh_after = ".hexdigest()"):
        salt = secrets.token_hex(40)
        encoded = hsh_func(((salt + raw) if hsh_enter == str else (salt + raw).encode()))
        if hsh_after:
            encoded = eval("encoded" + hsh_after, dict({"encoded": encoded})) # Add hsh_after e.g. hashlib.sha256(b"hello").hexdigest()


        super().__init__(encoded, hsh_func, hsh_enter, hsh_after, salt) # Initialise _Password with the result of the password

    

class defaultpass(Password):
    def __init__(self, raw: str):
        super().__init__(raw, hl.sha256, bytes, ".hexdigest()")


PwsType = TypeVar("PwsType", Password, _Password)


if __name__ == "__main__":
    print("Password: \"hello\" with sha256\n\n")

    pw = defaultpass("hello") # Generates internal code of sha256("hello".encode()).hexdigest()

    print("Password is hello!" if pw.validate("hello") else "uh oh what did u do wrong")
    print("\n")
    print("Password: \"Hello\" with reversed function\n\n")
    
    def reverse(x):
        return "".join(x)
    
    pw2 = Password("hello", hsh_func = reverse, hsh_enter = str, hsh_after = None) # Generates internal code of reverse("hello")

    print("Password is hello!" if pw2.validate("hello") else "uh oh what did u do wrong")
    