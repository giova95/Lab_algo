import os
import random
import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd

sys.setrecursionlimit(100000)


class Node:
    def __init__(self, init_key):
        self.key = init_key
        self.next = None

    def get_key(self):
        return self.key

    def get_next(self):
        return self.next

    def set_key(self, new_key):
        self.key = new_key

    def set_next(self, new_next):
        self.next = new_next


class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def add_ordered(self, item):
        current = self.head
        previous = None
        stop = False
        while current is not None and not stop:
            if current.get_key() > item:
                stop = True
            else:
                previous = current
                current = current.get_next()

        temp = Node(item)
        if previous is None:
            temp.set_next(self.head)
            self.head = temp
        else:
            temp.set_next(current)
            previous.set_next(temp)

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.get_next()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.get_key() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def print_list(self):
        current = self.head
        while current is not None:
            print('..', current.get_key())
            current = current.get_next()

    def find_min_ordered(self):
        if self.is_empty():
            return None
        return self.head.get_key()

    def os_select_list(self, x, i):
        current = x
        i -= 1
        while current is not None and i > 0:
            current = current.get_next()
            i -= 1
        return current

    def os_rank_list(self, x):
        current = self.head
        rank = 0
        while current is not None:
            if current is x:
                return rank
            rank += 1
            current = current.get_next()
        return None


class NodeABR:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def get(self):
        return self.key

    def set(self, key):
        self.key = key

    def get_children(self):
        children = []
        if self.left is not None:
            children.append(self.left)
        if self.right is not None:
            children.append(self.right)
        return children


class ABR:
    def __init__(self):
        self.root = None

    def set_root(self, key):
        self.root = NodeABR(key)

    def insert_node(self, current_node, key):
        if key <= current_node.key:
            if current_node.left:
                self.insert_node(current_node.left, key)
            else:
                new_node = NodeABR(key)
                new_node.parent = current_node
                current_node.left = new_node
        elif key > current_node.key:
            if current_node.right:
                self.insert_node(current_node.right, key)
            else:
                new_node = NodeABR(key)
                new_node.parent = current_node
                current_node.right = new_node

    def insert(self, key):
        if self.root is None:
            self.set_root(key)
        else:
            self.insert_node(self.root, key)

    def find(self, key):
        return self.find_node(self.root, key)

    def find_node(self, current_node, key):
        if current_node is None:
            return False
        elif key == current_node.key:
            return True
        elif key < current_node.key:
            return self.find_node(current_node.left, key)
        else:
            return self.find_node(current_node.right, key)

    def inorder(self):
        def _inorder(v):
            if v is None:
                return
            if v.left is not None:
                _inorder(v.left)
            print(v.key)
            if v.right is not None:
                _inorder(v.right)

        _inorder(self.root)

    def os_select(self, x, i):
        if x is None:
            return None
        r = self.tree_size(x.left) + 1
        if i == r:
            return x
        elif i < r:
            return self.os_select(x.left, i)
        else:
            return self.os_select(x.right, i - r)

    def tree_size(self, node):
        def _inorder(v):
            if v is None:
                return 0
            left_size = _inorder(v.left)
            right_size = _inorder(v.right)
            return left_size + 1 + right_size

        return _inorder(node)

    def os_rank(self, T, x):
        if x is None:
            return None
        r = self.tree_size(x.left) + 1
        y = x
        while y != T.root:
            if y == y.parent.right:
                r += self.tree_size(y.parent.left) + 1
            y = y.parent
        return r


def main():
    struct_size = [10, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]

    select_list_times = []
    rank_list_times = []
    select_abr_times = []
    rank_abr_times = []

    for size in struct_size:
        linked_list = LinkedList()
        abr = ABR()

        for i in range(size):
            linked_list.add_ordered(1 * random.randint(0, size))
            abr.insert(1 * random.randint(0, size))

        # calcolo tempi: lista ordinata selezionando elemento pù grande
        select_list_time = timeit.timeit(lambda: linked_list.os_select_list(linked_list.head, size), number=5)
        rank_list_time = timeit.timeit(
            lambda: linked_list.os_rank_list(linked_list.os_select_list(linked_list.head, size)), number=5)
        select_list_times.append(select_list_time)
        rank_list_times.append(rank_list_time)

        # calcolo tempi: ABR selezionando elemento più grande
        select_abr_time = timeit.timeit(lambda: abr.os_select(abr.root, size), number=5)
        rank_abr_time = timeit.timeit(
            lambda: abr.os_rank(abr, abr.os_select(abr.root, size)), number=5)
        select_abr_times.append(select_abr_time)
        rank_abr_times.append(rank_abr_time)

    # preparazione e salvataggio tabelle: Lista Ordinata
    data_counting = pd.DataFrame({'Elementi': struct_size, 'Tempo(s)': select_list_times})
    data_counting['Tempo(s)'] = data_counting['Tempo(s)'].apply(
        lambda x: '{:.3e}'.format(x))
    data_counting = data_counting.iloc[1:]
    data_counting.style.set_properties(**{'text-align': 'center'})

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data_counting.values, colLabels=data_counting.columns, loc='center', cellLoc='center', rowLoc='center')
    ax.set_title('OS-Select Lista ordinata',
                 fontweight="bold")
    plt.savefig('select_list_table.png')
    plt.close()

    data_counting = pd.DataFrame({'Elementi': struct_size, 'Tempo(s)': rank_list_times})
    data_counting['Tempo(s)'] = data_counting['Tempo(s)'].apply(
        lambda x: '{:.3e}'.format(x))
    data_counting = data_counting.iloc[1:]
    data_counting.style.set_properties(**{'text-align': 'center'})
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data_counting.values, colLabels=data_counting.columns, loc='center', cellLoc='center',
             rowLoc='center')
    ax.set_title('OS-Select Lista ordinata',
                 fontweight="bold")
    plt.savefig('rank_list_table.png')
    plt.close()

    # disegno e salvataggio grafico prestazioni: Lista ordinata
    plt.plot(struct_size, select_list_times, label='OS-SELECT per lista ordinata', marker='o')
    plt.xlabel('Dimensione della lista')
    plt.ylabel('Tempo medio (secondi)')
    plt.legend()
    plt.savefig('select_list_plot.png')
    plt.close()

    plt.plot(struct_size, rank_list_times, label='OS-RANK per lista ordinata', marker='o')
    plt.xlabel('Dimensione della lista')
    plt.ylabel('Tempo medio (secondi)')
    plt.legend()
    plt.savefig('rank_list_plot.png')
    plt.close()

    # preparazione e salvataggio tabelle: ABR
    data_counting = pd.DataFrame({'Elementi': struct_size, 'Tempo(s)': select_abr_times})
    data_counting['Tempo(s)'] = data_counting['Tempo(s)'].apply(
        lambda x: '{:.3e}'.format(x))
    data_counting = data_counting.iloc[1:]
    data_counting.style.set_properties(**{'text-align': 'center'})
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data_counting.values, colLabels=data_counting.columns, loc='center', cellLoc='center',
             rowLoc='center')
    ax.set_title('OS-Select Lista ordinata',
                 fontweight="bold")
    plt.savefig('select_abr_table.png')
    plt.close()

    data_counting = pd.DataFrame({'Elementi': struct_size, 'Tempo(s)': rank_abr_times})
    data_counting['Tempo(s)'] = data_counting['Tempo(s)'].apply(
        lambda x: '{:.3e}'.format(x))
    data_counting = data_counting.iloc[1:]
    data_counting.style.set_properties(**{'text-align': 'center'})
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data_counting.values, colLabels=data_counting.columns, loc='center', cellLoc='center',
             rowLoc='center')
    ax.set_title('OS-Select Lista ordinata',
                 fontweight="bold")
    plt.savefig('rank_abr_table.png')
    plt.close()

    # disegno e salvataggio grafico prestazioni: ABR
    plt.plot(struct_size, select_abr_times, label='OS-SELECT per ABR', marker='o')
    plt.xlabel('Dimensione ABR')
    plt.ylabel('Tempo medio (secondi)')
    plt.legend()
    plt.savefig('select_abr_plot.png')
    plt.close()

    plt.plot(struct_size, rank_abr_times, label='OS-RANK per ABR', marker='o')
    plt.xlabel('Dimensione ABR')
    plt.ylabel('Tempo medio (secondi)')
    plt.legend()
    plt.savefig('rank_abr_plot.png')
    plt.close()


if __name__ == "__main__":
    main()
