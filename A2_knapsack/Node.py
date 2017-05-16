
class TreeNode:
    def __init__(self):
        self.isRoot = False
        self.parrent = None
        self.potential = 0
        self.weight = 0
        self.left = None
        self.right = None
        self.value = None
        self.depth = 0

    def __lt__(self, other):
        return self.depth > other.depth
