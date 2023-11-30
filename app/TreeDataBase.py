import pickle
import uuid as uuid
from typing import Dict, Tuple, List, Union, Callable
import os


class TreeNode(object):
    """
    Represents a node in a hierarchical tree structure.

    This class provides functionalities to create tree nodes with unique identifiers,
    add children nodes, update, find, and delete nodes based on specific queries, and
    print the tree structure in a readable format.

    Attributes:
        id (UUID): A unique identifier for the node.
        data (Dict[str, any]): Data stored in the node.
        children (List[TreeNode]): A list of child nodes.
        node_identifier (NodeIdentifier): A unique identifier within the tree.

    Methods:
        add_child(child_node): Adds a child node to the current node.
        update_node(query, new_data): Updates the node specified by the query with new data.
        find_by_query(query): Finds and returns a node by a specific query.
        delete_node(query): Deletes a node specified by the query.
        insert_node(new_node_data, new_node_identifier): Inserts a new node with the given data and identifier.
        print_tree(indent, last): Prints the tree structure starting from this node.
        print_tree_no_ident(parent_identifier, indent, last): Prints the tree structure without repeating the full identifier of each node.
        get_tree_structure(): Returns a dictionary representing the tree structure starting from this node.
        is_valid_new_node_identifier(new_node_identifier): Validates a new node identifier.
        _extract_node_identifiers(): Extracts identifiers of all nodes in the subtree.
        _search(query_dict, current_level): Recursively searches for a node matching the query.
        _get_unique_part_of_identifier(parent_identifier): Extracts the unique part of the node's identifier relative to its parent.
        beauty_dict(): Returns a dictionary representation of the node.
    """

    def __init__(self, data: Dict[str, any], node_identifier: str):
        """
        Constructs all the necessary attributes for the TreeNode object.

        Parameters:
            data (Dict[str, any]): Data to be stored in the node.
            node_identifier (str): The identifier for the node.
        """
        self.id = uuid.uuid4()
        self.data = data
        self.children: List["TreeNode"] = []
        self.node_identifier = NodeIdentifier(node_identifier)

    # @staticmethod
    def is_valid_new_node_identifier(self, new_node_identifier: str) -> bool:
        """
        Validates if a new node identifier is valid.

        Parameters:
            new_node_identifier (str): The identifier to be validated.

        Returns:
            bool: True if valid, False otherwise.
        """
        # Basic validation: new_node_identifier should start with the root node's key
        root_key = next(
            iter(self.node_identifier)
        )  # Get the first key of the root node
        return new_node_identifier.startswith(f"{root_key}=")

    def add_child(self, child_node) -> None:
        """
        Adds a child node to this node.

        Parameters:
            child_node (TreeNode): The child node to be added.
        """
        self.children.append(child_node)

    def _extract_node_identifiers(self) -> List["NodeIdentifier"]:
        identifiers = [self.node_identifier]
        for child in self.children:
            identifiers.extend(child._extract_node_identifiers())
        return identifiers

    def get_all_children(self) -> List["TreeNode"]:
        children = [self.beauty_dict()]
        for child in self.children:
            children.extend(child.get_all_children())

        return children

    def update_node(self, query: str, new_data: Dict[str, any]) -> Tuple[bool, str]:
        """
        Updates the data of a node specified by a query.

        Parameters:
            query (str): The query to identify the node.
            new_data (Dict[str, any]): The new data for the node.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success or failure, and a message.
        """
        node = self.find_by_query(query)
        if node:
            node.data = new_data
            return True, "Node updated successfully."
        return False, "Node not found."

    def find_by_query(self, query: str) -> "TreeNode":
        node_idx = NodeIdentifier(query)
        return self._search(node_idx)

    def _search(self, query_dict: "NodeIdentifier", current_level=0) -> "TreeNode":
        if all(self.node_identifier.get(k) == v for k, v in query_dict.items()):
            return self

        for child in self.children:
            result = child._search(query_dict, current_level + 1)
            if result:
                return result
        return None

    def delete_node(self, query):
        def _delete_node(parent: TreeNode, query: str):
            for i, child in enumerate(parent.children):
                if (
                    child.node_identifier.get_current_level_identifier()
                    == NodeIdentifier(query).get_current_level_identifier()
                ):
                    del parent.children[i]
                    return True
                if _delete_node(child, query):
                    return True
            return False

        if self.find_by_query(query):
            if _delete_node(self, query):
                return True, "Node deleted successfully."
        return False, "Node not found."

    def insert_node(
        self, new_node_data: Dict[str, any], new_node_identifier: str
    ) -> Tuple[bool, str]:
        # Validate the new node's identifier
        if not self.is_valid_new_node_identifier(new_node_identifier):
            return False, "Invalid new node identifier."

        new_node_identifier_dict = NodeIdentifier(new_node_identifier)

        (
            *parent_identifier_items,
            new_node_own_identifier,
        ) = new_node_identifier_dict.items()
        parent_identifier = ",".join([f"{k}={v}" for k, v in parent_identifier_items])

        parent_node = self.find_by_query(parent_identifier)
        if not parent_node:
            return False, "Parent node not found."

        if new_node_identifier_dict in self._extract_node_identifiers():
            return False, "A node with this identifier already exists."

        new_node = TreeNode(new_node_data, new_node_identifier)
        parent_node.add_child(new_node)
        return True, "Node inserted successfully."

    def __str__(self) -> str:
        return f"TreeNode(id={self.id}, data={self.data}, node_identifier={self.node_identifier})"

    def beauty_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "data": self.data,
            "node_id": self.node_identifier,
        }

    def print_tree(self, indent="", last=True):
        # Convert the node_identifier dictionary back to string for printing
        identifier_str = ",".join([f"{k}={v}" for k, v in self.node_identifier.items()])

        # Print the current node
        prefix = "└── " if last else "├── "
        print(f"{indent}{prefix}{identifier_str}")

        indent += "    " if last else "│   "
        child_count = len(self.children)
        for i, child in enumerate(self.children):
            child.print_tree(indent, i == child_count - 1)

    def print_tree_no_ident(self, parent_identifier=None, indent="", last=True):
        # Isolate the unique part of the current node's identifier
        unique_identifier = self._get_unique_part_of_identifier(parent_identifier)

        # Print the current node
        prefix = "└── " if last else "├── "
        print(f"{indent}{prefix}{unique_identifier}")

        # Prepare for the next level
        full_identifier = ",".join(
            [f"{k}={v}" for k, v in self.node_identifier.items()]
        )
        indent += "    " if last else "│   "
        child_count = len(self.children)
        for i, child in enumerate(self.children):
            child.print_tree_no_ident(full_identifier, indent, i == child_count - 1)

    def get_tree_structure(self):
        # Create a dictionary for this node
        node_dict = {}

        # The value for this node's key will be a dictionary if it has children,
        # or a list if it's a leaf node
        if self.children:
            for child in self.children:
                # Recursively get the dictionary for each child and add it to the node's dictionary
                node_dict[
                    child.node_identifier.get_current_level_identifier()
                ] = child.get_tree_structure()
        else:
            # If there are no children, this is a leaf node, so use a list (or another appropriate value)
            node_dict = []  # Or any other value you wish to assign to leaf nodes

        return node_dict

    def _get_unique_part_of_identifier(self, parent_identifier):
        if parent_identifier:
            parent_parts = set(parent_identifier.split(","))
            child_parts = set(
                ",".join([f"{k}={v}" for k, v in self.node_identifier.items()]).split(
                    ","
                )
            )
            unique_parts = child_parts - parent_parts
            return ",".join(sorted(unique_parts))
        else:
            return ",".join([f"{k}={v}" for k, v in self.node_identifier.items()])


class NodeIdentifier:
    """
    Represents a unique identifier for nodes in a tree structure.

    This class is used to manage and manipulate node identifiers, which are essential for
    locating and differentiating nodes within a tree. It provides functionalities for parsing
    identifiers, comparing them, and retrieving specific parts of an identifier.

    Attributes:
        node_identifier (Dict[str, str]): A dictionary representing the parsed node identifier.

    Methods:
        get_current_level_identifier(): Returns the identifier of the current level of the node.
        __str__(): Returns a string representation of the node identifier.
        __eq__(other): Checks equality with another NodeIdentifier.
        __hash__(): Returns the hash of the node identifier.
        get(key): Retrieves the value for a given key in the node identifier.
        items(): Returns a list of tuples (key, value) in the node identifier.
        __iter__(): Returns an iterator over the node identifier.
        __next__(): Returns the next item from the node identifier iterator.
        parse_identifier(identifier): Parses a string identifier into a dictionary.
        from_tuples(tuples): Sets the node identifier from a list of key-value tuples.

    The class supports string representation and equality comparison, allowing for easy manipulation
    and use in various tree operations. The identifier is typically structured as a comma-separated
    string of key-value pairs, which are parsed into a dictionary for efficient access and manipulation.
    """

    def __init__(self, node_identifier: str = None):
        if node_identifier is None:
            self.node_identifier = {}
        else:
            self.node_identifier = self.parse_identifier(node_identifier)

    def get_current_level_identifier(self):
        last_key = list(self.node_identifier.keys())[-1]
        return f"{last_key}={self.node_identifier[last_key]}"

    def __str__(self):
        return ",".join([f"{k}={v}" for k, v in self.node_identifier.items()])

    def __eq__(self, other):
        return self.node_identifier == other.node_identifier

    def __hash__(self):
        return hash(str(self))

    def get(self, key) -> Union[str, None]:
        return self.node_identifier.get(key)

    def items(self):
        return self.node_identifier.items()

    def __iter__(self):
        return self.node_identifier.__iter__()

    def __next__(self):
        return self.node_identifier.__next__()

    @staticmethod
    def parse_identifier(identifier: str) -> Dict[str, str]:
        return dict(kv.split("=") for kv in identifier.split(","))

    def from_tuples(self, tuples: List[Tuple[str, str]]):
        self.node_identifier = dict(tuples)
        return self


class TreeDataBase:
    """
    Manages a tree database, allowing for creation, manipulation, and storage of a tree structure.

    This class encapsulates the functionality to create a tree, insert, update, delete, and query nodes,
    and manage the persistence of the tree structure using file operations.

    Attributes:
        root (Union[TreeNode, None]): The root node of the tree.
        db_path (str): The file path for saving the tree structure.

    Methods:
        create_tree_db(path, data, node_identifier): Initializes the tree with a root node and sets the file path for the database.
        insert(new_node_data, new_node_identifier): Inserts a new node with the given data and identifier.
        get_all_children(): Retrieves all child nodes of the tree.
        update(query, new_data): Updates a node specified by a query with new data.
        query(query): Finds and returns a node based on a specific query.
        delete(query): Deletes a node specified by a query.
        get_tree(): Returns the entire tree structure.
        print_tree(): Prints the tree structure in a readable format.
        print_tree_no_ident(): Prints the tree structure without repeating the full identifier of each node.
        save_tree(filename): Saves the current tree structure to a file.
        load_from_file(filename, root_id): Loads a tree structure from a file, optionally initializing a new tree if the file does not exist.
        pickle_obj_load(pickle): Loads a tree structure from a pickle object.
        save_cb(): Callback function to save the tree structure to the database file.

    The class supports operations for managing a hierarchical tree structure with complex node identifiers
    and provides mechanisms for persistent storage and retrieval of the tree data.
    """

    def __init__(
        self,
    ):
        self.root: Union["TreeNode", None] = None

    def create_tree_db(self, path, data, node_identifier):
        self.root = TreeNode(data, node_identifier)
        self.db_path = path
        self.save_tree(path)

    def insert(
        self, new_node_data: Dict[str, any], new_node_identifier: str
    ) -> Tuple[bool, str]:
        success, message = self.root.insert_node(new_node_data, new_node_identifier)
        if success and self.save_cb:
            self.save_cb()
        return success, message

    def get_all_children(self):
        return self.root.get_all_children()

    def update(self, query: str, new_data: Dict[str, any]) -> Tuple[bool, str]:
        success, message = self.root.update_node(query, new_data)
        if success and self.save_cb:
            self.save_cb()
        return success, message

    def query(self, query: str) -> "TreeNode":
        return self.root.find_by_query(query)

    def delete(self, query):
        success, message = self.root.delete_node(query)
        if success and self.save_cb:
            self.save_cb()
        return success, message

    def get_tree(self):
        return self.root.get_tree_structure()

    def print_tree(self):
        self.root.print_tree()

    def print_tree_no_ident(self):
        self.root.print_tree_no_ident()

    def save_tree(self, filename):
        # save_tree(self.root, filename)
        with open(filename, "wb") as file:
            pickle.dump(self.root, file)

    def load_from_file(self, filename, root_id=None):
        self.db_path = filename
        if not self.db_path:
            return False
        if not os.path.exists(self.db_path):
            if root_id is not None:
                self.root = TreeNode({}, root_id)
                self.save_tree(self.db_path)
            else:
                return False

        with open(self.db_path, "rb") as file:
            self.root = pickle.load(file)

        return True

    def pickle_obj_load(self, pickle):
        self.root = pickle

    def save_cb(self):
        if self.db_path:
            self.save_tree(self.db_path)
