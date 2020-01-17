# import boolean

# sql = "((a OR b) AND (c OR d))"
# alg =  boolean.BooleanAlgebra()
# cond =  alg.parse(u"((a=2 OR b=1) AND (c=2 OR d=4))",simplify=True)
# print(cond)
# import re
# def ParseNestedParen(string, level):
#     """
#     Return string contained in nested (), indexing i = level
#     """
#     CountLeft = len(re.findall("\(", string))
#     CountRight = len(re.findall("\)", string))
#     if CountLeft == CountRight:
#         LeftRightIndex = [x for x in zip(
#         [Left.start()+1 for Left in re.finditer('\(', string)], 
#         reversed([Right.start() for Right in re.finditer('\)', string)]))]

#     elif CountLeft > CountRight:
#         return ParseNestedParen(string + ')', level)

#     elif CountLeft < CountRight:
#         return ParseNestedParen('(' + string, level)

#     return string[LeftRightIndex[level][0]:LeftRightIndex[level][1]]
# def maxDepth(S): 
#     current_max = 0
#     max = 0
#     n = len(S) 
  
#     # Traverse the input string 
#     for i in xrange(n): 
#         if S[i] == '(': 
#             current_max += 1
  
#             if current_max > max: 
#                 max = current_max 
#         elif S[i] == ')': 
#             if current_max > 0: 
#                 current_max -= 1
#             else: 
#                 return -1
  
#     # finally check for unbalanced string 
#     if current_max != 0: 
#         return -1
  
#     return max
# s= '((a=b or b=c) and ((c=4) and (e=8 or w))'
# print()
# print(ParseNestedParen(s, maxDepth(s) - 1))
import tt
from tt import BooleanExpression
with BooleanExpression('(a or (b and e))').constrain(a=1, b=0, e=1) as b:
    print(b.tokens)