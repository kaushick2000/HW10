class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BasicBST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        # If tree is empty, create root
        if not self.root:
            self.root = Node(value)
            return

        # Find the right spot to insert
        current = self.root
        while True:
            # Go left
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    break
                current = current.left
            # Go right
            else:
                if current.right is None:
                    current.right = Node(value)
                    break
                current = current.right

    def search(self, value):
        current = self.root

        # Keep going until we hit a leaf or find the value
        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def print_inorder(self):
        def _inorder(node):
            if node:
                _inorder(node.left)
                print(node.value, end=' ')
                _inorder(node.right)

        _inorder(self.root)
        print()  # New line after printing

# Test the implementation
if __name__ == "__main__":
    # Create a BST
    bst = BasicBST()

    # Insert some numbers
    test_values = [5, 3, 7, 1, 4, 6, 8]
    print("Inserting values:", test_values)
    for value in test_values:
        bst.insert(value)

    # Print the tree in order
    print("Tree in-order traversal:", end=' ')
    bst.print_inorder()

    # Test searching
    print("\nTesting search:")
    for value in [4, 9]:
        if bst.search(value):
            print(f"{value} is in the tree")
        else:
            print(f"{value} is not in the tree")