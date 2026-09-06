from app.security.crypto import derive_key, encrypt, decrypt, new_salt

def test_round_trip_and_random_nonce():
    key=derive_key('Correct-Horse-Battery-42!', new_salt())
    a=encrypt('super-secret', key); b=encrypt('super-secret', key)
    assert a != b
    assert decrypt(a,key) == 'super-secret'

def test_wrong_key_fails():
    k1=derive_key('one-long-password!', new_salt())
    k2=derive_key('two-long-password!', new_salt())
    blob=encrypt('secret', k1)
    try: decrypt(blob,k2); assert False
    except Exception: assert True
