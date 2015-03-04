import re
import argparse
import sys
from copy import deepcopy

def is_term(t):
    return re.match(r"[A-Z]+[0-9]*", t) is not None

def print_tree(node, level = 0):
    if node is not None:
        if type(node) is Node:
            print("." * 4 * level + node.root)
            for n in node.children:
                print_tree(n, level + 1)
        else:
            print("." * 4 * level + node)

class Node(object):
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def __repr__(self):
        return "{R: " + self.root + ", C: " + str(self.children) + "}"

def parse(astr):
    # Taken from Norvig's "(How to Write a (Lisp) Interpreter (in Python))"
    tokens = astr.replace("(", " ( ") \
                 .replace(")", " ) ") \
                 .replace("-", " - ") \
                 .split()
    op_stack = []
    out_stack = []

    for token in tokens:
        print(token)
        print(out_stack)
        print(op_stack)
        print("---")

        if is_term(token):
            out_stack.append(token)
        elif token == "-":
            op_stack.append(token)
        elif token in ["<=>",
                       "=>",
                       "|",
                       "&"]:
            while op_stack and op_stack[-1] == "-":
                try:
                    out_stack.append(Node(op_stack.pop(),
                                            [out_stack.pop()]))
                except:
                    print("Invalid format")
                    return

            op_stack.append(token)

        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                if op_stack[-1] == "-":
                    try:
                        out_stack.append(Node(op_stack.pop(),
                                              [out_stack.pop()]))
                    except:
                        print("Invalid format")
                        return

                else:
                    try:
                        out_stack.append(Node(op_stack.pop(),
                                             [out_stack.pop(),
                                             out_stack.pop()][::-1]))
                    except:
                        print("Invalid format")
                        return

            if op_stack:
                op_stack.pop()
            else:
                print("Mismatched parenthesis")
                return
        else:
            print("Invalid token:", token)
            return

    while op_stack:
        if op_stack[-1] != '(':
            out_stack.append(op_stack.pop())
        else:
            print("Mismatched parenthesis")
            return

    if len(out_stack) == 1:
        return out_stack[0]
    else:
        print("Invalid format")
        return

def trav1(node):
    if type(node) == Node:
        if node.root == "=>":
            node.root = "|"
            node.children[0] = Node("-", [node.children[0]])
        elif node.root == "<=>":
            node.root = "&"
            #node.children = [Node("=>", [node.children[0], node.children[1]]),
                             #Node("=>", [node.children[1], node.children[0]])]
            node.children = [Node("|", [Node("-", [node.children[0]]), node.children[1]]),
                             Node("|", [Node("-", [node.children[1]]), node.children[0]])]

        for n in node.children:
            trav1(n)

def cnfize(ast):
    trav1(ast)

def main(argv=None):
    if argv:
        astr = argv[0]

    ast = parse(astr)
    print(ast)
    print_tree(ast)
    cnfize(ast)
    print(ast)
    print_tree(ast)

if __name__ == "__main__":
    main(sys.argv[1:])
