
import random

__metaclass__ = type

class Generator:
    def __init__(self, data):
        if isinstance(data, str):
            data = data.split('\n')
        self.clusters = []
        for item in data:
            if item.find(' ') < 0:
                item += ' '
            name, info = item.split(' ', 2)
            for i in range(len(name) - 2):
                self.clusters.append((name[i:i+3], info))
    
    def generate(self, length=5):
        length -= 3  # Account for initial cluster and cluster length of 3
        valid = False
        while not valid:
            valid = True
            clusters = [random.choice(self.clusters)[0]]
            for i in range(length):
                random.shuffle(self.clusters)
                valid = False
                for c in self.clusters:
                    if c[0][0] == clusters[-1][2]:
                        valid = True
                        clusters.append(c[0])
                        break
                if not valid:
                    break
                if clusters[-2] == clusters[-1]:
                    # Don't allow triple letters
                    valid = False
                    break
        return (clusters[0][0] + ''.join([c[1:] for c in clusters]))[:length+3]
    
    

