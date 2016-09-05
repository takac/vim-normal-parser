import ply.yacc as yacc
import ply.lex as lex

from vimlex import tokens

# w			[count] words forward.
# W			[count] WORDS forward.
# e			Forward to the end of word [count].
# E			Forward to the end of WORD [count].
# b			[count] words backward.
# B			[count] WORDS backward.

ops = {'d': 'delete', 'c': 'change', 'y': 'yank'}
motions = {
        'w': {'single': 'word forward', 'multi': '{count} words forward'},
        'W': {'single': 'WORD forward', 'multi': '{count} WORDS forward'},
        'e': {'single': 'forward to end of word', 'multi': 'forward to end of {count} words'},
        'E': {'single': 'forward to end of WORD', 'multi': 'forward to end of {count} WORDS'},
        'h': {'single': 'left', 'multi': 'left {count} chars'},
        'l': {'single': 'right', 'multi': 'right {count} chars'},
        'l': {'single': 'line upwards', 'multi': '{count} lines upward'},
        'j': {'single': 'line downwards', 'multi': '{count} lines downward'},
        '{': {'single': 'paragraph downwards', 'multi': '{count} paragraphs downward'},
        }
text_objs = {'w': 'word', 'p': 'paragraph', 's': 'sentence', '}': 'curly brace block'}
modifiers = {'a': 'around', 'i': 'inside'}

def format_op_text_obj(op, mod, obj, op_rep=1, obj_rep=1):
    out = {'op_rep': op_rep, 'op': ops[op], 'mod': modifiers[mod], 'obj_rep': obj_rep, 'text_obj': text_objs[obj]}
    format = "{op_rep} {op} {mod} {obj_rep} {text_obj}"
    if op_rep == 1:
        format = format.replace("{op_rep} ", "")
    if obj_rep == 1:
        format = format.replace("{obj_rep} ", "")
    return format.format(**out)

def format_op_action(op, motion, op_rep=1, motion_rep=1):
    if motion_rep == 1:
        return "{} {} {}".format(op_rep, ops[op], motions[motion]['single'])
    return "{} {} {}".format(op_rep, ops[op], motions[motion]['multi'].format(count=motion_rep))

def p_rep_operator_rep_motion(p):
    'operator_motion : NUMBER OPERATOR NUMBER MOTION'
    p[0] = format_op_action(p[2], p[4], op_rep=p[1], motion_rep=p[3])

def p_rep_operator_motion(p):
    'operator_motion : NUMBER OPERATOR MOTION'
    p[0] = format_op_action(p[2], p[3], op_rep=p[1])

def p_operator_rep_motion(p):
    'operator_motion : OPERATOR NUMBER MOTION'
    p[0] = format_op_action(p[1], p[3], motion_rep=p[2])

def p_operator_motion(p):
    'operator_motion : OPERATOR MOTION'
    p[0] = format_op_action(p[1], p[2])

def p_operator_rep_mod_textobj(p):
    'operator_motion : OPERATOR NUMBER TEXTOBJMOD TEXTOBJ'
    p[0] = format_op_text_obj(p[1], p[3], p[4], obj_rep=p[2])

def p_rep_operator_rep_mod_textobj(p):
    'operator_motion : NUMBER OPERATOR NUMBER TEXTOBJMOD TEXTOBJ'
    p[0] = format_op_text_obj(p[2], p[4], p[5], op_rep=p[1], obj_rep=p[3])

def p_rep_operator_mod_textobj(p):
    'operator_motion : NUMBER OPERATOR TEXTOBJMOD TEXTOBJ'
    p[0] = format_op_text_obj(p[2], p[3], p[4], op_rep=p[1])

def p_operator_mod_textobj(p):
    'operator_motion : OPERATOR TEXTOBJMOD TEXTOBJ'
    p[0] = format_op_text_obj(p[1], p[2], p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

if __name__ == '__main__':
    parser = yacc.yacc()

    while True:
       try:
           s = raw_input('normal> ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print(result)
