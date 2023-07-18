# Eliminate irrelevant characters
def replace_word (line):
    newline = line
    digit="1234567890"
    sym="·_~`<>:;(){}[]!$%*&=:?,.+-\\\/\"\"'©@#^«–——“”|"
    net_sym=['</b>','<b>','<i>','</i>','<pd>','</pd>','<u>','</u>',]

    for i in range(len(digit)):
        newline=newline.replace(digit[i],'')
    for i in range(len(sym)):
        newline=newline.replace(sym[i],'')
    for i in range(len(net_sym)):
        newline=newline.replace(net_sym[i],'')
    return newline

def map (filename,arr,i):
    article = open(filename, 'r',encoding='utf-8')
    for line in article:
        line = replace_word(line)
        for word in line.split():
            word = word.lower()
            arr.append(word)
    article.close()
    return

