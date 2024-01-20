class Node:
    def __init__(self, data, left=None, right=None, parent=None, depth: int = None):
        self.left = left
        self.data = data
        self.right = right
        self.parent = parent
        self.depth = depth


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.val},L{self.left.val if self.left else ''},R{self.right.val if self.right else ''}"


def _tree() -> list[TreeNode]:
    """Returns nodes of an example tree
                0
            1_______7
          2___3______8
             4__________9
              _5_________10
            6_________11_
    Returns:
        list[TreeNode]: Tree Nodes, where r[0] is root
    """
    nodes = [TreeNode(i) for i in range(12)]
    root = nodes[0]
    root.right = nodes[7]
    root.right.right = nodes[8]
    root.right.right.right = nodes[9]
    root.right.right.right.right = nodes[10]
    root.right.right.right.right.left = nodes[11]
    root.left = nodes[1]
    root.left.left = nodes[2]
    root.left.right = nodes[3]
    root.left.right.left = nodes[4]
    root.left.right.left.right = nodes[5]
    root.left.right.left.right.left = nodes[6]
    return nodes


def _bsearch_tree() -> list[TreeNode]:
    """Returns nodes of an example binary search tree
                6
             3_____7
          2___5______8
        1___4__________9
          _0_____________10
    Returns:
        list[TreeNode]: Tree Nodes, where r[0] is root
    """
    nodes = [TreeNode(i) for i in range(11)]
    root = nodes[6]
    root.right = nodes[7]
    root.right.right = nodes[8]
    root.right.right.right = nodes[9]
    root.right.right.right.right = nodes[10]
    root.left = nodes[3]
    root.left.left = nodes[2]
    root.left.left.left = nodes[1]
    root.left.right = nodes[5]
    root.left.right.left = nodes[4]
    root.left.right.left.left = nodes[0]
    return nodes


def run_tests(fnc, test_cases) -> None:
    for i, case in enumerate(test_cases):
        ans = fnc(*case["in"])
        if ans != case["out"]:
            print(f"Test # {i+1} : Calculated {ans}, expected {case['out']}")
