
# Note: This Queue class is sub-optimal. Why?
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class QueueLL:
    def __init__(self):
        self.size = 0
        # self.storage = []
        self.storage = LinkedList()

    def __len__(self):
        return self.size

    def enqueue(self, value):
        self.size += 1
        self.storage.append(value)

    def dequeue(self):
        if self.size > 0:
            self.size -= 1
            # return self.storage.pop(0)
            return self.storage.remove_head()
        else:
            return None

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def append(self, value):
        return self.add_to_tail(value)

    def push(self, value):
        return self.add_to_tail(value)

    def add_to_tail(self, value):
        new_node = Node(value)
        self.add_node_to_tail(new_node)
        self.length += 1
        return self.length

    def add_node_to_tail(self, node):
        if self.tail is not None:
            self.tail.next = node
        else:
            self.add_node_to_head(node)
        self.tail = node

    def unshift(self, value):
        return self.add_to_head(value)

    def add_node_to_head(self, node):
        if self.head is not None:
            node.next = self.head
        self.head = node

    def add_to_head(self, value):
        new_node = Node(value)
        self.add_node_to_head(new_node)
        self.length += 1
        return self.length

    def shift(self):
        return self.remove_head()

    def remove_head(self):
        value = None
        old_head = self.head
        if old_head is not None:
            if self.tail is old_head:
                self.tail = None
            if old_head.next is not None:
                self.head = old_head.next
            else:
                self.head = None
            value = old_head.value
            self.length -= 1
        return value

    def remove_tail(self):
        value = None
        old_tail = self.tail
        if old_tail is not None:
            i = self.head
            j = None
            while i is not old_tail:
                j = i
                i = i.next
            if j is not None:
                j.next = None
            self.tail = j
            value = old_tail.value
            self.length -= 1
            if self.head is old_tail:
                self.head = None
        return value

    def pop(self):
        return self.remove_tail()

    def remove(self, index):
        node = self.head
        last = self.head
        for i in range(1, index-1):
            node = node.next
            if i == index-1:
                node.next = node.next.next
        self.length -= 1
        return self.length

class StackLL:
    def __init__(self):
        self.size = 0
        #self.storage = []
        self.storage = LinkedList()

    def __len__(self):
        return self.size

    def push(self, value):
        self.size += 1
        return self.storage.append(value)

    def pop(self):
        if self.size > 0:
            self.size -= 1
            return self.storage.pop()
        else:
            return None

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
