from cudatext import *

ST_NONE = 'n'
ST_BEGIN = 'b'
ST_MIDDLE = 'm'

def log(s):
    print('[DocBlock]', s)

def get_status(ed):
    x0, y0, x1, y1 = ed.get_carets()[0]
    ln = ed.get_text_line(y0)
    end = x0 >= len(ln)
    if ln.rstrip().endswith('/**') and end:
        return ST_BEGIN
    if ln.lstrip().startswith('* '):
        return ST_MIDDLE
    return ST_NONE
    
jsdocs = [
  'abstract',
  'access',
  'alias',
  'arg',
  'argument',
  'augments',
  'author',
  'borrows',
  'callback',
  'class',
  'classdesc',
  'const',
  'constant',
  'constructor',
  'constructs',
  'copyright',
  'default',
  'defaultvalue',
  'deprecated',
  'desc',
  'description',
  'emits',
  'enum',
  'event',
  'example',
  'exception',
  'exports',
  'extends',
  'external',
  'file',
  'fileoverview',
  'fires',
  'func',
  'function',
  'global',
  'host',
  'ignore',
  'inner',
  'instance',
  'kind',
  'lends',
  'license',
  'link',
  'member',
  'memberof',
  'method',
  'mixes',
  'mixin',
  'module',
  'name',
  'namespace',
  'overview',
  'param',
  'private',
  'prop',
  'property',
  'protected',
  'public',
  'readonly',
  'requires',
  'return',
  'returns',
  'see',
  'since',
  'static',
  'summary',
  'this',
  'throws',
  'todo',
  'tutorial',
  'type',
  'typedef',
  'var',
  'variation',
  'version',
  'virtual',
  ]
  
phpdocs = [
  'abstract',
  'access',
  'author',
  'copyright',
  'deprec',
  'deprecated',
  'example',
  'global',
  'ignore',
  'internal',
  'link',
  'name',
  'package',
  'param',
  'php',
  'return',
  'see',
  'since',
  'static',
  'staticvar',
  'subpackage',
  'todo',
  'version',
  ]  

jsdocs = ['jsdoc' + '|' + item + '|' for item in jsdocs]
acp_jsdocs = '\n'.join(jsdocs)+'\n'

phpdocs = ['phpdoc' + '|' + item + '|' for item in phpdocs]
acp_phpdocs = '\n'.join(phpdocs)+'\n'
           

class Command:
    # autocomplete only after "@" or "@text"
    def on_complete(self, ed_self):
        log('on_complete init')
        st = get_status(ed)
        if st!=ST_MIDDLE:
            return log('on_complete bad status: '+str(st))
    
        x0, y0, x1, y1 = ed.get_carets()[0]
        x0init = x0
        while ed.get_text_substr(x0-1, y0, x0, y0).isalpha():
            x0 -= 1
        txt = ed.get_text_substr(x0-1, y0, x0, y0)
        if txt != '@':
            log('on_complete not after @')
            return

        lex = ed.get_prop(PROP_LEXER_CARET)
        if 'Script' in lex or lex=='JSDoc':
            text = acp_jsdocs
            log('lexer JS')
        else:
            text = acp_phpdocs
            log('lexer PHP')
        
        chars_num = x0init-x0
        ed.complete(text, chars_num, 0)
        return True            

    def on_key(self, ed_self, key, state):
        log('on_key init')
        ed = ed_self
        st = get_status(ed)
        eol = '\n'
        if st==ST_NONE:
            return log('on_key bad status: '+str(st))
        if key!=13:
            return log('on_key unknown key')

        x, y, x1, y1 = ed.get_carets()[0]
            
        if st==ST_BEGIN:
            ln = ed.get_text_line(y)
            pos = ln.find('/')
            indent = ' '*pos
            ed.insert(x, y, eol+indent+'* '+eol+indent+'*/')
            ed.set_caret(len(indent)+3, y+1)
            return False #block Enter
            
        if st==ST_MIDDLE:
            ln = ed.get_text_line(y)
            pos = ln.find('*')
            indent = ' '*pos
            ed.insert(x, y, eol+indent+'* ')
            ed.set_caret(len(indent)+3, y+1)
            return False #block Enter
