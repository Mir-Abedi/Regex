# proj approach one using trie
import time


NUMBER_CHILDREN = 62 # 26 letters * 2 + 10 numbers

def get_index(c):
    if ord(c) >= ord('a') and ord(c) <= ord('z'):
        return ord(c) - ord('a')
    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
        return ord(c) - ord('A') + 26
    if ord(c) >= ord('0') and ord(c) <= ord('9'):
        return ord(c) - ord('0') + 52

    # check for none in return
    return None

def is_alpha_numeric(c):
    if ord(c) >= ord('a') and ord(c) <= ord('z'):
        return True
    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
        return True
    if ord(c) >= ord('0') and ord(c) <= ord('9'):
        return True
    return False

class Node(object):
    def __init__(self, parent, num_end, value):
        self.value = value
        self.children = [None for _ in range(NUMBER_CHILDREN)]
        self.parent = parent
        # num_end = number of strings that end with this character
        # for handling repeated inputs
        self.num_end = num_end
        self.full_children = [] # index of children that are not None
        self.q = -1 # to avoid repeated nodes in answer

def insert(root, string): # returns -1 if unsuccessful
    node = root
    i = 0
    for i in string:
        temp = get_index(i)
        if temp == None: # this is just in case
            # if happens often tree update is also needed
            return -1
        if node.children[temp] == None:
            node.children[temp] = Node(node, 0, i)
            node.full_children.append(temp)
        node = node.children[temp]
    node.num_end += 1
    return 1

def find(root, string): # returns (num_found, answer_nodes)
    global q_count
    if len(string) == 0:
        if root.q == q_count or root.num_end == 0:
            return (0, [])
        root.q = q_count
        return (root.num_end, [root])
    node = root
    for i in range(len(string)):
        if is_alpha_numeric(string[i]): # normal character
            if i + 1 >= len(string): # only one character
                if not node.children[get_index(string[i])]:
                    return (0, [])
                else:
                    node = node.children[get_index(string[i])]
            elif string[i + 1] == '*': # * character with normal character
                return call_star_on_children(node, string[i], string[i + 2:])
            else: # find one character
                if not node.children[get_index(string[i])]:
                    return (0, [])
                else:
                    node = node.children[get_index(string[i])]
        else: # '\' found
            if not string[i + 1] == 'S': # next character should be 'S'
                continue
            if i + 2 >= len(string): # only one \S
                return call_on_every_child(node, '')
            elif string[i + 2] == '*': # wildcard
                return call_on_subtree(node, string[i + 3:])
            else: # only one \S
                return call_on_every_child(node, string[i + 2:])
    if node.q == q_count or node.num_end == 0:
        return (0, [])
    node.q = q_count
    return (node.num_end, [node])

def call_star_on_children(node, character, string): # returns (num_found, answer_nodes)
    temp = get_index(character)
    num_found = 0
    arr_found = []
    while node:
        ans = find(node, string)
        num_found += ans[0]
        arr_found.extend(ans[1])
        node = node.children[temp]
    return (num_found, arr_found)

def call_on_every_child(node, string):
    num_found = 0
    arr_found = []
    for i in node.full_children:
        ans = find(node.children[i], string)
        num_found += ans[0]
        arr_found.extend(ans[1])
    return (num_found, arr_found)


def call_on_subtree(node, string): # calls find(string) on every possible child
    num_found = 0
    arr_found = []
    for i in node.full_children:
        ans = call_on_subtree(node.children[i], string)
        num_found += ans[0]
        arr_found.extend(ans[1])
    ans = find(node, string)
    num_found += ans[0]
    arr_found.extend(ans[1])
    return (num_found, arr_found)


def get_string_for_node(node):
    s = ''
    num = node.num_end
    while node.value != -1:
        s += node.value
        node = node.parent
    s = s[-1::-1]
    s += ' '
    return s * num


n, q = map(int, input().strip().split())

root = Node(None, 0, -1)
for i in input().strip().split():
    temp = insert(root, i)
    if temp == -1:
        print('Could not insert ' + i)

q_count = 0
start_time = time.time_ns()

for i in range(q):
    q_count = i
    query = input().strip()
    ans = find(root, query)
    # print(ans[0], end = ' ')
    for j in ans[1]:
        pass
        # print(get_string_for_node(j), end = '')
    # print('')

end_time = time.time_ns()
duration = (end_time - start_time)/1000000
print(duration)


