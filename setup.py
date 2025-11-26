from setuptools import setup, find_packages

setup(
    name="pygments-evm-lexer",
    version="0.1.0",
    description="Pygments lexer for Ethereum Virtual Machine (EVM) assembly",
    packages=find_packages(),
    install_requires=["Pygments>=2.0"],
    entry_points={
        "pygments.lexers": [
            "evm = evmlexer.evm_lexer:EVMLexer",
        ],
    },
)
