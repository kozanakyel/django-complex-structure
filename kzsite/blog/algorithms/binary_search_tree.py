import dataclasses
from typing import Any, Optional


class DuplicateKeyError(Exception):
    def __init__(self, key: str) -> None:
        Exception.__init__(self, f"{key} already exists.")


@dataclasses.dataclass
class Node:
    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def search(self, key: Any) -> Optional[Node]:
        current = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        return None

    def insert(self, key: Any, data: Any) -> None:
        new_node = Node(key=key, data=data)
        parent: Optional[Node] = None
        current: Optional[Node] = self.root
        while current:  # walk step
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if replacing_node:
            replacing_node.parent = deleting_node.parent

    def delete(self, key: Any) -> None:
        if self.root and (deleting_node := self.search(key=key)):

            # Case 1: no child or Case 2a: only one right child
            if deleting_node.left is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # Case 2b: only one left left child
            elif deleting_node.right is None:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # Case 3: two children
            else:
                replacing_node = BinarySearchTree.get_leftmost(node=deleting_node.right)
                # The leftmost node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    self._transplant(
                        deleting_node=replacing_node,
                        replacing_node=replacing_node.right,
                    )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                
    @staticmethod
    def get_height(node: Node) -> int:
        if node.left and node.right:
            return max(
                BinarySearchTree.get_height(node=node.left),
                BinarySearchTree.get_height(node=node.right),
            ) + 1

        if node.left:
            return BinarySearchTree.get_height(node=node.left) + 1

        if node.right:
            return BinarySearchTree.get_height(node=node.right) + 1

        # If reach here, it means the node is a leaf node.
        return 0

    @staticmethod
    def get_leftmost(node: Node) -> Node:
        current_node = node
        while current_node.left:
            current_node = current_node.left
        return current_node
    
    @staticmethod
    def get_rightmost(node: Node) -> Node:
        current_node = node
        while current_node.right:
            current_node = current_node.right
        return current_node

    @staticmethod
    def get_predecessor(node: Node) -> Optional[Node]:
        if node.left:  # Case 1: left child is not empty
            return BinarySearchTree.get_rightmost(node=node.left)
        # Case 2: left child is empty
        parent = node.parent
        while parent and (node == parent.left):
            node = parent
            parent = parent.parent
        return parent
    
    @staticmethod
    def get_successor(node: Node) -> Optional[Node]:
        if node.right:  # Case 1: right child is not empty
            return BinarySearchTree.get_leftmost(node=node.right)
        # Case 2: right child is empty
        parent = node.parent
        while parent and (node == parent.right):
            node = parent
            parent = parent.parent
        return parent
    
    def __repr__(self) -> str:
        if self.root:
            return (
                f"{type(self)}, root={self.root}, "
                f"tree_height={str(self.get_height(self.root))}"
            )
        return "empty tree"
 
 
class Map:
    """Key-value Map implemented by the Binary Search Tree."""

    def __init__(self) -> None:
        self._bst = BinarySearchTree()

    def __setitem__(self, key: Any, value: Any) -> None:
        self._bst.insert(key=key, data=value)

    def __getitem__(self, key: Any) -> Optional[Any]:
        node = self._bst.search(key=key)
        if node:
            return node.data
        return None

    def __delitem__(self, key: Any) -> None:
        self._bst.delete(key=key)

    @property
    def empty(self) -> bool:
        """Return `True` if the map is empty; `False` otherwise."""
        return self._bst.empty

if __name__ == "__main__":

    # Initialize the Map instance.
    contacts = Map()

    # Add some items.
    contacts["Mark"] = "mark@email.com"
    contacts["John"] = "john@email.com"
    contacts["Luke"] = "luke@email.com"

    # Retrieve an email
    print(contacts["Mark"])

    # Delete one item.
    del contacts["John"]

    # Check the deleted item.
    print(contacts["John"])    