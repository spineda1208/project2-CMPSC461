from Lexer import Lexer
import ASTNodeDefs as AST
from typing import Any, List


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)

        self.symbol_table = {"global": {}}
        self.scope_counter = 0
        self.scope_stack = ["global"]
        self.messages = []

        self.messages: List[str] = tokens.pop(0)

    def advance(self) -> None:
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    def error(self, message) -> None:
        self.messages.append(message)

    # TODO: Implement logic to enter a new scope, add it to symbol table, and update `scope_stack`
    def enter_scope(self) -> None:
        pass

    # TODO: Implement logic to exit the current scope, removing it from `scope_stack`
    def exit_scope(self) -> None:
        pass

    # Return the current scope name
    def current_scope(self) -> str:
        return self.scope_stack[-1]

    # TODO: Check if a variable is already declared in the current scope; if so, log an error
    def check_variable_declared(self, identifier) -> None:
        self.error(
            f"Variable {identifier} has already been declared in the current scope"
        )

    # TODO: Check if a variable is declared in any accessible scope; if not, log an error
    def check_variable_use(self, identifier) -> None:
        self.error(
            f"Variable {identifier} has not been declared in the current or any enclosing scopes"
        )

    # TODO: Check type mismatch between two entities; log an error if they do not match
    def check_type_match_2(self, vType, eType, var, exp) -> None:
        self.error(f"Type Mismatch between {vType} and {eType}")

    # TODO: Implement logic to add a variable to the current scope in `symbol_table`
    def add_variable(self, name, variable_type) -> None:
        pass

    # TODO: Retrieve the variable type from `symbol_table` if it exists
    def get_variable_type(self, name) -> None:
        return None

    def parse(
        self,
    ) -> AST.Block:
        statements: List[
            (AST.Assignment | AST.FunctionCall | AST.IfStatement | AST.WhileStatement)
        ] = []
        while self.current_token[0] != "EOF":
            statement = self.statement()
            statements.append(statement)
        return AST.Block(statements)

    # TODO: Modify the `statement` function to dispatch to declare statement
    def statement(self):
        current_token_identifier = self.current_token[0]
        match current_token_identifier:
            case "IDENTIFIER":
                peek = self.peek()
                match peek:
                    case "EQUALS":
                        return self.assign_stmt()
                    case "LPAREN":
                        return self.function_call()
                    case _:
                        raise ValueError(
                            f"Unexpected token after identifier: {self.current_token}"
                        )
            case "IF":
                return self.if_stmt()
            case "WHILE":
                return self.while_stmt()
            case _:
                raise ValueError(f"Unexpected token: {self.current_token}")

    # TODO: Implement the declaration statement and handle adding the variable to the symbol table
    def decl_stmt(self):
        """
        Parses a declaration statement.
        Example:
        int x = 5
        float y = 3.5
        TODO: Implement logic to parse type, identifier, and initialization expression and also handle type checking
        """
        return AST.Declaration(variable_type, variable_name, expression)

    # TODO: Parse assignment statements, handle type checking
    def assign_stmt(self):
        """
        Parses an assignment statement.
        Example:
        x = 10
        x = y + 5
        TODO: Implement logic to handle assignment, including type checking.
        """
        return AST.Assignment(variable_name, expression)

    # TODO: Implement the logic to parse the if condition and blocks of code
    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition {
            # statements
        }
        else {
            # statements
        }
        TODO: Implement the logic to parse the if condition and blocks of code.
        """
        return AST.IfStatement(condition, then_block, else_block)

    # TODO: Implement the logic to parse while loops with a condition and a block of statements
    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition {
            # statements
        }
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        return AST.WhileStatement(condition, block)

    # TODO: Implement logic to capture multiple statements as part of a block
    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by `{}`.
        Example:

        x = 5
        y = 10

        TODO: Implement logic to capture multiple statements as part of a block.
        """
        return AST.Block(statements)

    # TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking
    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking.
        """
        left = self.term()
        while self.current_token[0] in ["PLUS", "MINUS"]:
            op = self.current_token[0]
            self.advance()
            right = self.term()
            self.check_type_match_2(left.value_type, right.value_type, left, right)
            left = AST.BinaryOperation(left, op, right, value_type=left.value_type)

        return left

    # TODO: Implement parsing for boolean expressions and check for type compatibility
    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions and check for type compatibility.
        """

    # TODO: Implement parsing for multiplication and division and check for type compatibility
    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement parsing for multiplication and division and check for type compatibility.
        """

    def factor(self):
        if self.current_token[0] == "NUMBER":
            # handle int
            return AST.Factor(number, "int")
        elif self.current_token[0] == "FNUMBER":
            # handle float
            return AST.Factor(number, "float")
        elif self.current_token[0] == "IDENTIFIER":
            # TODO: Ensure that you parse the identifier correctly, retrieve its type from the symbol table, and check if it has been declared in the current or any enclosing scopes.
            return AST.Factor(variable_name, variable_type)
        elif self.current_token[0] == "LPAREN":
            self.advance()
            expr = self.expression()
            self.expect("RPAREN")
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        func_name = self.current_token[1]
        self.advance()
        self.expect("LPAREN")
        args = self.arg_list()
        self.expect("RPAREN")

        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of function arguments.
        Example:
        (x, y + 5)
        """
        args = []
        if self.current_token[0] != "RPAREN":
            args.append(self.expression())
            while self.current_token[0] == "COMMA":
                self.advance()
                args.append(self.expression())

        return args

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(
                f"Expected token {token_type}, but got {self.current_token[0]}"
            )

    def peek(self):
        return self.tokens[0][0] if self.tokens else None
