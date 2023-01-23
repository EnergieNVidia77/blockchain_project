
class merkelTree:
    def __init__(self, v, nextL, nextR, nb = -1):
        self.value = v
        self.nextR = nextR
        self.nextL = nextL
        self.nb = nb
    
    def modifyValue(self, v):
        self.value = v
    
    def evalValue(self):
        if self.nextR == None and self.nextL == None:
            return self.value
        elif self.nextR == None and self.nextL != None:
            return self.nextR.evalValue()
        elif self.nextR != None and self.nextL == None:
            return self.nextL.evalValue()
        else :
            return self.nextR.evalValue() + self.nextL.evalValue()
    
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
            
                                                    



    
def findDepth(size):
    pow2 = 0
    div = size
    while(div > 1):
        pow2 += 1
        div = div/2
    return pow2
    

def printArbre(t):
    if t == None :
        return ""
    else :
        return f"{t.value}[{printArbre(t.nextL)}, {printArbre(t.nextR)}]"

def makeMerkel(LV):
    size = len(LV)
    depth = findDepth(size)
    if depth <= 0:
        return merkelTree(LV[0], None, None, 0)    
    else:
        listR = []
        listL = []
        bound = 2**(depth-1)
        for i in range(size):
            if i < bound:
                listL.append(LV[i])
            else:
                listR.append(LV[i])
        toReturn = merkelTree(-1, makeMerkel(listL), makeMerkel(listR), size)
        toReturnValue = toReturn.evalValue()
        toReturn.modifyValue(toReturnValue)
        return toReturn

