class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Newly added node starts with a height of 1

class BalancedTree:
    def __init__(self):
        self.root = None  # Initial tree root is empty

    def insert(self, value):
        self.root = self._insert_node(self.root, value)

    def delete(self, value):
        self.root = self._delete_node(self.root, value)

    def search(self, root, value):
        if not root or root.value == value:
            return root
        elif value < root.value:
            return self.search(root.left, value)
        return self.search(root.right, value)

    def inorder(self):
        return self._inorder_traversal(self.root, [])

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        # Update heights
        node.height = max(self._height(node.left), self._height(node.right)) + 1
        new_root.height = max(self._height(new_root.left), self._height(new_root.right)) + 1
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        # Update heights
        node.height = max(self._height(node.left), self._height(node.right)) + 1
        new_root.height = max(self._height(new_root.left), self._height(new_root.right)) + 1
        return new_root

    def _insert_node(self, current, value):
        if not current:
            return TreeNode(value)
        elif value < current.value:
            current.left = self._insert_node(current.left, value)
        else:
            current.right = self._insert_node(current.right, value)

        # Update height of the ancestor node
        current.height = 1 + max(self._height(current.left), self._height(current.right))

        # Rebalance the tree if necessary
        balance = self._balance_factor(current)

        # Left-heavy situations
        if balance > 1:
            if value < current.left.value:
                return self._rotate_right(current)  # Left-Left Case
            else:
                current.left = self._rotate_left(current.left)  # Left-Right Case
                return self._rotate_right(current)

        # Right-heavy situations
        if balance < -1:
            if value > current.right.value:
                return self._rotate_left(current)  # Right-Right Case
            else:
                current.right = self._rotate_right(current.right)  # Right-Left Case
                return self._rotate_left(current)

        return current

    def _delete_node(self, root, value):
        if not root:
            return root

        elif value < root.value:
            root.left = self._delete_node(root.left, value)

        elif value > root.value:
            root.right = self._delete_node(root.right, value)

        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self._find_min_node(root.right)
            root.value = temp.value
            root.right = self._delete_node(root.right, temp.value)

        if not root:
            return root

        # Update height and rebalance
        root.height = 1 + max(self._height(root.left), self._height(root.right))
        balance = self._balance_factor(root)

        # Left-heavy situations
        if balance > 1:
            if self._balance_factor(root.left) >= 0:
                return self._rotate_right(root)  # Left-Left Case
            else:
                root.left = self._rotate_left(root.left)  # Left-Right Case
                return self._rotate_right(root)

        # Right-heavy situations
        if balance < -1:
            if self._balance_factor(root.right) <= 0:
                return self._rotate_left(root)  # Right-Right Case
            else:
                root.right = self._rotate_right(root.right)  # Right-Left Case
                return self._rotate_left(root)

        return root

    def _find_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)
        return result

# Testing the BalancedTree (AVL Tree) implementation
tree = BalancedTree()
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(40)
tree.insert(50)
tree.insert(25)

# Print inorder traversal of the AVL tree
print("Inorder traversal:", tree.inorder())

# Search for a node
print("Search for 30:", "Found" if tree.search(tree.root, 30) else "Not found")
print("Search for 100:", "Found" if tree.search(tree.root, 100) else "Not found")

# Delete nodes
tree.delete(50)
print("Inorder traversal after deleting 50:", tree.inorder())

tree.delete(30)
print("Inorder traversal after deleting 30:", tree.inorder())
