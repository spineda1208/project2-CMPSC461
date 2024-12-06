from Lexer import Lexer
from Parser import Parser

source_code: str = """
my_name = 100
x = 12
while x == 10 {
    foo(x)
    bar(y)
    baz(z)
}
"""

print("Tokenizing inititated:")
print("-" * 22)
lexer = Lexer(source_code)
tokens = lexer.tokenize()

print("Tokenized:")
print("-" * 10)
for i in tokens:
    print(i)
print("\n")

print("Parsing inititated:")
print("-" * 19)
# parser = Parser(tokens)
# ast = parser.parse()
# print("\nParsed:")
# print("-" * 7)

# result = ""
# for node in ast:
#     result += node.to_string()

# print(result)
