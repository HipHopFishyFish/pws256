# pws256
This is a python module for username and passwords with hash functions, which you can customise.


## Example
```
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
>>> pw2.hashed # Includes salt so when reversed, salt is at the back
"drowssap...bv4w75..."
>>> import pws256.users as u
>>> pw3 = pws256.Password("hello")
>>> usr = u.User("me", pw3)
>>> usr.save_to_file("test.csv")
>>> user = u.User.load_from_file("me", "test.csv")
>>> user.password.verify("hello")
True
>>> pw4 = pws256.defaultpass("hello")
>>> pw4.salt = "abc"
Traceback (most recent call last):
...
>>> pw4.salt_settable(True)
>>> pw4.salt = "abc"
>>> pw4.salt
"abc"
>>> pw4.salt_settable(False)
Traceback (most recent call last):
...
>>>
```

# pws256.Password()

## Normal pws256.Password()

```
pw = pws256.Password(
    raw: str
)
```

Creates a password that can be verified and shaped in different ways


## Custom pws256.Password()

```
pw = pws256.Password(
    raw: str,
    hsh_func: function | class = hashlib.sha256,
    hsh_enter: type[str] | type[bytes] = type[bytes],
    hsh_after: str = ".hexdigest()"
)
```

Create a Password with a custom function that is called, type that goes into that function, and what comes after e.g. ```.hexdigest()```

### Initialisation Parameters

#### *hsh_func*
hsh_func is a parameter that must be a function.  
If you had a function called reverse and it took the reverse of a string,  
to use it here, you would have to have your function as the hsh_func

#### *hsh_enter*
hsh_enter determines which type the raw string should be before it enters the hash function  
hsh_enter is default as bytes, but if your function took in a string, you should  change it to str

#### *hsh_after*
hsh_after detirmines what to put after the function call using eval()  
for example, if you had hashlib.sha256 as your hsh_func, you should have  
".hexdigest()" as your hsh_after. If you don't want to call a method after,  
put hsh_after as None


### Methods

#### *validate()*
The validate method validates the password against a string
```
pw = pws256.Password("hello")
pw.validate("hello") # returns True
pw.validate("bello") # returns False
```




# pws256.defaultpass()


Derived from Password and has no parameters to confuse you!
```
pw = pws256.defaultpass(
    raw: str
)
```


# pws256.users.User()
```
usr = users.User("username", pws256.Password(...))
```

You can create a user with users.User()  
The password parameter has to be a pws256.Password() or has to be  
derived from pws256._Password().  

### Initialisation Parameters

#### *username*
A custom username that must be a string.

#### *password*
A password that is a class derived from _Password()  
If the class is not, it will throw an error.  

### Methods

#### *save_to_file(filename: str | TextIOWrapper, close: bool)*

You can save it to a file by using this method. The close param  
at the end can be used if you want to close the file afterwards.

#### (classmethod) *load_from_file(username: str, filename: str | TextIOWrapper, ...)*

```
users.User.load_from_file("username", "doc.csv")
```

You can use this method to get a new User from a file using a username
If you had a user who's username was "username", you could get it out from  
doc.csv using this method.


