Plugin "DocBlock" for CudaText.
It helps to enter docblock comments for lexers: PHP, JavaScript, CoffeeScript.

  /**
   * Some text
   * here
   */

1) It handles Enter key press. Plugin looks, if end of current line is "/**", if so then empty docblock is entered and caret placed in it. If you type middle of docblock, ie begin of current line is indent + "* ", then plugin enters "* " on next line too.

2) Auto-completion works, for JavaScript and PHP: inside docblock type "@" and press Ctrl+Space (ie hotkey for auto-completion): you'll see list of JSDoc or PHPDoc tags. 


Author: Alexey Torgashin (CudaText)
License: MIT