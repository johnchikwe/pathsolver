from node import Node


class LLStack:  # stores singly linked list without tail
    """
    This is responsible for storing and managing the coordinates
    """

    def __init__(self):  # based off of a stack
        """
        Initializes head and size
        """
        self.__head = None
        self.__size = 0

    @property
    def size(self):
        """
        This property returns size of LLStack

        Returns:
             size (int): current size
        """
        return self.__size

    # removing the top node means removal from the head
    def pop(self):  # don't iterate because it's a stack
        """
        Responsible for popping the head

        Returns:
            popped (tuple): top of the LLStack
        """
        if self.__head is None:
            raise IndexError
        else:
            popped = self.__head.data
            self.__head = self.__head.next  # this action is what deletes the node
        self.__size -= 1
        return popped

    def push(self, data: tuple):
        """
        Responsible for adding coordinates to LLStack

        Parameters:
             data (tuple): Coordinates of the map

        Raises:
            TypeError: if value in tuple is not an integer
            ValueError: if value in tuple is less than 0 or length
            of data is not 2
        """
        for i in data:
            if not isinstance(i, int):
                raise TypeError('must be integer')
            if i < 0:
                raise ValueError

        if not len(data) == 2:
            raise ValueError

        node = Node(data, self.__head)  # passing reference of current head node to new one
        self.__head = node
        self.__size += 1

    def __str__(self):
        """
        Outputs the string reversed version of LLStack

        Returns:
             output (str): Reversed Linked List Stack
        """
        output = ""

        """
        the reversal is just using current tuple then adding previous tuple(s) around it
        """
        curr = self.__head  # curr always starts with head
        while curr:
            output = f"{curr.__str__()}" + " -> " + output
            curr = curr.next
        if output.endswith(" -> "):
            output = output[:-4]  # gets rid of the arrow and spaces around it

        return output


