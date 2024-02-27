from dataclasses import dataclass
import dataclasses
import re
from typing import List, Literal, cast


TokenType = Literal["whitespace","int_literal", "identifier", "operator", "parenthesis", "punctuation", "comment"]

@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str
    location: 'SourceLocation'


@dataclasses.dataclass(frozen=True)
class SourceLocation:
    file: str
    line: int
    column: int

def tokenize(source_code: str) -> List[Token]:
    whitespace_re = re.compile(r"\s+")
    int_literal_re = re.compile(r"\d+")
    identifier_re = re.compile(r"[a-zA-Z_]\w*")    
    operator_re = re.compile(r"==|!=|<=|>=|[+\-*/=<>]")
    parentheses_re = re.compile(r"[\(\)\{\}]")
    punctuation_re = re.compile(r"[,;]")
    comment_re = re.compile(r"//.*|#.*")

    position = 0
    line = 1
    column = 1
    result: List[Token] = []

    # Function to update the line and column numbers based on the matched token
    def update_position(matched_text: str) -> None:
        nonlocal line, column, position
        position += len(matched_text)
        new_lines = matched_text.count("\n")
        # start_positon = position - len(matched_text)
        # text = source_code[start_positon:position]
        if new_lines > 0:
            line += new_lines
            column = len(matched_text.split("\n")[-1]) + 1
        else:
            column += len(matched_text)
        # if new_lines = text.count("\n"):
        #     line += new_lines
        #     column = len(text) - text.rfind("\n")
        # else:
        #     column += len(text)
        # position = start_positon + len(text)

    while position < len(source_code):
        match = None
        # for pattern, type_ in [
        for pattern, type_ in [
            (whitespace_re, "whitespace"),
            (int_literal_re, "int_literal"),
            (identifier_re, "identifier"),
            (operator_re, "operator"),
            (parentheses_re, "parenthesis"),
            (punctuation_re, "punctuation"),
            (comment_re, "comment")
        ]:
            match = pattern.match(source_code, position)
            if match:
                matched_text = match.group(0)
                assert_type = cast(TokenType, type_)
                result.append(Token(assert_type, match.group, SourceLocation("", line, column - len(matched_text) + 1)))
                update_position(matched_text)
                break
        if not match:
            raise ValueError(f"Unexpected character at {position}: {source_code[position]}")

    return result
        # match = whitespace_re.match(source_code, position)
        # if match is not None:
        #     position += match.end() - position
        #     continue

        # match = int_literal_re.match(source_code, position)
        # if match is not None:
        #     result.append(Token("int_literal", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

        # match = identifier_re.match(source_code, position)
        # if match is not None:
        #     result.append(Token("identifier", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

        # match = operator_re.match(source_code, position)   
        # if match is not None:
        #     result.append(Token("operator", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

        # match = parentheses_re.match(source_code, position)
        # if match is not None:
        #     result.append(Token("parenthesis", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

        # match = punctuation_re.match(source_code, position)
        # if match is not None:
        #     result.append(Token("punctuation", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

        # match = comment_re.match(source_code, position)
        # if match is not None:
        #     result.append(Token("comment", match.group(), SourceLocation("", line, column)))
        #     position += match.end() - position
        #     column += match.end() - position
        #     continue

