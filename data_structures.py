class Node:
    def __init__(self, obj):
        super().__setattr__("obj", obj)
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
        return str(self.obj)

class Stack:
    def __init__(self):
        self.top_node = None
    def peek(self):
        return self.top_node.obj if self.top_node is not None else None
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


