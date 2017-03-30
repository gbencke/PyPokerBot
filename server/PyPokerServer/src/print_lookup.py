import helpers.LookupTable as LT


lookup = LT.LookupTable()

print(lookup.create_lookup("XX"))
exit(0)
print(lookup.create_lookup("XX:XX"))
print(lookup.create_lookup("XX:XX:XX"))
print(lookup.create_lookup("T5"))
print(lookup.create_lookup("T5:XX"))
print(lookup.create_lookup("T5:XX:XX"))


