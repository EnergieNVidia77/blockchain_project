import merkle_class as mC
import transaction_class as Tr
from block_class import Block


transactionList = [Tr.Transaction(b"alice", "bob", 50), Tr.Transaction(b"didier", "ernest", 30),
                    Tr.Transaction(b"philipe", "roger", 5), Tr.Transaction(b"patrick", "caramba", 150)]
myBlock = Block(122, transactionList, "salut les bro")
print(myBlock)
myMerkle = myBlock.get_header()
print("Merkle root: ", myMerkle.get_root())
print("")
myProof = myMerkle.proof(3)

print("proof: ", myProof)
print("")
print(mC.EvalProof(myProof, transactionList[3].get_hash(), myMerkle.get_root()))


print("---------------")

h1 = transactionList[0].get_hash()
h2 = transactionList[1].get_hash()
h3 = transactionList[2].get_hash()
h4 = transactionList[3].get_hash()


