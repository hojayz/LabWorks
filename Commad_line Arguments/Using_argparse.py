import argparse

parser = argparse.ArgumentParser(
                    prog = 'SquareRoot',
                    description= 'This program find the square root of argument',
                    epilog= 'Text at the bottom of help'
)
parser.add_argument('square', help='display a square of a given number',
                    type=int)
parser.add_argument('-v', '--verbose', help="increase output verbosity",
                    action='store_true')

args = parser.parse_args()
print(args.square**2)
print(f'the value of {args.v} or {args.verbose}')

