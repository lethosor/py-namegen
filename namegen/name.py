"""
Cluster-chaining name generator
"""

import random
import re

try:
    unicode('')
except NameError:
    unicode = str

def xor(c1, c2):
    if c1 and c2:
        return False
    if c1 or c2:
        return True
    return False

__metaclass__ = type

class Generator:    
    def __init__(self, data):
        self.filters = ['\W']
        self.cluster_cache = {}
        self.names = False
        
        if isinstance(data, list):
            self.names = data
        elif hasattr(data, 'read'):
            if hasattr(data.read, '__call__'):
                data = data.read()
        if isinstance(data, str):
            self.names = data.replace('\r', '').split()
        if not self.names:
            raise TypeError('Data cannot be used to create name list.')
        # Unicode!
        for i, n in enumerate(self.names):
            if not isinstance(n, unicode):
                self.names[i] = unicode(n, 'UTF-8')
    
    def clusters(self, clength):
        if not isinstance(clength, int):
            raise TypeError('Cluster length must be an integer')
        if clength < 2:
            raise RangeError('Cluster length must be at least 2')
        if not clength in self.cluster_cache:
            clusters = []
            filters = [re.compile(f, re.UNICODE) for f in (self.filters + ['[\x01\x02]'])]
            for n in self.names:
                for f in filters:
                    n = re.sub(f, '', n)
                n = n.lower()
                # Prepend/append markers
                n = '\x01' * (clength - 1) + n + '\x02' * (clength - 1)
                for i in range(len(n) - (clength - 1)):
                    clusters.append(n[i:i + clength])
            self.cluster_cache[clength] = clusters
        return self.cluster_cache[clength]
    
    def generate(self, length=8, clength=3):
        clusters = self.clusters(clength)
        result = '\x01' * (clength - 1)  # maybe just 1
        while len(result) - clength + 1 < length:
            random.shuffle(clusters)
            ok = False
            for c in clusters:
                if result.endswith(c[:-1]):
                    result += c[-1]
                    ok = True
                    break
            if not ok:
                raise Exception('Failed to generate name')
        return result
        #return result[clength-1:]
        #return result[clength - 1:length + clength - 1]
        #return result[1:-1]
        
    