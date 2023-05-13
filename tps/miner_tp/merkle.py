import merkle_class as mC
import transaction_class as Tr
from block_class import Block


transactionList = [Tr.Transaction(b"alice", "bob", 50), Tr.Transaction(b"didier", "ernest", 30),
                    Tr.Transaction(b"philipe", "roger", 5), Tr.Transaction(b"patrick", "caramba", 150)]
myBlock = Block(122, transactionList, "salut les bro")
myMerkel = myBlock.get_header()
print(myMerkel.get_root())
print("")
myProof = myMerkel.proof(3)
print(myProof)
print("")
print(mC.EvalProof(myProof, transactionList[3].get_hash(), myMerkel.get_root()))