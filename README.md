# Generate a random pass phrase

![Password Strength by xkcd](http://imgs.xkcd.com/comics/password_strength.png)

Inspired by the 'Password Strength' comic by [xkcd](http://xkcd.com/936/)

# What it does

Pass phrases are 5 words; adjective, noun, verb, adjective, noun. I find this pattern produces 
phrases which are easier to remember/visualise than 4 completely random words as recommended by the xkcd comic. 

## Usage

**From the command line**

    $ ./pass_phrase.py
    elegant pies gather unadvised coal

**In your own scripts**

There is no easy way to use it in your own scripts at the moment.
But if you really must use it _right this second_ in your own scripts then 
you can do:

    >>> from pass_phrase import generate_wordlist, passphrase
    >>> adjectives = generate_wordlist("adjectives.txt")
    >>> nouns = generate_wordlist("nouns.txt")
    >>> verbs = generate_wordlist("verbs.txt")
    >>> passphrase(adjectives, nouns, verbs, " ")
    'berserk history offend awful earthquake'

## Word files

The script expects 3 different word files, I've included examples of these in the repo:

+ adjectives.txt
+ nouns.txt
+ verbs.txt

It will check for the existence of these files in the current directory or in `~/.pass-phrase/`

If you want to use other files, or relocate them, use the command line options.

    $ ./pass_phrase.py --adjectives="/usr/share/dict/adjectives" --nouns="/usr/share/dict/nouns" --verbs="/usr/share/dict/verbs"

## Command line options

    Options:
      -h, --help            show this help message and exit
      --adjectives=ADJECTIVES
                            List of valid adjectives for passphrase
      --nouns=NOUNS         List of valid nouns for passphrase
      --verbs=VERBS         List of valid verbs for passphrase
      -s SEPARATOR, --separator=SEPARATOR
                            Separator to add between words
      -n NUM, --num=NUM     Number of passphrases to generate
      --min=MIN_LENGTH      Minimum length of a valid word to use in passphrase
      --max=MAX_LENGTH      Maximum length of a valid word to use in passphrase
      --valid_chars=VALID_CHARS
                            Valid chars, using regexp style (e.g. '[a-z]')
      -U, --uppercase       Force passphrase into uppercase
      -L, --lowercase       Force passphrase into lowercase
      -C, --capitalise, --capitalize
                            Force passphrase to capitalise each word
      --l337                7#izz R3@l|j !$ 4941Nst 7#3 w#()|e 5P|R!7 0pH t#3
                            7#|N6.
      --l337ish             A l337 version which is easier to remember.
      -V, --verbose         Report various metrics for given options


## License

MIT: http://aaron.mit-license.org