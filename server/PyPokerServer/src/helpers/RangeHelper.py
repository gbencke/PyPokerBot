

class RangeHelper:

    def _get_sklansky_groups(self):
        return [ ['AA','AKs','KK','QQ','JJ'],
                 ['AKo','AQs','AJs','KQs','TT'],
                 ['AQo','ATs','KJs','JTs','99'],
                 ['AJo','KQo','KTs','QTs','J9s','T9s','98s','88'],
                 ['A9s','A8s','A7s','A6s','A5s','A4s','A3s','A2s','KJo','QJo','JTo','97s','87s','77','76s','66'],
                 ['ATo','KTo','QTo','J8s','86s','75s','65s','55','45s'],
                 ['K9s','K8s','K7s','K6s','K5s','K4s','K3s','K2s','J9o','T9o','98o','64s','53s','44','43s','33','22']
               ]


    def __init__(self):
        self.SklanskyRanges = self._get_sklansky_groups

    def get_group(self,group_index):
        ret = []
        for x in range(group_index):
            ret = ret + self.SklanskyRanges()[x]
        return ret

    def get_cards(self,str):
        if str == 'T1':
            return self.get_group(1)
        if str == 'T2':
            return self.get_group(2)
        if str == 'T3':
            return self.get_group(3)
        if str == 'T4':
            return self.get_group(4)
        if str == 'T5':
            return self.get_group(5)
        if str == 'T6':
            return self.get_group(6)
        if str == 'T7':
            return self.get_group(7)
        return [str]

    def parse(self, str):
        ret = ''
        for x in str.split(':'):
            ret = ret + ':' + ','.join(self.get_cards(x))
        return ret[1:]



