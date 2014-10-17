
def eectokenizer(line):
    """parses the cummings tokens from a 
    line of text, returning the tokens in a list
    TBD: try this on a arbitrary stream of text.
    """
    empty  = ' \t\n'
    escape = '\\'
    state  = ''
    open   = '('
    close  = ')'
    separ  = ','

    stream = []

    collect = ''
    for c in line:
        
        if state == 'escape':
            collect += c
            state = ''
            continue
            
        if c in empty and not collect:
            continue
                
        if c == escape:
            state = 'escape'
            continue
                    
        if c == open or c == close or c == separ:

            stream.append( collect)
            stream.append( c)
            collect = ''

        else:
            collect += c

    return stream

class inputStream(Object):
    """reads STDIN and named files from argv[1:],
    treating the filename '-' as an alias for STDIN,
    returning the cummings tokens in a flattend list
    """
    # https://docs.python.org/2/library/fileinput.html
    def __init__:
        tokens = []
        for line in fileinput.input():
            tokens.append( eectokenizer(line))
            
        return sum(tokens, [])
