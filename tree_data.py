"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        for subtree in self._subtrees:
            subtree._parent_tree = self
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.data_size = data_size
        if len(self._subtrees) != 0 and data_size == 0:
            for subtree in self._subtrees:
                self.data_size += subtree.data_size

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
        @rtype: bool

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t.is_empty()
        False
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> rect = t.generate_treemap((0, 0, 1024, 738))
        >>> rect[0][0]
        (0, 0, 384, 738)
        """
        if self.data_size == 0:  # Represents a tree with size 0
            return []
        elif len(self._subtrees) == 0:  # Represents a leaf
            return [(rect, self.colour)]
        else:
            new_rect = []
            current_space = 0
            subtree_count = 0
            for subtree in self._subtrees:
                if rect[2] > rect[3]:  # --> Vertical Rectangles
                    width = int((subtree.data_size / self.data_size) * rect[2])
                    x = int(rect[0] + current_space)
                    height = int(rect[3])
                    y = int(rect[1])
                    width = self._extend_height(False, subtree_count, rect,
                                                current_space, width)
                    new_rect += subtree.generate_treemap((x, y, width, height))
                    current_space += width
                    subtree_count += 1
                else:  # rect[2] <= rect[3] --> Horizontal Rectangles
                    height = int((subtree.data_size / self.data_size) * rect[3])
                    y = int(rect[1] + current_space)
                    width = int(rect[2])
                    x = int(rect[0])
                    height = self._extend_height(True, subtree_count, rect,
                                                 current_space, height)
                    new_rect += subtree.generate_treemap((x, y, width, height))
                    current_space += height
                    subtree_count += 1
            return new_rect

    def _extend_height(self, height_or_width, subtree_count, rect,
                       current_space, length):
        """ Returns the height of the Tree.  Extends the height in some
        cases to avoid gaps forming.

        @type self: AbstractTree
        @type height_or_width: Bool
            True if height must be modified.  False if width must be modified.
        @type subtree_count: int
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @type current_space: int
        @type length: int
            Either the height or the width.
        @rtype: int
        """
        if subtree_count == len(self._subtrees) - 1:
            if height_or_width:
                return math.ceil(rect[1] + rect[3] - current_space)
            else:
                return math.ceil(rect[0] + rect[2] - current_space)
        return length

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError

    def get_text(self, location, treemap):
        """ Returns the text to display when a user clicks a certain rectangle
        on the pygame screen, as well as the AbstractTree that was clicked.

        @type self: AbstractTree
        @type location: (int, int)
        @type treemap: list[((int, int, int, int), (int, int, int))]
        @rtype: tuple(str, AbstractTree)

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t.get_text((0, 0), t.generate_treemap(0, 0, 1024, 738))
        '/B/A/f1.txt'
        """
        tree_number = 0
        for index, rectangle in enumerate(treemap):
            if location[0] in range(rectangle[0][0], rectangle[0][0] +
                                    rectangle[0][2]) and \
                            location[1] in range(rectangle[0][1],
                                                 rectangle[0][1] + rectangle[0][
                                                     3]):
                tree_number = index
                break

        tree_from_number = self._get_tree_from_number(tree_number)
        assert tree_from_number is not None, 'tree_from_number is None!'
        tree_size = tree_from_number.data_size
        return (tree_from_number.get_text_from_tree() + tree_from_number._root
                + ' (' + str(tree_size) + ')',
                tree_from_number)

    def get_text_from_tree(self):
        """ Returns required text based on the seleted AbstractTree.

        @type self: AbstractTree
        @rtype: str

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t._subtrees[0].get_text_from_tree()
        'B/'
        """
        if self._parent_tree is None:
            return ''
        else:
            tree_path = self._parent_tree._root
            tree_path = self._parent_tree.get_text_from_tree() + tree_path \
                + self.get_separator()
            return tree_path

    def _get_tree_from_number(self, tree_number):
        """ Returns a tree based on the position of the tree in the rectangle
        list.

        This is a recursive method.

        Preconditions: - 0 <= tree_number < Number of leaves in the tree
                       - self isn't empty.

        @type self:  AbstractTree
        @type tree_number: int
        @rtype: AbstractTree

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> tree._get_tree_from_number(1)._root
        'f1'
        >>> tree._get_tree_from_number(2)._root
        'f2'
        >>> tree._get_tree_from_number(3)._root
        'f3'
        >>> tree._get_tree_from_number(4)._root
        'f4'
        """
        if len(self._subtrees) == 0 and tree_number == 0:
            return self
        else:
            for subtree in self._subtrees:
                subtree_sum = subtree._get_subtree_leaf_sum()
                previous_subtree_sum = subtree_sum - subtree._number_of_leaves()
                if previous_subtree_sum < tree_number + 1 <= subtree_sum:
                    return subtree._get_tree_from_number(tree_number -
                                                         previous_subtree_sum)
            for subtree in self._subtrees:
                if len(subtree._subtrees) == 0:
                    if tree_number == 0:
                        return subtree
                    else:
                        tree_number -= 1
                else:
                    tree_number -= subtree._number_of_leaves()

    def _number_of_leaves(self, count=0):
        """ Returns the number of leaves of a Tree.

        This is a recursive method.

        @type self: FileSystemTree
        @rtype: int

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t._number_of_leaves()
        4
        """
        for subtree in self._subtrees:
            if len(subtree._subtrees) == 0:
                count += 1
            else:
                count += subtree._number_of_leaves(count)
        assert count is not None, '_number_of_leaves returns None.'
        return count

    def _get_subtree_leaf_sum(self):
        """ Returns the number of leaves in each subtree that comes before this
        subtree in the _parent_tree's _subtree list, plus the number of leaves
        in this subtree.

        @type self: AbstractTree
        @rtype: int

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t._subtrees[1]._get_subtree_leaf_sum()
        3
        """
        subtree_sum = 0
        subtree_index = self._parent_tree._subtrees.index(self)
        for subtree in self._parent_tree._subtrees[:subtree_index + 1]:
            subtree_sum += subtree._number_of_leaves()
        assert subtree_sum is not None, '_get_subtree_leaf_sum returns None.'
        return subtree_sum

    def remove_leaf(self, location, treemap):
        """ Removes the leaf in the AbstractTree at the specified location.

        Returns the AbstractTree without the deleted leaf.

        @type self: AbstractTree
        @type location: (int, int)
        @type treemap: list[((int, int, int, int), (int, int, int))]
        @rtype: AbstractTree
        """
        tree_number = 0
        for index, rectangle in enumerate(treemap):
            if location[0] in range(rectangle[0][0], rectangle[0][0] +
                                    rectangle[0][2]) and \
                            location[1] in range(rectangle[0][1],
                                                 rectangle[0][1] + rectangle[0][
                                                     3]):
                tree_number = index
                break

        deleted_leaf = self._get_tree_from_number(tree_number)
        assert deleted_leaf is not None, 'tree_from_number is None!'
        new_tree = self
        new_tree._delete_leaf(deleted_leaf)
        return new_tree

    def _delete_leaf(self, deleted_leaf):
        """ Deletes the specified leaf from the AbstractTree.

        @type self: AbstractTree
        @type deleted_leaf: AbstractTree
        @rtype: None
        """
        for subtree in self._subtrees:
            if subtree == deleted_leaf:
                subtree._change_data_sizes(subtree.data_size, False)
                self._subtrees.remove(subtree)
            else:
                subtree._delete_leaf(deleted_leaf)

    def _change_data_sizes(self, changed_data_size, add_or_subtract):
        """ Adjusts the data sizes of other AbstractTrees in the AbstractTree
        that contains the tree that is going to be removed.

        @type self: AbstractTree
        @type changed_data_size: int
        @type add_or_subtract: Bool
        - Addition is performed if True.  Subtraction otherwise.
        @rtype: None
        """
        if self._parent_tree is not None:
            if add_or_subtract:
                self._parent_tree.data_size += changed_data_size
            else:
                self._parent_tree.data_size -= changed_data_size
            self._parent_tree._change_data_sizes(changed_data_size,
                                                 add_or_subtract)
        else:
            return None

    def change_leaf_size(self, selected_leaf, up_or_down):
        """ Increases the data size attribute of selected_leaf, and modifies the
        data sizes of other AbstractTrees in the AbstractTree that contains
        selected_leaf.

        @type self: AbstractTree
        @type selected_leaf: AbstractTree
        @type up_or_down: Bool
        - Upsized if True.  Downsized otherwise.
        @rtype: AbstractTree
        """
        if self.data_size <= 1:
            return self
        for index, subtree in enumerate(self._subtrees):
            if subtree == selected_leaf:
                changed_size = int(0.01 * subtree.data_size)
                if up_or_down:
                    self._subtrees[index].data_size += changed_size
                    subtree._change_data_sizes(changed_size, True)
                else:
                    self._subtrees[index].data_size -= changed_size
                    subtree._change_data_sizes(changed_size, False)
            else:
                subtree.change_leaf_size(selected_leaf, up_or_down)
        return self


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None

        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t._root
        B
        """
        root = os.path.basename(path)
        subtrees = []
        data_size = os.path.getsize(path)
        if os.path.isdir(path):
            for filename in os.listdir(path):
                subitem = os.path.join(path, filename)
                new_tree = FileSystemTree(subitem)
                subtrees.append(new_tree)
        super().__init__(root, subtrees, data_size)

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        @type self: FileSystemTree
        @rtype: str
        >>> t = FileSystemTree('C:\\Users\\HP\\Documents\\Year '\
        '1\\CSC148\\assignments\\a2\\B')
        >>> t.get_separator()
        '/'
        """
        return '/'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
