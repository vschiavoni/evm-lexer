A simple lexer for [Pygmentize](https://pygments.org/docs/cmdline/)  to code-highlight EVM bytecode inside Minted latex code.

Install it for the pygmentize version used. Find the required Python installation:

```
head -n 1 `which pygmentize`
#!/opt/homebrew/Cellar/pygments/2.19.2/libexec/bin/python
```

Then:
```
/opt/homebrew/Cellar/pygments/2.19.2/libexec/bin/python -pip install -e .
```

Check for correct installation:

```
pygmentize -L lexers | grep -e evm
* evm, evmasm:
    EVM (filenames *.evm, *.evmasm, *.easm)
```

Then, use in Latex/minted:
```
  \begin{minted}[
    fontsize=\small,
    linenos,
    numbersep=8pt,
    frame=none,
    breaklines,  
    style=vs
]{evmasm}
PUSH1 60
PUSH1 04
DUP1
SLOAD
POP
DUP4
DUP2
JUMPDEST
\end{minted}
```
