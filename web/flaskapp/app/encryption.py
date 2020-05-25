
# NOTE: parameters and return values should be of type Python string (i.e. convert to and from byte strings as neccessary internally here)

def GenerateKeyPair(seed=None):
  """Returns (public, private) key pair tuple. Uses seed if given, otherwise generates random keys."""
  if seed:
    # generate key pair using provided seed
    return ("publicKey", "privateKey")  # FIXME
  else:
    # generate key pair using random seed
    return ("publicKey", "privateKey")  # FIXME

def Encrypt(publicKey, plaintext):
  """Encrypts plaintext using provided public key and returns ciphertext"""
  return (plaintext)  # FIXME

def Decrypt(privateKey, ciphertext):
  """Decrypts ciphertext using provided private key and returns plaintext"""
  return ciphertext  # FIXME
