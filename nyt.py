# This program solves 'challenge mode' (aka uses ALL numbers) for the Digits puzzle
# located at https://www.nytimes.com/games/digits"
# future version may create "hard questions" (limited number of solutions)
# Steve Earth, July 16 2023

from itertools import permutations as perm
from itertools import product as prod
QTY = 6 # quantity of number provided in game

# defining the allowable operations and how to display them
def plus(x,y):
    return x+y
def minus(x,y):
    return x-y
def mult(x,y):
    return x*y
def div(x,y):
    if y==0 or x%y!=0:
        return float("inf")
    else:
        return int(x/y)
OPS = [plus, minus, mult, div]
symbs = {plus:"+",minus:"-",mult:"*",div:"/"}

class Tree:
    
    def __init__(self, value=0):
        self.value = value
        self.right = None
        self.left = None
        
    def preprint(self, ops, nums):
        if not isinstance(self.value, int):
            return "("+self.left.preprint(ops,nums) + \
                   symbs[ops[int(self.value)]] + \
                   self.right.preprint(ops,nums) + ")"
        return str(nums[self.value])
    
    def eval(self, ops, nums):
        if isinstance(self.value, str):
            return ops[int(self.value)](self.left.eval(ops,nums), self.right.eval(ops,nums))
        return nums[self.value]
    
    # this decorates the tree with the operation indexes by replacing all the "." with "i"
    def dec(self, curr=None): # curr is how many . have been replaced thus far
        if curr==None:        # it needs to be a mutable list to not reset at recursion
            curr=[0]
        if not isinstance(self.value,str):
            return
        self.value = str(curr[0])
        curr[0]+=1
        self.left.dec(curr)
        self.right.dec(curr)
    
# making a list of all binary trees with n leaves, starting with label k
def makeTrees(n,k=0):
    if n==1:
        return [Tree(k)]
    ans = []
    for leftAmt in range(1,n):
        for leftTree in makeTrees(leftAmt, k):
            for rightTree in makeTrees(n - leftAmt,leftAmt+k):
                newTree = Tree(".")
                newTree.left = leftTree
                newTree.right = rightTree
                newTree.dec()
                ans.append(newTree)
    return ans

def search(ops, combos, trees, target):
    for op in ops:
        for combo in combos:
            for tree in trees:
                if tree.eval(op,combo)==target:
                    return (tree, op, combo)
    return "it is not possible to acquire that target using all six numbers"

genericTrees = makeTrees(QTY)
target = int(input("enter target value (or 0 to exit): "))
nums=[0]*QTY
while target!=0:
    for j in range(QTY):
        msg = "option #"+str(j+1)+": "
        nums[j]=int(input(msg))
    ans=search(list(prod(OPS,repeat=QTY-1)), list(perm(nums)), list(genericTrees), target)
    if isinstance(ans, str):
        print(ans)
    else:
        print(ans[0].preprint(ans[1],ans[2])+" = "+str(target))
    target = int(input("enter target value (or 0 to exit): "))
