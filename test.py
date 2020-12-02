from pprint import pprint
from parser.dstv_object import Dstv_object

test = Dstv_object("./parser/pt9.nc1")
print("Holes")
pprint(test.holes)
print("Contours")
pprint(test.external_contours)
