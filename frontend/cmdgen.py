from enum import Enum, auto

from .tokens import TokenKind
from .parser import *
from .tree import *


class Cmdgen:
    def __init__(self, root):
        self.command = []
        self.root = root

class Command(Enum):
    RemoveLine = auto()

command = []


def merge_branches(root):
    result = []

    def dfs(node, path):
        path.append(node)

        if not node.children:
            result.append(path.copy())
        else:
            for child in node.children:
                dfs(child, path)

        path.pop()

    dfs(root, [])
    return result



def declareSBObjC(node, result=None, number_seen=None):
    if result is None:
        result = []
    if number_seen is None:
        number_seen = set()
    
    data = node.data
    data_type = data[0]
    data_value = data[1] if len(data) > 1 else None
    
    if data_type == TokenKind.Number and data_value not in number_seen:
        result.append(f'scoreboard players set "{data_value}" __NUMBER__ {data_value}')
        number_seen.add(data_value)
    
    for child in node.children:
        declareSBObjC(child, result, number_seen)

    return result


def genCommandContext(node, result=None, exec_context=None):
    if result is None:
        result = []
    if exec_context is None:
        exec_context = []

    data = node.data
    data_type = data[0]
    data_value = data[1] if len(data) > 1 else None

    if (data_type == TokenKind.KeywordExecute):
        if node.parent.parent is not None:
            exec_context = []
        
        exec_context.append('execute')
        exec_context.append(node.children[0].data[1])
        exec_context.append('run')

    # ---------- Step 1: Assign ----------
    elif data_type == TokenKind.Assign:
        
        
        instructions, _ = genSBOp(node)
        for ins in instructions:
            excCntxt = ''
            if exec_context:
                excCntxt = ' '.join(exec_context)
                # cmd.append(' '.join(exec_context))
            
            result.append(f'{excCntxt} {ins}' if node.parent.parent is None else ins)

    # ---------- Step 2: CommandSegment ----------
    elif data_type == TokenKind.CommandSegment and node.parent.data[0] != TokenKind.KeywordExecute:
        full_cmd = data_value
        if node.parent.parent is None:
            # if node.parent.parent.data[0] == TokenKind.KeywordDef:
            excCntxt = ''

            if exec_context:
                excCntxt = ' '.join(exec_context)

            full_cmd = f'{excCntxt} {data_value}' if exec_context else data_value
        result.append(full_cmd)
        

    # ---------- Step 3: Recurse ----------
    for child in node.children:
        genCommandContext(child, result, exec_context)

    return result




