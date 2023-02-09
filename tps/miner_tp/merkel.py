import merkelClass as mC

L = [1,2,3,4, 5, 6, 7, 8]
A = mC.makeMerkel(L)
print(mC.printArbre(A))
print(A.proof(1))
