from enum import Enum

from .tokens import TokenKind
from .scrbrd import NumberSBObj

class Node:
    def __init__(self, data, children=None, parent=None):
        self.data = data
        self.children = children or []
        self.parent = parent

        for child in self.children:
            child.parent = self


class BlockNode(Node):
    def __init__(self, statements):
        super().__init__((TokenKind.Block, "Block"), statements)


class BinaryNode(Node):
    def __init__(self, left, operator, right):
        super().__init__(("Binary", operator[0], operator[1]), [left, right])
        self.operator = operator
        self.left = left
        self.right = right


def traverse(root=None):
    if root is None:
        return

    print(root.data)
    for child in root.children:
        traverse(child)


def prettyTraverse(node, indent=0):
    if node is None:
        return

    if isinstance(node.data, tuple):
        label = node.data[0]
        payload = node.data[1:]
    else:
        label = node.data
        payload = ()

    payload_str = ""
    if payload:
        payload_str = " : " + ", ".join(map(str, payload))

    print("  " * indent + str(label) + payload_str)

    for child in node.children:
        prettyTraverse(child, indent + 1)









def serialize_value(v):
    if isinstance(v, Enum):
        return str(v)
    return v

def node_to_dict(node):
    if node is None:
        return None

    if isinstance(node.data, tuple):
        label = serialize_value(node.data[0])
        payload = [serialize_value(x) for x in node.data[1:]]
    else:
        label = serialize_value(node.data)
        payload = []

    return {
        "type": label,
        "payload": payload,
        "children": [node_to_dict(c) for c in node.children]
    }







temp_counter = 0

def new_temp():
    global temp_counter
    temp_counter += 1
    return f"tmp{temp_counter}"


def genSBOp(node):
    instr = []
    node_type = node.data[0]

    if node_type == TokenKind.Number:
        temp = new_temp()
        instr.append(f'scorebaord players operation {temp} {NumberSBObj} = "{node.data[1]}" {NumberSBObj}')
        return instr, temp

    if node_type == TokenKind.Access:
        if node.children:
            target_node = node.children[0]
            if target_node.data[0] == TokenKind.Target:
                temp = new_temp()
                instr.append(f'scoreboard players operation {temp} {NumberSBObj} = {target_node.data[1]} {node.data[1]}')
                return instr, temp
        raise ValueError("Access node missing Target child")

    if node_type == "Binary":
        left_instr, left_var = genSBOp(node.left)
        right_instr, right_var = genSBOp(node.right)
        instr.extend(left_instr)
        instr.extend(right_instr)
        temp = new_temp()

        op_map = {
            '+': '+=',
            '-': '-=',
            '*': '*=',
            '/': '/=',
            '%': '%='
        }
        operator = node.data[2]
        compound_op = op_map[operator]

        instr.append(f'scoreboard players operation {temp} {NumberSBObj} = {left_var} {NumberSBObj}')
        instr.append(f"scoreboard players operation {temp} {NumberSBObj} {compound_op} {right_var} {NumberSBObj}")
        return instr, temp

    if node_type == TokenKind.Assign:
        lhs_node = node.children[0]
        rhs_node = node.children[1]

        if lhs_node.data[0] == TokenKind.Access and lhs_node.children:
            lhs_target = lhs_node.children[0].data[1]
            lhs_context = lhs_node.data[1]
            target_name = f"{lhs_target} {lhs_context}"
        else:
            target_name = new_temp()

        rhs_instr, rhs_var = genSBOp(rhs_node)
        instr.extend(rhs_instr)
        instr.append(f"scoreboard players operation {target_name} {NumberSBObj} = {rhs_var} {NumberSBObj}")
        return instr, target_name

    return [], None
