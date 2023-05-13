# Classe des arbres de Merkle
import hashlib
import pickle


class merkleTree:
    def __init__(self, v, nextL, nextR, nb = -1):
        self.value = v
        self.nextR = nextR
        self.nextL = nextL
        self.nb = nb
    # Permet de modifier la valeur des de la racine de l'arbre

    def modifyValue(self, v):
        self.value = v

    # Evalue la valeur de du noeud pendant la création de l'arbre
    def evalValue(self):
        if self.nextR == None and self.nextL == None:
            return self.value
        elif self.nextR == None and self.nextL != None:
            return self.nextR.evalValue().hexdigest()
        elif self.nextR != None and self.nextL == None:
            return self.nextL.evalValue().hexdigest()
        # Donne la preuve de la transaction numero i  in  [0, len(transction) - 1]
        else:
            return hashlib.sha256(pickle.dumps(
                int(self.nextR.evalValue(), 16)
                + int(self.nextL.evalValue(), 16)
                )).hexdigest()



    def proof(self, i):
        if self.nb <= 1:
            return []
        if i >= self.nb:
            return []
        else:
            depth = findDepth(self.nb)

            if i < 2**(depth - 1):

                return [self.nextR.value] + self.nextL.proof(i%(2**(depth - 1)))
            else:
                return [self.nextL.value] + self.nextR.proof(i%(2**(depth - 1)))

    # Donne la valeur de la racine de l'arbre
    def get_root(self):
        return self.value


# Donne la profondeur de l'arbre crée avec une liste de la taille size
def findDepth(size):
    pow2 = 0
    div = size
    while (div > 1):
        pow2 += 1
        div = div/2
    return pow2


# print l'arbre de merkel t
def printArbre(t):
    if t == None :
        return ""
    else:
        return f"{t.value}[{printArbre(t.nextL)}, {printArbre(t.nextR)}]"


# Crée l'arbre de merkel associé a la liste LV passer en parametre
def makeMerkle(LV):
    size = len(LV)
    depth = findDepth(size)
    if depth <= 0:
        return merkleTree(LV[0], None, None, 0)
    else:
        listR = []
        listL = []
        bound = 2**(depth-1)
        for i in range(size):
            if i < bound:
                listL.append(LV[i])
            else:
                listR.append(LV[i])
        toReturn = merkleTree(-1, makeMerkle(listL), makeMerkle(listR), size)
        toReturnValue = toReturn.evalValue()
        toReturn.modifyValue(toReturnValue)
        return toReturn


def EvalProof(proof, leaf, head):
    currentRes = leaf
    for i in reversed(proof):
        currentRes = hashlib.sha256(pickle.dumps(
            int(i, 16) + int(currentRes, 16))).hexdigest()

    if currentRes == head:
        return True
    else:
        return False