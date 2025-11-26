import re

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Keyword, Name, Number, Punctuation


class EVMLexer(RegexLexer):
    """
    Simple lexer for Ethereum Virtual Machine (EVM) assembly / disassembly.

    Intended for the textual form emitted by tools like `evm disasm`,
    `solc --asm`, huff/evmasm, etc., not Solidity source.
    """
    name = "EVM"
    aliases = ["evm", "evmasm"]
    filenames = ["*.evm", "*.evmasm", "*.easm"]
    mimetypes = ["text/x-evm"]

    flags = re.IGNORECASE | re.MULTILINE

    # Core opcodes (no numeric suffix). Extend if you want every obscure one.
    _opcodes = r"""STOP ADD MUL SUB DIV SDIV MOD SMOD ADDMOD MULMOD EXP SIGNEXTEND
        LT GT SLT SGT EQ ISZERO AND OR XOR NOT BYTE SHL SHR SAR SHA3
        ADDRESS BALANCE ORIGIN CALLER CALLVALUE CALLDATALOAD CALLDATASIZE CALLDATACOPY
        CODESIZE CODECOPY GASPRICE EXTCODESIZE EXTCODECOPY RETURNDATASIZE RETURNDATACOPY
        EXTCODEHASH BLOCKHASH COINBASE TIMESTAMP NUMBER DIFFICULTY GASLIMIT
        CHAINID SELFBALANCE BASEFEE POP MLOAD MSTORE MSTORE8 SLOAD SSTORE
        JUMP JUMPI PC MSIZE GAS JUMPDEST
        CREATE CALL CALLCODE RETURN DELEGATECALL CREATE2 STATICCALL REVERT INVALID SELFDESTRUCT"""

    tokens = {
        "root": [
            # Line comments
            (r";.*?$", Comment.Single),
            (r"//.*?$", Comment.Single),

            # C-style block comments
            (r"/\*", Comment.Multiline, "comment"),

            # Labels at start of line: "tag_1:"
            (r"^(\s*)([A-Za-z_.$][\w.$]*)(:)",
             bygroups(Text.Whitespace, Name.Label, Punctuation)),

            # Whitespace
            (r"\s+", Text.Whitespace),

            # Opcodes with numeric suffixes
            (r"\b(PUSH)(\d{1,2})\b", bygroups(Keyword, Number.Integer)),
            (r"\b(DUP)(\d{1,2})\b", bygroups(Keyword, Number.Integer)),
            (r"\b(SWAP)(\d{1,2})\b", bygroups(Keyword, Number.Integer)),
            (r"\b(LOG)([0-4])\b", bygroups(Keyword, Number.Integer)),

            # Core opcodes
            (r"\b(?:" + "|".join(_opcodes.split()) + r")\b", Keyword),

            # Hex immediates (with or without 0x)
            (r"0x[0-9a-fA-F_]+", Number.Hex),
            # Raw hex blobs like 6080604052...
            (r"\b[0-9a-fA-F]{2,}\b", Number.Hex),

            # Decimal immediates
            (r"\b\d+\b", Number.Integer),

            # Identifiers / symbols
            (r"[A-Za-z_.$][\w.$]*", Name),

            # Fallback: one char as plain text
            (r".", Text),
        ],

        "comment": [
            (r"[^*/]+", Comment.Multiline),
            (r"/\*", Comment.Multiline, "#push"),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[*/]", Comment.Multiline),
        ],
    }

    def analyse_text(self, text):
        """
        Hint Pygments that this looks like EVM asm,
        so `guess_lexer` can pick it up.
        """
        score = 0.0
        if re.search(r"\bPUSH\d{1,2}\b", text):
            score += 0.3
        if re.search(r"\bDUP\d{1,2}\b", text):
            score += 0.2
        if re.search(r"\bSWAP\d{1,2}\b", text):
            score += 0.1
        if re.search(r"\bJUMPDEST\b", text, re.IGNORECASE):
            score += 0.2
        if re.search(r"0x[0-9a-fA-F]{2,}", text):
            score += 0.1
        return min(score, 1.0)
