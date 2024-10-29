class Node:
    def __init__(self, key):
        self.key = key
        self.red = True  # True for red, False for black
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None)
        self.nil.red = False
        self.root = self.nil

    def insert(self, key):
        """Insert a new key into the tree"""
        new_node = Node(key)
        new_node.left = self.nil
        new_node.right = self.nil

        # Standard BST insert
        parent = None
        current = self.root

        while current != self.nil:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insert(new_node)

    def _fix_insert(self, node):
        """Fix the tree after insertion"""
        while node != self.root and node.parent.red:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.red:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self._rotate_left(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle.red:
                    uncle.red = False
                    node.parent.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self._rotate_right(node.parent.parent)

        self.root.red = False

    def delete(self, key):
        """Delete a key from the tree"""
        node = self.search(key)
        if not node:
            return False

        y = node
        y_original_color = y.red

        if node.left == self.nil:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.red
            x = y.right

            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.red = node.red

        if not y_original_color:
            self._fix_delete(x)

        return True

    def _fix_delete(self, node):
        """Fix the tree after deletion"""
        while node != self.root and not node.red:
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.red:
                    sibling.red = False
                    node.parent.red = True
                    self._rotate_left(node.parent)
                    sibling = node.parent.right

                if not sibling.left.red and not sibling.right.red:
                    sibling.red = True
                    node = node.parent
                else:
                    if not sibling.right.red:
                        sibling.left.red = False
                        sibling.red = True
                        self._rotate_right(sibling)
                        sibling = node.parent.right

                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.right.red = False
                    self._rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.red:
                    sibling.red = False
                    node.parent.red = True
                    self._rotate_right(node.parent)
                    sibling = node.parent.left

                if not sibling.right.red and not sibling.left.red:
                    sibling.red = True
                    node = node.parent
                else:
                    if not sibling.left.red:
                        sibling.right.red = False
                        sibling.red = True
                        self._rotate_left(sibling)
                        sibling = node.parent.left

                    sibling.red = node.parent.red
                    node.parent.red = False
                    sibling.left.red = False
                    self._rotate_right(node.parent)
                    node = self.root

        node.red = False

    def search(self, key):
        """Search for a key in the tree"""
        node = self.root
        while node != self.nil and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node if node != self.nil else None

    def _rotate_left(self, node):
        """Perform left rotation"""
        right_child = node.right
        node.right = right_child.left

        if right_child.left != self.nil:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node):
        """Perform right rotation"""
        left_child = node.left
        node.left = left_child.right

        if left_child.right != self.nil:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def _transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v"""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """Find minimum key in subtree rooted at node"""
        while node.left != self.nil:
            node = node.left
        return node

    def inorder(self):
        """Return inorder traversal of the tree"""
        result = []
        def _inorder(node):
            if node != self.nil:
                _inorder(node.left)
                result.append((node.key, "Red" if node.red else "Black"))
                _inorder(node.right)
        _inorder(self.root)
        return result

def test_rbt():
    """Test the Red-Black Tree implementation"""
    print("Starting Red-Black Tree tests...")

    # Create tree
    tree = RedBlackTree()

    # Test 1: Insertion
    print("\nTest 1: Insertion")
    values = [7, 3, 18, 10, 22, 8, 11, 26]
    for val in values:
        tree.insert(val)
        print(f"Inserted {val}")

    print("\nInorder traversal after insertions:")
    print(tree.inorder())

    # Test 2: Search
    print("\nTest 2: Search")
    for val in [7, 18, 26, 100]:
        result = tree.search(val)
        print(f"Searching for {val}: {'Found' if result else 'Not found'}")

    # Test 3: Deletion
    print("\nTest 3: Deletion")
    delete_values = [18, 11, 7]
    for val in delete_values:
        success = tree.delete(val)
        print(f"Deleting {val}: {'Success' if success else 'Failed'}")

    print("\nInorder traversal after deletions:")
    print(tree.inorder())

if __name__ == "__main__":
    test_rbt()