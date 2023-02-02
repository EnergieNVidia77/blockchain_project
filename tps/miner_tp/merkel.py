import merkelClass as mC
import Transaction as Tr

transactionList = [Tr.Transaction("alice", "bob", 50), Tr.Transaction("didier", "ernest", 30),
                    Tr.Transaction("philipe", "roger", 5), Tr.Transaction("patrick", "caramba", 150)]
HashList = [i.get_hash() for i in transactionList]
print(HashList)
A = mC.makeMerkel(HashList)
print("")
print(mC.printArbre(A))
print("")
B = A.proof(3)
print(A.proof(3))
print("")
print(mC.EvalProof(B, 7, A.value))