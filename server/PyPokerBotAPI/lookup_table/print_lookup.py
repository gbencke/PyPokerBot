import pprint
from ..helpers.LookupTable import LookupTable


lookup = LookupTable()

XX = lookup.create_lookup("XX")
print('lookup_table = { "XX" : \\')
pprint.PrettyPrinter().pprint(XX)
print(' } ')
exit(0)

print(lookup.create_lookup("XX:XX"))
print(lookup.create_lookup("XX:XX:XX"))
print(lookup.create_lookup("T5"))
print(lookup.create_lookup("T5:XX"))
print(lookup.create_lookup("T5:XX:XX"))


