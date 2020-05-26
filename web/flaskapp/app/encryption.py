from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# NOTE: parameters and return values should be of type Python string (i.e. convert to and from byte strings as neccessary internally here)

def GenerateKeyPair(seed=None):
  """Returns (public, private) key pair tuple. Uses seed if given, otherwise generates random keys."""
  if seed:
    # generate key pair using provided seed
    return ("publicKey", "privateKey")  # FIXME
  else:
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    return (public_pem.decode(), private_pem.decode())

def Encrypt(publicKey, plaintext):
  publicKey = publicKey.encode('utf-8')
  plaintext = plaintext.encode('utf-8')
  public_key = serialization.load_pem_public_key(publicKey, backend=default_backend())
  ciphertext = public_key.encrypt(plaintext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
  """Encrypts plaintext using provided public key and returns ciphertext"""
  return ciphertext

def Decrypt(privateKey, ciphertext):
  privateKey = privateKey.encode('utf-8')
  private_key = serialization.load_pem_private_key(privateKey, password=None, backend=default_backend())
  plaintext = private_key.decrypt(ciphertext,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
  """Encrypts plaintext using provided public key and returns ciphertext"""
  return plaintext.decode()