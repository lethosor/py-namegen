"""
Cluster-chaining name generator
"""

import random
import re

try:
    unicode('')
except NameError:
    unicode = str

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