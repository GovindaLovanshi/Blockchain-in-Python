import hashlib

def crypto_hash(*args):
    inputs = sorted(args)  # Sort the input arguments
    hash = hashlib.sha256()
    hash.update(''.join(inputs).encode('utf-8'))
    return hash.hexdigest()

# Usage:
# result = crypto_hash("world", "hello")
# print(result)
