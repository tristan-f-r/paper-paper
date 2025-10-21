import argparse
import networkx as nx
from PAPER.tree_tools import addRandomEdges, createPATree
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        prog="PAPERpaper",
        description="Create disease-module-like graphs using PAPER (https://doi.org/10.1093/jrsssb/qkad102).",
    )
    parser.add_argument(
        "-n",
        "--nodes",
        help="number of nodes in the random graph",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-e",
        "--edges",
        help="number of noise edges in the random graph",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-a",
        "--alpha",
        help="Alpha for APA. See Section 2.1 of the paper.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-b",
        "--beta",
        help="Beta for APA. See Section 2.1 of the paper.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-k", "--k", help="The number of clusters.", default=1, type=int
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The desired output file. If none is specified, we print to stdout",
    )
    parser.add_argument(
        "-io",
        "--inner_output",
        help="The desired output file for the inner graph. If none is specified, we ignore this.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Adapted from https://github.com/nineisprime/PAPER/blob/f11d95cbdeb319130cbcb20e4a220912951781cd/PAPER/tree_tools.py#L298-L308.
    (igraph, _) = createPATree(n=args.nodes, alpha=args.alpha, beta=args.beta, K=args.k)
    addRandomEdges(igraph, m=args.edges)

    # We preserve the type information on the internal igraph
    igraph.es["tree"] = True
    igraph.es[(args.nodes - args.k) :]["tree"] = False

    # and build two networkx graphs:
    # the whole graph (including Erdős–Rényi edges)
    graph = igraph.to_networkx()

    # and our our affine-preferential-attachment-generated trees (marked as 'tree' above)
    tree_graph = nx.from_edgelist(
        [(u, v) for u, v, e in graph.edges(data=True) if e["tree"]]
    )

    nx.write_edgelist(graph, args.output if args.output else sys.stdout, data=False)

    if args.inner_output:
        nx.write_edgelist(tree_graph, args.inner_output, data=False)

if __name__ == "__main__":
    main()
