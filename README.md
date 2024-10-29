# pws256
This is a python module for username and passwords with hash functions, which you can customise.


## Example
```
>>> import pws256 as pws
>>> pw = pws.Password()
>>> pw.hash_func
<hashlib.sha256>
>>> import hashlib as hl
>>> pw = pws.Password(hl.sha512)
>>> pw.hash_func
<hashlib.sha512>

```
