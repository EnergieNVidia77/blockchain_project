import hashlib
import pickle
import merkel_class as mC
import transaction_class as Tr
from block_class import Block

transactionList = [Tr.Transaction("alice", "bob", 50), Tr.Transaction("didier", "ernest", 30),
                    Tr.Transaction("philipe", "roger", 5), Tr.Transaction("patrick", "caramba", 150)]
myBlock = Block(122, transactionList, "salut les bro")
myMerkel = myBlock.get_header()
print(f"ma racine est {myMerkel.get_root()}")
print("")
myProof = myMerkel.proof(1)
print(f"ma preuve est {myProof}")
print("")
print(hashlib.sha256(pickle.dumps(int(myMerkel.get_root().hexdigest(), 16))))
print(mC.EvalProof(myProof, hashlib.sha256(pickle.dumps(transactionList[1])), myMerkel.get_root()))