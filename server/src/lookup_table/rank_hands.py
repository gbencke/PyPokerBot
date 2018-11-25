import .lookup_table as lookup_table

for x in lookup_table.lookup_table['XX']:
    print('{},{}'.format(x['current'],x['equity']))

