from fisk import fisk_lexer


def test_lexer_fisk_sample():
    with open("sample.fisk", 'r') as f:
        sample = f.read()

    assert fisk_lexer.produce_tokens(sample) == [
        ("DIRECTIVE", "org"),
        ("NUMBER", 0x100),
        ("OPERATION", "jmp"),
        ("IDENTIFIER", "main"),
        ("LABEL", "array"),
        ("DIRECTIVE", "db"),
        ("NUMBER", 1),
        ("NUMBER", 1),
        ("NUMBER", 2),
        ("NUMBER", 3),
        ("NUMBER", 5),
        ("NUMBER", 8),
        ("LABEL", "msg"),
        ("DIRECTIVE", "db"),
        ("STRING", "Hello, Fisk!"),
        ("NUMBER", 0),
        ("LABEL", "main"),
        ("OPERATION", "mov"),
        ("REGISTER", "r0"),
        ("NUMBER", 0x03),
        ("OPERATION", "mov"),
        ("REGISTER", "r1"),
        ("IDENTIFIER", "msg"),
        ("OPERATION", "int"),
        ("NUMBER", 0x10),
        ("OPERATION", "mov"),
        ("REGISTER", "r0"),
        ("LBRACKET", None),
        ("REGISTER", "r1"),
        ("RBRACKET", None),
        ("OPERATION", "int"),
        ("NUMBER", 0x11),
        ("OPERATION", "jmp"),
        ("IDENTIFIER", "$"),
        ("END", None),
    ]
