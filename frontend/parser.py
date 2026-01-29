from .tree import Node, BlockNode, BinaryNode
from .tokens import TokenKind


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def isAtEnd(self):
        return self.peek()[0] == TokenKind.EndOfFile

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, kind):
        if self.isAtEnd():
            return False
        return self.peek()[0] == kind

    def matches(self, *kinds):
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True
        return False

    def consume(self, kind, message):
        if self.check(kind):
            return self.advance()
        raise Exception(f"{message} at token {self.peek()[1]}")





    # Program
    def parseProgram(self):
        program = Node((TokenKind.Root, "ROOT"))
        while not self.isAtEnd():
            program.children.append(self.parseStatement())
        return program




    # Statements
    def parseStatement(self):
        if self.matches(TokenKind.KeywordDef):
            return self.parseDefStatement()

        if self.matches(TokenKind.KeywordIf):
            return self.parseIfStatement()

        if self.matches(TokenKind.KeywordExecute):
            return self.parseExecuteStatement()

        if self.check(TokenKind.LeftCurly):
            return self.parseBlock()

        if self.check(TokenKind.CommandSegment):
            return self.parseCommandStatement()

        return self.parseExpressionStatement()

    def parseDefStatement(self):
        name = self.consume(TokenKind.Identifier, "Expected identifier after def")
        block = self.parseBlock()
        return Node((TokenKind.KeywordDef, name[1]), [block])

    def parseIfStatement(self):
        self.consume(TokenKind.LeftParen, "Expected '(' after if")

        # segment = self.consume(TokenKind.CommandSegment, "Expected execute segment")
        segment = self.parseCommandSegment()

        self.consume(TokenKind.RightParen, "Expected ')' after if")
        block = self.parseBlock()
        segment.children.append(block)
        return Node((TokenKind.KeywordIf, 'if'), [segment])


    def parseExecuteStatement(self):
        self.consume(TokenKind.LeftParen, "Expected '(' after execute")

        # segment = self.consume(TokenKind.CommandSegment, "Expected execute segment")
        segment = self.parseCommandSegment()

        self.consume(TokenKind.RightParen, "Expected ')' after execute")
        block = self.parseBlock()
        segment.children.append(block)
        return Node((TokenKind.KeywordExecute, 'execute'), [segment])



    # Commands
    def parseCommandSegment(self):
        command = self.consume(TokenKind.CommandSegment, "Expected command segment")
        return Node((TokenKind.CommandSegment, command[1]))

    def parseCommandStatement(self):
        command = self.parseCommandSegment()
        if self.check(TokenKind.Semicolon):
            self.advance()
        return command



    # Blocks
    def parseExpressionStatement(self):
        expr = self.parseExpression()
        if self.check(TokenKind.Semicolon):
            self.advance()
        return expr

    def parseBlock(self):
        self.consume(TokenKind.LeftCurly, "Expected '{'")
        statements = []

        while not self.check(TokenKind.RightCurly) and not self.isAtEnd():
            statements.append(self.parseStatement())

        self.consume(TokenKind.RightCurly, "Expected '}'")
        return BlockNode(statements)

    # Expressions
    def parseExpression(self):
        return self.parseAssignment()

    def parseAssignment(self):
        left = self.parseEquality()

        if self.matches(TokenKind.Equal):
            value = self.parseAssignment()

            if isinstance(left, Node) and left.data[0] in (TokenKind.Identifier, TokenKind.Access):
                return Node((TokenKind.Assign, 'ASSIGN'), [left, value])

            raise Exception("Invalid assignment target.")

        return left


    def parseEquality(self):
        expr = self.parseComparison()
        while self.matches(TokenKind.Equals, TokenKind.NotEquals):
            operator = self.previous()
            right = self.parseComparison()
            expr = BinaryNode(expr, operator, right)
        return expr

    def parseComparison(self):
        expr = self.parseTerm()
        while self.matches(TokenKind.Greater, TokenKind.Less, TokenKind.Geq, TokenKind.Leq):
            operator = self.previous()
            right = self.parseTerm()
            expr = BinaryNode(expr, operator, right)
        return expr

    def parseTerm(self):
        expr = self.parseFactor()
        while self.matches(TokenKind.Plus, TokenKind.Minus):
            operator = self.previous()
            right = self.parseFactor()
            expr = BinaryNode(expr, operator, right)
        return expr

    def parseFactor(self):
        expr = self.parseUnary()
        while self.matches(TokenKind.Asterisk, TokenKind.Slash):
            operator = self.previous()
            right = self.parseUnary()
            expr = BinaryNode(expr, operator, right)
        return expr

    def parseUnary(self):
        if self.matches(TokenKind.Not, TokenKind.Minus):
            operator = self.previous()
            right = self.parseUnary()
            return Node(("Unary", operator[0]), [right])
        return self.parseCallOrAccess()

    def parseCallOrAccess(self):
        expr = self.parsePrimary()

        while True:
            if self.matches(TokenKind.Dot):
                name = self.consume(TokenKind.Identifier, "Expected property after '.'")
                expr = Node((TokenKind.Access, name[1]), [expr])

            elif self.matches(TokenKind.Increment):
                expr = Node(("Increment",), [expr])

            else:
                break

        return expr

    def parsePrimary(self):
        if self.matches(TokenKind.Number):
            return Node((TokenKind.Number, self.previous()[1]))

        if self.matches(TokenKind.Identifier):
            return Node((TokenKind.Identifier, self.previous()[1]))

        if self.matches(TokenKind.Target):
            return Node((TokenKind.Target, self.previous()[1]))

        if self.matches(TokenKind.LeftParen):
            expr = self.parseExpression()
            self.consume(TokenKind.RightParen, "Expected ')'")
            return expr

        raise Exception("Expected expression.")
