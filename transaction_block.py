from blockchain import CBlock
import pickle
from signatures import generate_keys, sign, verify
from transaction import Tx

class TxBlock (CBlock):

    def __init__(self, previous_block):
        super(TxBlock, self).__init__([], previous_block)

    def add_tx(self, tx_in):
        self.data.append(tx_in)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for trx in self.data:
            if not trx.is_valid():
                return False
        return True

if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Sucess! Loaded tx is valid")
    loadfile.close()

    root = TxBlock(None)
    root.add_tx(Tx1)

    Tx2 = Tx()
    Tx2.add_input(pu2,1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.add_tx(Tx2)

    B1 = TxBlock(root)

    Tx3 = Tx()
    Tx3.add_input(pu3,1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.add_tx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1,1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.add_tx(Tx4)

    with open("block.dat", "wb") as save_file:
        pickle.dump(B1, save_file)

    loadfile = open("block.dat" ,"rb")
    load_B1 = pickle.load(loadfile)

    for b in [root, B1, load_B1, load_B1.previous_block]:
        if b.is_valid():
            print ("Success! Valid block")
        else:
            print ("ERROR! Bad block")

    B2 = TxBlock(B1)

    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.sign(pr3)
    B2.add_tx(Tx5)

    load_B1.previous_block.add_tx(Tx4)

    for b in [B2, load_B1]:
        if b.is_valid():
            print ("ERROR! Bad block verified.")
        else:
            print ("Success! Bad blocks detected")
