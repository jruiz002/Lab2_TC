import re

def get_precedence(c):
    """
    Calculate precedence for regex operators.
    Precedences for REs:
    '(' -> 1
    '|' -> 2
    '.' -> 3
    '?' -> 4
    '*' -> 4
    '+' -> 4
    '^' -> 5
    """
    precedence_map = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }
    return precedence_map.get(c, 0)

def preprocess_regex(regex):
    """
    Preprocess regex to handle escaped characters and convert extensions.
    Converts '+' to 'aa*' pattern and '?' to '(a|ε)' pattern.
    """
    result = []
    i = 0
    
    while i < len(regex):
        char = regex[i]
        
        if char == '\\' and i + 1 < len(regex):
            result.append(char)
            result.append(regex[i + 1])
            i += 2
            continue
            
            
        else:
            result.append(char)
            i += 1
    
    return ''.join(result)

def format_regex(regex):
    """
    Format regex by adding explicit concatenation operators ('.').
    Properly handles character classes, escaped characters, and multi-character tokens.
    """
    all_operators = ['|', '?', '+', '*', '∗', '^']
    binary_operators = ['^', '|']
    result = []
    
    cleaned_regex = regex.replace(' ', '')
    
    i = 0
    while i < len(cleaned_regex):
        char = cleaned_regex[i]
        
        # Handle escaped characters
        if char == '\\' and i + 1 < len(cleaned_regex):
            next_char = cleaned_regex[i + 1]
            if next_char in ['n', 't', 'r', 's', 'd', 'w']:
                token = char + next_char
                result.append(token)
                i += 2
            elif next_char in ['(', ')', '{', '}', '[', ']', '+', '*', '?', '|', '^', '.']:
                result.append(next_char) 
                i += 2
            else:
                token = char + next_char
                result.append(token)
                i += 2
        elif char == '[':
            j = i + 1
            while j < len(cleaned_regex) and cleaned_regex[j] != ']':
                j += 1
            if j < len(cleaned_regex):
                token = cleaned_regex[i:j+1]
                result.append(token)
                i = j + 1
            else:
                result.append(char)
                i += 1
        elif char == '{':
            j = i + 1
            while j < len(cleaned_regex) and cleaned_regex[j] != '}':
                j += 1
            if j < len(cleaned_regex): 
                token = cleaned_regex[i:j+1]
                result.append(token)
                i = j + 1
            else:
                result.append(char)
                i += 1
        else:
            result.append(char)
            i += 1
    
    final_result = []
    for i in range(len(result)):
        token = result[i]
        final_result.append(token)
        
        # Check if we need to add concatenation operator
        if i + 1 < len(result):
            next_token = result[i + 1]
            
            if (token != '(' and 
                token not in binary_operators and
                next_token != ')' and 
                next_token not in all_operators):
                final_result.append('.')
    
    return ''.join(final_result)

def infix_to_postfix(regex):
    """
    Convert infix regex to postfix using Shunting Yard algorithm.
    """
    postfix = []
    stack = []
    formatted_regex = format_regex(regex)
    operators = {'|', '.', '?', '*', '+', '^'}
    
    for c in formatted_regex:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack:
                stack.pop()
        elif c in operators:
            # Handle operators
            while (stack and 
                   stack[-1] != '(' and
                   get_precedence(stack[-1]) >= get_precedence(c)):
                postfix.append(stack.pop())
            stack.append(c)
        else:
            postfix.append(c)
    
    # Pop remaining operators from stack
    while stack:
        postfix.append(stack.pop())
    
    return ''.join(postfix)

def read_regex_from_file(filename):
    """
    Read regex from a text file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    """
    Main function to demonstrate the Shunting Yard algorithm.
    """
    # Test with file input
    filename = input("Enter the filename containing the regex (or press Enter for manual input): ").strip()
    
    if filename:
        regex = read_regex_from_file(filename)
        if regex is None:
            return
    else:
        regex = input("Enter the regular expression: ")
    
    print(f"Original regex: {regex}")
    
    # Preprocess to handle extensions
    preprocessed = preprocess_regex(regex)
    print(f"After preprocessing: {preprocessed}")
    
    # Convert to postfix
    postfix = infix_to_postfix(preprocessed)
    print(f"\nPostfix notation: {postfix}")
    

if __name__ == "__main__":
    main()