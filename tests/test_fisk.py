from fisk import FiskLexer


def test_lexer_fisk_sample():
    with open("sample.fisk", 'r') as f:
        sample = f.read()

    tokens = list(FiskLexer().tokens(sample))

    assert tokens == [
        ("DIRECTIVE", "org"),
        ("NUMBER", 0x100),
        ("OPERATION", "jmp"),
        ("IDENTIFIER", "main"),
        ("LABEL", "array"),
        ("DIRECTIVE", "db"),
        ("NUMBER", 1),
        ("SYMBOL", ","),
        ("NUMBER", 1),
        ("SYMBOL", ","),
        ("NUMBER", 2),
        ("SYMBOL", ","),
        ("NUMBER", 3),
        ("SYMBOL", ","),
        ("NUMBER", 5),
        ("SYMBOL", ","),
        ("NUMBER", 8),
        ("LABEL", "msg"),
        ("DIRECTIVE", "db"),
        ("STRING", "Hello, Fisk!"),
        ("SYMBOL", ","),
        ("NUMBER", 0),
        ("LABEL", "main"),
        ("OPERATION", "mov"),
        ("REGISTER", "r0"),
        ("SYMBOL", ","),
        ("NUMBER", 0x03),
        ("OPERATION", "mov"),
        ("REGISTER", "r1"),
        ("SYMBOL", ","),
        ("IDENTIFIER", "msg"),
        ("OPERATION", "int"),
        ("NUMBER", 0x10),
        ("OPERATION", "mov"),
        ("REGISTER", "r0"),
        ("SYMBOL", ","),
        ("SYMBOL", "["),
        ("REGISTER", "r1"),
        ("SYMBOL", "]"),
        ("OPERATION", "int"),
        ("NUMBER", 0x11),
        ("OPERATION", "jmp"),
        ("IDENTIFIER", "$"),
        ("SYMBOL", "end"),
    ]
