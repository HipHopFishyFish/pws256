import hashlib as hl


class _Password:
    def __init__(self, hashed, hsh_func, hsh_enter, hsh_after):
        self.hashed = hashed
        self.hsh_enter = hsh_enter
        self.hsh_func = hsh_func
        self.hsh_after = hsh_after

    def validate(self, other: str):
        encoded = self.hsh_func(other if self.hsh_enter == str else other.encode())
        if self.hsh_after:
            encoded = eval("encoded" + self.hsh_after, dict({"encoded": encoded}))

        return encoded == self.hashed
    


class Password(_Password):
    def __init__(self, raw: str, hsh_func=hl.sha256, hsh_enter: str | bytes = bytes, hsh_after = ".hexdigest()"):
        encoded = hsh_func(raw if hsh_enter == str else raw.encode())
        if hsh_after:
            encoded = eval("encoded" + hsh_after, dict({"encoded": encoded}))


        super().__init__(encoded, hsh_func, hsh_enter, hsh_after) # Initialise _Password with the result of the password

    
if __name__ == "__main__":
    print("Using password: \"hello\" with sha256")
    pw = Password("hello")
    print("It is " + str(pw.validate("hello")) + " that the password is \"hello\".")
    print("Using password: \"hello\" with reversed")
    reverse = lambda x : "".join(reversed(x))
    pw = Password("hello", reverse, str, None)
    print("It is " + str(pw.validate("hello")) + " that the password is \"hello\".")