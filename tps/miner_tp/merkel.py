import merkelClass as mC
import Transaction as Tr
import Block

transactionList = [Tr.Transaction("alice", "bob", 50), Tr.Transaction("didier", "ernest", 30),
                    Tr.Transaction("philipe", "roger", 5), Tr.Transaction("patrick", "caramba", 150)]
myBlock = Block.Block(122, transactionList, "salut les bro")
myMerkel = myBlock.get_header()
print(myMerkel.get_root())
print("")
myProof = myMerkel.proof(3)
print(myProof)
print("")
print(mC.EvalProof(myProof, hash(transactionList[3]), myMerkel.get_root()))