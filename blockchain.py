""" Simple blockchain"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

#digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
#digest.update(b"abc")
#digest.update(b"123")
#hash = digest.finalize()
#print(hash)

class someClass:
    string = None
    num = 1264378

    def __init__(self, mystring):
        self.string = mystring

    def __repr__(self):
        return self.string + "^^^^" + str(self.num)

class CBlock:

    previous_hash = None
    previous_block = None
    data = None

    def __init__(self, data, previous_block):
        self.data = data
        self.previous_block = previous_block
        if self.previous_block != None:
            self.previous_hash = previous_block.compute_hash()

    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.previous_hash), "utf-8"))
        digest.update(bytes(str(self.data), "utf-8"))
        return digest.finalize()

if __name__ == '__main__':
    root  = CBlock(b'I am root', None)
    B1 = CBlock('Im a child!', root)
    if root.compute_hash() == B1.previous_hash:
        print("Success! B1 hash matches")
    else:
        print("ERROR! B1 hash does not match")
    if B1.previous_block.compute_hash() == B1.previous_hash:
        print("Success! B1 hash matches")
    else:
        print("ERROR! B1 hash does not match")
    B2 = CBlock('Im a brother', root)
    B3 = CBlock(b'I contiain bytes', B1)
    B4 = CBlock(12354, B3)
    B5 = CBlock(someClass('Hi there!'), B4)
    B6 = CBlock("child of B5", B5)

    for b,name in [(B1,'B1'), (B2,'B2'), (B3,'B3'), (B4,'B4'), (B5,'B5')]:
        if b.previous_block.compute_hash() == b.previous_hash:
            print("Success! "+name+" hash matches")
        else:
            print("ERROR! " +name+" hash does not match")

    #Tampering
    B4.data = 12345
    if B5.previous_block.compute_hash() == B5.previous_hash:
        print("ERROR! Failed to detect tamper")
    else:
        print("Success! Tampering detected.")
    B5.data.num = 23678
    if B6.previous_block.compute_hash() == B6.previous_hash:
        print("ERROR! Failed to detect tamper")
    else:
        print("Success! Tampering detected.")





