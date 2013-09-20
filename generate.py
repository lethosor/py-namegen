import argparse
import namegen

parser = argparse.ArgumentParser()
parser.add_argument('--length', required=False, default=5,
                    help="Name length (default 5)")
parser.add_argument('--count', required=False, default=10,
                    help="Number of names to generate (default 10)")
parser.add_argument('file', help="Input file (required)")
args = parser.parse_args()

f = open(args.file)
generator = namegen.name.Generator(f.read())
f.close()

for i in range(int(args.count)):
    print(generator.generate(int(args.length)))

