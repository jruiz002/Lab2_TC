# Shunting Yard Algorithm for Regular Expressions

This project implements the Shunting Yard algorithm in Python to convert regular expressions from infix to postfix notation, with support for escaped characters and regex extensions.

## Features

- **Shunting Yard Algorithm**: Converts infix regex to postfix notation
- **Escaped Character Support**: Handles characters escaped with backslash (\)
- **Regex Extensions**: Converts `+` and `?` operators to basic regex operations
  - `a+` becomes `aa*` (one or more)
  - `a?` becomes `(a|ε)` (zero or one)
- **File Input**: Reads regex patterns from text files
- **Precedence Handling**: Proper operator precedence for regex operators

## Prerequisites

You need Python installed on your system. If Python is not installed:

### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and make sure to check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing: `python --version`

### Alternative (Microsoft Store):
1. Open Microsoft Store
2. Search for "Python"
3. Install Python 3.x

## Files

- `shunting_yard.py`: Main implementation file
- `test_regex.txt`: Sample regex file for testing
- `README.md`: This documentation file

## Usage

### Running the Program

```bash
python shunting_yard.py
```

The program will prompt you to:
1. Enter a filename containing a regex pattern, or
2. Press Enter to input the regex manually

### Example Usage

```
Enter the filename containing the regex (or press Enter for manual input): test_regex.txt
Original regex: (a+|b)*c?
After preprocessing: ((aa*|b)*)(c|ε)
Postfix notation: aa*.b|*.c.ε|.
```

### Manual Input Example

```
Enter the filename containing the regex (or press Enter for manual input): 
Enter the regular expression: a+b?
Original regex: a+b?
After preprocessing: aa*(b|ε)
Postfix notation: aa*b.ε|.
```

## Algorithm Details

### Operator Precedence

1. `(` - Parentheses (lowest precedence)
2. `|` - Alternation (OR)
3. `.` - Concatenation
4. `?`, `*`, `+` - Quantifiers
5. `^` - Exponentiation (highest precedence)

### Preprocessing Steps

1. **Escape Handling**: Preserves escaped characters as literals
2. **Extension Conversion**:
   - `a+` → `aa*` (one or more occurrences)
   - `a?` → `(a|ε)` (zero or one occurrence)
3. **Concatenation**: Adds explicit `.` operators where needed

### Test Cases

The program includes built-in test cases:
- `a+b` → `aa*b` → `aa*b.`
- `a?b` → `(a|ε)b` → `a.ε|b.`
- `(a|b)*` → `(a|b)*` → `ab|*`
- `\\+a` → `\\+a` → `\\+a.` (escaped plus)

## Implementation Notes

- The algorithm follows the standard Shunting Yard approach
- Escaped characters are handled during preprocessing
- The `ε` symbol represents epsilon (empty string)
- Parentheses are properly balanced and processed
- The implementation handles complex nested expressions

## Error Handling

- File not found errors are caught and reported
- Invalid regex patterns are processed as-is (no validation)
- Empty input is handled gracefully

## Extending the Code

To add new operators:
1. Update the `get_precedence()` function
2. Add handling in `preprocess_regex()` if needed
3. Update the `all_operators` and `binary_operators` lists in `format_regex()`