"""
# Zach Roth
# CS302
# Fall 2022
# Assignment 4 & 5

This file contains the data structures that make up the program database.
Four classes: Node and Linked_List, and Tree_Node and Tree. Many basic operations
are provided in order to perform their perspective roles.
"""

import collections

class Node:
    def __init__(self, data, next=None):
        self._data = data
        self._next = next
        self._active = True

    def set_next(self, next):
        if isinstance(next, Node):
            self._next = next

    def get_next(self):
        if self._next:
            return self._next
        else:
            return None

    def get_data(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self._data)

    def __eq__(self, other):
        if self._data == other:
            return True
        else:
            return False

    def __ne__(self, other):
        if self._data != other:
            return True
        else:
            return False

    def __lt__(self, other):
        if self._data < other.get_data():
            return True
        else:
            return False

    def __ge__(self, other):
        if self._data >= other.get_data():
            return True
        else:
            return False

class Linked_List:
    def __init__(self, head=None):
        self._head = head

    def __iter__(self):
        head = self._head
        while head is not None:
            yield head
            head = head.get_next()

    def __str__(self):
        head = self._head
        nodes = []
        while head is not None:
            nodes.append(repr(head))
            head = head.get_next()
        return "\n".join(nodes)

    def get_head(self):
        return self._head

    def append(self, data):
        self._head = self.append_helper(self._head, data)

    def append_helper(self, head, data):
        if head is None:
            return Node(data)
        else:
            head.next = self.append_helper(head.get_next(), data)

        return head

    def sort(self):
        collected_data = []
        head = self._head
        # feed nodes into list
        while head is not None:
            collected_data.append(head._data)
            head = head.get_next()

        # sort nodes
        collected_data.sort()

        # store sorted nodes into deque
        sorted_data = collections.deque(collected_data)

        # feed sorted nodes back into linked list
        head = self._head
        while head is not None:
            head._data = sorted_data.popleft()
            head = head.get_next()

    def search(self, head, target):
        if head is None:
            return False

        if head.get_data() == target:
            return True

        return self.search(head.get_next(), target)

    def retrieve(self, target):
        if self._head is None:
            return None

        result = self.retrieve_helper(self._head, target)

        return result

    def retrieve_helper(self, head, target):
        if head is None:
            return None
        print(head.get_next())
        print(target)
        if head.get_data() == target:
            return head

        return self.retrieve_helper(head.get_next(), target)

    def remove(self, target):
        if self.search(self._head, target) is True:
            self._head = self.remove_helper(self._head, target)
            return True
        else:
            return False

    def remove_helper(self, head, target):
        if head is None:
            return None
        elif head.get_data() == target:
            return head.get_next()
        else:
            head._next = self.remove_helper(head.get_next(), target)
            return head


class Tree_Node:
    def __init__(self, d, left=None, right=None):
        self._e_info = d  # event info
        self._comment_list = Linked_List()
        self._left = left
        self._right = right

    def get_e_info(self):
        return self._e_info

    def get_comment_list(self):
        return self._comment_list.get_head()

    def get_left(self):
        if self._left:
            return self._left
        else:
            return None

    def get_right(self):
        if self._right:
            return self._right
        else:
            return None

    def set_left(self, left):
        if isinstance(left, Tree_Node):
            self._left = left

    def set_right(self, right):
        if isinstance(right, Tree_Node):
            self._right = right

    def add_comment(self, comment):
        self._comment_list.append(comment)

    def display_comments(self):
        print(self._comment_list)

    def __str__(self):
        return (f'{self._e_info}\n'
                f'Comments:\n{self._comment_list}')

    def __repr__(self):
        return (f' {self._e_info}'
                f' {self._comment_list}')

    def __lt__(self, other):
        if other.data < self._e_info:
            return True
        else:
            return False

    def __ge__(self, other):
        if other.data >= self._e_info:
            return True
        else:
            return False

class Tree:
    def __init__(self, root=None):
        self._root = root

    # add node wrapper function
    def add_tree_node(self, list_node_data):  # data is a Node
        if self._root is None:
            self._root = Tree_Node(list_node_data)
        else:
            self._root = self.add_helper(self._root, list_node_data)

    # add node helper function
    def add_helper(self, root, list_node_data):
        if root is None:
            return Tree_Node(list_node_data)
        else:
            print(list_node_data)
            print(root.get_e_info())
            if list_node_data < root.get_e_info():
                root._left = self.add_helper(root._left, list_node_data)

            if list_node_data >= root.get_e_info():
                root._right = self.add_helper(root._right, list_node_data)

            return root

    # find node wrapper function
    def find_tree_node(self, list_node_data):
        if self._root is None:
            return None

        result = self.find_helper(self._root, list_node_data)

        return result

    # find node helper function
    def find_helper(self, root, target):
        if root is None:
            return None


        if root.get_e_info() == target:
            return root

        root.left = self.find_helper(root.get_left(), target)
        root.right = self.find_helper(root.get_right(), target)

        return root

    # print comment list
    def display_tree_node_comments(self, tree_node):
        print(tree_node)

    def display_tree(self):
        if self._root is None:
            return

        self.display_tree_helper(self._root)

    def display_tree_helper(self, root):
        if root is None:
            return None

        print(root)
        self.display_tree_helper(root.get_left())
        self.display_tree_helper(root.get_right())
