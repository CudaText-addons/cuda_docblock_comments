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

JSDOCS = [
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

PHPDOCS = [
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

def get_completions(word, is_js):
    prefix = 'jsdoc' if is_js else 'phpdoc'
    tags = JSDOCS if is_js else PHPDOCS
    if bool(word):
        tags = [t for t in tags if t.startswith(word)]
    items = [prefix + '|' + t + '|' for t in tags]
    return '\n'.join(items)+'\n'


class Command:
    # autocomplete only after "@" or "@text"
    def on_complete(self, ed_self):
        log('on_complete init')
        st = get_status(ed)
        if st!=ST_MIDDLE:
            return log('on_complete bad status: '+str(st))

        x0, y0, x1, y1 = ed.get_carets()[0]
        line = ed.get_text_line(y0) 
        if x0>len(line):
            return log('on_complete, after line end')
        x0init = x0
        
        while (x0>0) and line[x0-1].isalpha():
            x0 -= 1
        txt = line[x0-1]
        if txt != '@':
            return log('on_complete not after @')

        lex = ed.get_prop(PROP_LEXER_CARET)
        is_js = 'Script' in lex or lex=='JSDoc'
        word = line[x0:x0init]
        text = get_completions(word, is_js)
        
        len1 = len(word)
        
        x2 = x0init
        while x2<len(line) and line[x2].isalpha():
            x2 += 1
        len2 = x2-x0init

        log('on_complete, word="%s" len1=%d len2=%d'%(word, len1, len2))
        ed.complete(text, len1, len2)
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
            pos = ln.find('/**')
            indent = ' '*(pos+1)
            ed.insert(x, y, eol+indent+'* '+eol+indent+'*/')
            ed.set_caret(len(indent)+3, y+1)
            return False #block Enter

        if st==ST_MIDDLE:
            ln = ed.get_text_line(y)
            pos = ln.find('* ')
            indent = ' '*pos
            ed.insert(x, y, eol+indent+'* ')
            ed.set_caret(len(indent)+3, y+1)
            return False #block Enter
