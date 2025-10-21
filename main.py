import argparse
from PAPER.tree_tools import createNoisyGraph
import sys

def parse_args():
    parser = argparse.ArgumentParser(
                    prog='PAPERpaper',
                    description='Create disease-module-like graphs using PAPER (https://doi.org/10.1093/jrsssb/qkad102).')
    parser.add_argument('-n', '--nodes', help="number of nodes in the random graph", required=True, type=int)
    parser.add_argument('-e', '--edges', help="number of noise edges in the random graph", required=True, type=int)
    parser.add_argument('-a', '--alpha', help="Alpha for APA. See Section 2.1 of the paper.", default=1, type=int)
    parser.add_argument('-b', '--beta', help="Beta for APA. See Section 2.1 of the paper.", default=1, type=int)
    parser.add_argument('-k', '--k', help="The number of clusters.", default=1, type=int)
    parser.add_argument('-o', '--output', help="The desired output file. If none is specified, we print to stdout")

    return parser.parse_args()

def main():
    args = parse_args()

    # https://github.com/nineisprime/PAPER/blob/f11d95cbdeb319130cbcb20e4a220912951781cd/PAPER/tree_tools.py#L271
    (graph, _) = createNoisyGraph(n=args.nodes, m=args.edges, alpha=args.alpha, beta=args.beta, K=args.k)

    graph.write(args.output if args.output else sys.stdout, "edgelist")

if __name__ == "__main__":
    main()
