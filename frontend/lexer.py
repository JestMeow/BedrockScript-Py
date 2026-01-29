
from .tokens import Token, TokenKind

def kindFromStr(str):
    match (str):
        # Keywords
        case 'def': return TokenKind.KeywordDef
        case 'if': return TokenKind.KeywordIf
        case 'execute': return TokenKind.KeywordExecute

        # Punctuators
        case '(': return TokenKind.LeftParen
        case ')': return TokenKind.RightParen
        case '[': return TokenKind.LeftSquare
        case ']': return TokenKind.RightSquare
        case '{': return TokenKind.LeftCurly
        case '}': return TokenKind.RightCurly

        case '.': return TokenKind.Dot
        case ':': return TokenKind.Colon
        case ';': return TokenKind.Semicolon
        case '\'': return TokenKind.SingleQuote
        case '"': return TokenKind.DoubleQuote

        # Arithmetic
        case '+': return TokenKind.Plus
        case '-': return TokenKind.Minus
        case '*': return TokenKind.Asterisk
        case '/': return TokenKind.Slash
        case '%': return TokenKind.Modulo

        # Assignment
        case '=': return TokenKind.Equal
        case '+=': return TokenKind.PlusEqual
        case '-=': return TokenKind.MinusEqual
        case '*=': return TokenKind.AsteriskEqual
        case '/=': return TokenKind.SlashEqual
        case '%=': return TokenKind.ModuloEqual
        case '++': return TokenKind.Increment
        case '--': return TokenKind.Decrement

        # Comparison
        case '==': return TokenKind.Equals
        case '!=': return TokenKind.NotEquals
        case '<': return TokenKind.Less
        case '>': return TokenKind.Greater
        case '<=': return TokenKind.Leq
        case '>=': return TokenKind.Geq

        # Logical
        case '&&': return TokenKind.And
        case '||': return TokenKind.Or
        case '!': return TokenKind.Not

        # Default
        case _: return TokenKind.Identifier



def isPunctuator(ch):
    if (ch.isspace() or ch == '' or ch == '+' or ch == '-' or ch == '*' or
            ch == '/' or ch == ',' or ch == ';' or ch == '>' or
            ch == '<' or ch == '=' or ch == '(' or ch == ')' or
            ch == '[' or ch == ']' or ch == '{' or ch == '}' or
            ch == '&' or ch == '|' or ch == '.'):
        return True
    return False


def isOperator(ch):
    if (ch == '+' or ch == '-' or ch == '*' or
            ch == '/' or ch == '>' or
            ch == '<' or ch == '='):
        return True
    return False

def isCommandEnd(ch):
    if (ch == ';' or ch == ')'):
        return True
    return False




def tokenize(str):
    tokens = []
    right = 0
    left = 0
    length = len(str)

    while (right < length):
        while (right < length and str[right].isspace()):
            right += 1
        left = right

        if (right >= length):
            break

        while right < length and not isPunctuator(str[right]) and not str[right].isspace() and str[right] != '.':
            right += 1
        
        if (right + 1 < length and isOperator(str[right]) and isOperator(str[right + 1])):
            if (left != right):
                sub = str[left:right]
                tokens.append((kindFromStr(sub), sub))
            
            tokens.append((kindFromStr(str[right:right+2]), str[right:right+2]))
            right += 2
            left = right

            continue
        
        if isPunctuator(str[right]) and left == right:
            tokens.append((kindFromStr(str[right]), str[right]))
            right += 1
            left = right
            continue
        
        if ((isPunctuator(str[right]) == True and left != right) or (right == length and left != right)):
            sub = str[left:right]

            isNumber = bool(sub)
            for ch in sub:
                if (not ch.isdigit()):
                    isNumber = False
                    break
                
            # isTarget = bool(sub)
            # for ch in sub:
            #     if (ch != '@'):
            #         isTarget = False
            #         print("ues")
            #         break

            if str[left] == '@':
                right = left + 1
                while right < length and str[right] != '.' and not str[right].isspace():
                    right += 1
                sub = str[left:right]
                tokens.append((TokenKind.Target, sub))
                left = right
                continue
            
            if str[right] == '.':
                tokens.append((TokenKind.Dot, '.'))
                right += 1
                left = right
                continue
            
            if (isNumber):
                tokens.append((TokenKind.Number, sub))
            # elif (isTarget):
            #     tokens.append((TokenKind.Target, sub))
            elif (kindFromStr(sub) != TokenKind.Identifier):
                tokens.append((kindFromStr(sub), sub))
            elif (kindFromStr(sub) == TokenKind.Identifier and str[left - 1] != '.' and tokens and tokens[-1][0] != TokenKind.KeywordDef):
                while (right < length and not isCommandEnd(str[right])):
                    right += 1
                
                sub = str[left:right]
                tokens.append((TokenKind.CommandSegment, sub))
            else:
                tokens.append((kindFromStr(sub), sub))
            
            left = right
    tokens.append((TokenKind.EndOfFile, ''))
    return tokens

                    


    