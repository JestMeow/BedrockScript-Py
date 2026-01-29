import sys

from pathlib import Path

from frontend.lexer import tokenize
from frontend.parser import Parser
# from frontend.tree import traverse, pretty_traverse, node_to_dict

from frontend.cmdgen import *

def main():
    try:
        fileInput = sys.argv[1]
    except:
        print("Incorrect number of arguments.")
        return
    

    def openFile(filepath, extension):
        path = Path(filepath)

        if not path.exists():
            print("Directory does not exist.")
            return

        if path.suffix == extension:
            with open(path, 'r') as f:
                content = f.read()

                tokens = tokenize(content)
                parser = Parser(tokens)

                ast = parser.parseProgram()

                print(f'scoreboard objectives add {NumberSBObj} dummy\n')

                scrbj = declareSBObjC(ast)

                for sb in scrbj:
                    print(sb)

                instructions = genCommandContext(ast)
                for ins in instructions:
                    print(ins)
        else:
            print(f'Open only {extension} files')

    openFile(fileInput, '.mcbs')



if __name__ == '__main__':
    main()