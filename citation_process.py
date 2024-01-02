import sys
import json
import re
import argparse

def titlize(word: str, exclude_word: list):
    if word.isupper() or word.istitle():
       return word
    else:
        if word.lower() in exclude_word:
            return word.lower()
        else:
            return word.capitalize()

def to_title(word:str, exclude_word: list):
    # "U+2013" is the En Dash Unicode Character, 
    # while "-" is the Hyphen-Minus Unicode Character
    # both are likely to appear in titles
    if ("\u2013" in word):
        hyphen_word = "\u2013".join([titlize(hw, exclude_word) for hw in word.split("\u2013")])
        return hyphen_word
    elif ('-' in word):
        hyphen_word = '-'.join([titlize(hw, exclude_word) for hw in word.split("-")])
        return hyphen_word
    else:
        return titlize(word, exclude_word)

def parse_line(line: str, next_line: str):
    is_HTML = False
    is_curly_brace = False
    string1 = None
    if re.search('".*"', line) is not None:
        string = re.search('".*"', line).group(0)
    elif re.search('{.*}', line) is not None:
        is_curly_brace = True
        string = re.search('{.*}', line).group(0)
    elif re.search('{.*</i>', line) is not None:
        is_curly_brace = True
        is_HTML = True
        string1 = re.search('{.*</i>', line).group(0)
        string2 = re.search('.*?}', next_line).group(0)
        string = "".join([string1, string2]) + ","
        string = string.replace('<i>','').replace('</i>','')
    else:
        raise ValueError('the format "{}" is not valid'.format(line))
    
    return is_HTML, is_curly_brace, [string, string1]


def citation_process(citation_block: list, journal_to_abbr: dict, exclude_word: list, required_entry: list):
    """citation_process _summary_

    Args:
        citation_block (list): 
            list of split() returns for a specfic citation block
        journal_to_abbr (dict): 
            dictionary for jornal names and abbreviation correspondences
        exclude_word (list):
            list of words that do not need to be titlized
        required_entry (list):
            required entry for "@article" type of citations
    """
    # copy of the requied_entry list
    unsatisfied = [_ for _ in required_entry]
    for i, line in enumerate(citation_block):
        line_strip = line.strip(" ")
        # use try...except to prevent index out of range
        try:
            next_line = citation_block[i+2]
        except IndexError as e:
            next_line = ''
        # Titlize article name
        if line_strip.startswith("title"):
            is_HTML, is_curly_brace, str_list =\
                parse_line(line_strip, next_line)
        
            title_list = [to_title(word, exclude_word) for word in str_list[0].split(" ")]
            title = " ".join(title_list)
            if is_HTML:
                citation_block[i] = line.replace(str_list[1], title)
                print("\n", citation_block[i], "\n")
                citation_block[i+1] = ""
                citation_block[i+2] = ""
            else:
                citation_block[i] = line.replace(str_list[0], title)
            
        # Journal Abbreviation
        if line_strip.startswith("journal"):
            is_HTML, is_curly_brace, str_list =\
                parse_line(line_strip, next_line)
            journal_name_template = '{{{}}}' if is_curly_brace else '"{}"'
            journal_str = str_list[0]
            journal_name_strip = journal_str[1:-1]
            journal_name = journal_name_strip.replace('{','').replace('}','')
            journal_name = journal_to_abbr.get(journal_name, journal_name_strip)
            journal_name = journal_name_template.format(journal_name)
            citation_block[i] = line.replace(journal_str, journal_name)
        
        # Check required entry
        string_start = next((word for word in unsatisfied if line_strip.lower().startswith(word)), None)
        # next() retrieves the first element from this generator expression that 
        # satisfies the condition specified. If no element satisfies the 
        # condition, it returns None (the second argument).
        if string_start: #string start = "string" (indicates True) or None (indicates False)
            unsatisfied.remove(string_start)

    if unsatisfied and (citation_block[0].strip(" ").startswith("@article")):
        print("No " + ", ".join(unsatisfied) + " in the citation entry.", file=sys.stderr)
        print("".join(citation_block) + "\n", file=sys.stderr)
    else:
        print("".join(citation_block), file=sys.stdout)
        
    return None
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="citation process")
    parser.add_argument('-u', '--user-json', 
                        type=str, default=None, help="customized json file")
    parser.add_argument('-e', '--exclude', 
                        type=str, default=None, help="words exclude titlize")
    parser.add_argument('-r', '--required',
                        type=str, default=None, help="required entries in citation")
    args = parser.parse_args()
    
    # Initialize abbreviation .json file
    with open('./data/journals.json') as file:
        journal_to_abbr = json.load(file)
    
    # Initialize exclude word & required entry lists
    exclude_word = []
    required_entry = []
    
    # read arguments for python
    if args.user_json is not None:
        with open(args.user_json) as file:
            customize_json = json.load(file)
        journal_to_abbr.update(customize_json)

    if args.exclude is not None:
        with open(args.exclude) as ex:
            exclude_word.extend(ex.read().split())
            
    if args.required is not None:
        with open(args.required) as r:
            required_entry.extend(r.read().split())
    
    # std input for bib files
    bib_text = sys.stdin.read()
    
    # Define a regular expression pattern to extract individual citations
    pattern = re.compile(r'@.*?\{.*?^\}', re.DOTALL | re.MULTILINE)
    
    # Extract individual citations
    citations = re.findall(pattern, bib_text)
    
    for c in citations:
        c_line = re.split("(\n)", c)
        citation_process(c_line, journal_to_abbr, exclude_word, required_entry)