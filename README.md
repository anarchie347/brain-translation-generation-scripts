# Brain Translation Generation Scripts

This is a series of code files used to generate hard-coded strings used for translations in the brain compiler, e.g. the Brain32 -> brainfuck translation of the '+' symbol.

Including generation fo these in the main compiler would lead to lots of wasted computation (could be reduced by memoising or evaluating at compile time), but it is still wasted time.

Each file is self-contained and contains code for translating from a given language only.