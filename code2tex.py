#!/usr/bin/env python3

import sys
import re
import os.path

# TODO: read extensions, header from files found in sys.path?

# A subset of the languages supported by the Listings latex package
# File extensions mapped to language names
exts = {
    "ada" : "Ada" ,
    "adb" : "Ada" ,
    "ads" : "Ada" ,
    "awk" : "Awk" ,
    "c" : "C" ,
    "h" : "C++" ,
    "hh" : "C++" ,
    "hpp" : "C++" ,
    "cxx" : "C++" ,
    "cpp" : "C++" ,
    "caml" : "Caml" ,
    "ex" : "Euphoria" ,
    "exw" : "Euphoria" ,
    "f" : "Fortran" ,
    "for" : "Fortran" ,
    "f90" : "Fortran" ,
    "fpp" : "Fortran" ,
    "html" : "HTML" ,
    "xhtml" : "HTML" ,
    "has" : "Haskell" ,
    "hs" : "Haskell" ,
    "idl" : "IDL" ,
    "java" : "Java" ,
    # pde = Processing
    "pde" : "Java" ,
    "lsp" : "Lisp" ,
    "lgo" : "Logo" ,
    "ml" : "ML" ,
    "php" : "PHP" ,
    "php3" : "PHP" ,
    "p" : "Pascal" ,
    "pas" : "Pascal" ,
    "pl" : "Perl" ,
    # pl for perl conflicts with pl for Prolog...
    "py" : "Python" ,
    "r" : "R" ,
    "rb" : "Ruby" ,
    "sas" : "SAS" ,
    "sql" : "SQL" ,
    "tex" : "TeX" ,
    "vbs" : "VBScript" ,
    "vhd" : "VHDL" ,
    "vrml" : "VRML" ,
    "v" : "Verilog" ,
    "xml" : "XML" ,
    "xslt" : "XSLT" ,
    "bash" : "bash" ,
    "csh" : "csh" ,
    "ksh" : "ksh" ,
    "sh" : "sh" ,
    "tcl" : "tcl"
}

latexspecials = "\\{}_^#&$%~"
specials_re = re.compile(
    '(%s)' % '|'.join(re.escape(c) for c in latexspecials)
)


def makeTop(output=sys.stdout):
    # print out the file header
    print('''
\\documentclass{article}
\\usepackage[hmargin=1in,vmargin=1in]{geometry}
\\usepackage{listings}
\\usepackage{color}

% For better handling of unicode (Latin characters, anyway)
\\IfFileExists{lmodern.sty}{\\usepackage{lmodern}}{}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}

\\lstset{
    numbers=left,                   % where to put the line-numbers
    numberstyle=\\small \\ttfamily \\color[rgb]{0.4,0.4,0.4},
                % style used for the linenumbers
    showspaces=false,               % show spaces adding special underscores
    showstringspaces=false,         % underline spaces within strings
    showtabs=false,                 % show tabs within strings adding particular underscores
    frame=lines,                    % add a frame around the code
    tabsize=4,                      % default tabsize: 4 spaces
    breaklines=true,                % automatic line breaking
    breakatwhitespace=false,        % automatic breaks should only happen at whitespace
    basicstyle=\\ttfamily,
    %identifierstyle=\\color[rgb]{0.3,0.133,0.133},   % colors in variables and function names, if desired.
    keywordstyle=\\color[rgb]{0.133,0.133,0.6},
    commentstyle=\\color[rgb]{0.133,0.545,0.133},
    stringstyle=\\color[rgb]{0.627,0.126,0.941},
    literate=
        {á}{{\\'a}}1 {é}{{\\'e}}1 {í}{{\\'i}}1 {ó}{{\\'o}}1 {ú}{{\\'u}}1
        {Á}{{\\'A}}1 {É}{{\\'E}}1 {Í}{{\\'I}}1 {Ó}{{\\'O}}1 {Ú}{{\\'U}}1
        {à}{{\\`a}}1 {è}{{\\`e}}1 {ì}{{\\`i}}1 {ò}{{\\`o}}1 {ù}{{\\`u}}1
        {À}{{\\`A}}1 {È}{{\\'E}}1 {Ì}{{\\`I}}1 {Ò}{{\\`O}}1 {Ù}{{\\`U}}1
        {ä}{{\\"a}}1 {ë}{{\\"e}}1 {ï}{{\\"i}}1 {ö}{{\\"o}}1 {ü}{{\\"u}}1
        {ã}{{\\~a}}1 {ẽ}{{\\~e}}1 {ĩ}{{\\~i}}1 {õ}{{\\~o}}1 {ũ}{{\\~u}}1
        {Ã}{{\\~A}}1 {Ẽ}{{\\~E}}1 {Ĩ}{{\\~I}}1 {Õ}{{\\~O}}1 {Ũ}{{\\~U}}1
        {Ä}{{\\"A}}1 {Ë}{{\\"E}}1 {Ï}{{\\"I}}1 {Ö}{{\\"O}}1 {Ü}{{\\"U}}1
        {â}{{\\^a}}1 {ê}{{\\^e}}1 {î}{{\\^i}}1 {ô}{{\\^o}}1 {û}{{\\^u}}1
        {Â}{{\\^A}}1 {Ê}{{\\^E}}1 {Î}{{\\^I}}1 {Ô}{{\\^O}}1 {Û}{{\\^U}}1
        {œ}{{\\oe}}1 {Œ}{{\\OE}}1 {æ}{{\\ae}}1 {Æ}{{\\AE}}1 {ß}{{\\ss}}1
        {ű}{{\\H{u}}}1 {Ű}{{\\H{U}}}1 {ő}{{\\H{o}}}1 {Ő}{{\\H{O}}}1
        {ç}{{\\c c}}1 {Ç}{{\\c C}}1 {ø}{{\\o}}1 {å}{{\\r a}}1 {Å}{{\\r A}}1
        {€}{{\\euro}}1 {£}{{\\pounds}}1 {«}{{\\guillemotleft}}1
        {»}{{\\guillemotright}}1 {ñ}{{\\~n}}1 {Ñ}{{\\~N}}1 {¿}{{?`}}1
        {º}{{\\textsuperscript{o}}}1
        {ª}{{\\textsuperscript{a}}}1
        {ě}{{\v{e}}}1 {Ě}{{\v{E}}}1 {ů}{{\r{u}}}1 {Ů}{{\r{U}}}1 {č}{{\v{c}}}1
        {ď}{{\v{d}}}1 {ň}{{\v{n}}}1 {ř}{{\v{r}}}1 {š}{{\v{s}}}1 {ť}{{\v{t}}}1
        {ý}{{\'y}}1 {ž}{{\v{z}}}1 {Č}{{\v{C}}}1 {Ď}{{\v{D}}}1 {Ň}{{\v{N}}}1
        {Ř}{{\v{R}}}1 {Š}{{\v{S}}}1 {Ť}{{\v{T}}}1 {Ý}{{\'Y}}1 {Ž}{{\v{Z}}}1
}

\\begin{document}
''', file=output)


def makeBottom(output=sys.stdout):
    print("\\end{document}", file=output)


def addListing(filename, custom_heading=None, output=sys.stdout):
    heading = filename
    if custom_heading is not None:
        heading = custom_heading

    heading_escaped = re.sub(specials_re, r'\\\1', heading)
    print("\\section*{%s}" % heading_escaped, file=output)

    ext = filename.split('.')[-1]
    lang = exts.get(ext, '')
    # uses '' if extension not found in our dictionary
    print("\\lstinputlisting[language=%s]{\"%s\"}" % (lang, filename), file=output)
    print("", file=output)

def readDirectory(folder):
    files = os.listdir(folder)
    for infile in files:
        if os.path.isdir(folder+'/'+infile):
            readDirectory(folder+'/'+infile)
        else:
            addListing(folder+'/'+infile)

def main():
    if len(sys.argv) < 2:
        sys.exit('''Usage: %s FILE [FILE2] [FILE3] [...]
 Outputs .tex file to STDOUT (redirect with \"%s FILE.py > FILE.tex\")
 Languages (for syntax highlighting) determined from file extensions.''' % (sys.argv[0], sys.argv[0]))

    files = sys.argv[1:]  # get all command line arguments

    # Check existence of all files first
    for infile in files:
        if not (os.path.isfile(infile) or os.path.isdir(infile)):
            sys.exit("File not found: %s" % infile)

    # Make the file (output to STDOUT)
    makeTop()
    for infile in files:
        if(os.path.isdir(infile)):
            readDirectory(infile)
        else:
            addListing(infile)
    makeBottom()


if __name__ == "__main__":
    main()
