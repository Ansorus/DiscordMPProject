class Node:
    def __init__(self, obj):
        super().__setattr__("reference", obj)
        super().__setattr__("connections", {})
    def __getattr__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self[item]
    def __getitem__(self, item):
        try:
            return self.connections[item]
        except KeyError:
            return None
    def __setattr__(self, key, value):
        try:
            super().__getattribute__(key)
            super().__setattr__(key, value)
        except AttributeError:
            self[key] = value
    def __setitem__(self, key, value):
        self.connections[key] = value
    def __str__(self):
        return str(self.reference)

# Search for obj
def search_from_head(head_to_search: Node, obj, return_index=False):
    node = head_to_search
    index = 0
    while True:
        if node.reference == obj:
            return (node, index) if return_index else node
        node = node.right
        index += 1
        if node is None:
            return None

class Stack:
    def __init__(self):
        self.top_node = None
    def peek(self):
        return self.top_node.reference if self.top_node is not None else None
    def push(self, obj):
        obj = obj if isinstance(obj, Node) else Node(obj)

        if self.top_node:
            self.top_node.up = obj
            obj.down = self.top_node

        self.top_node = obj
    def pop(self):
        if self.top_node:

            if self.top_node.down is not None:
                self.top_node = self.top_node.down
                self.top_node.up = None
                return

            del self.top_node
            self.top_node = None


