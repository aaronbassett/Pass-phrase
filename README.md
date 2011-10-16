# Generate a random pass phrase

![Password Strength by xkcd](http://imgs.xkcd.com/comics/password_strength.png)

Inspired by the 'Password Strength' comic by [xkcd](http://xkcd.com/936/)

# What it does

Pass phrases are 5 words; adjective, noun, verb, adjective, noun. I find this pattern produces 
phrases which are easier to remember/visualise than 4 completely random words as recommended by the xkcd comic. 

## Usage

**From the command line**

    >>> python pass_phrase.py
    elegant pies gather unadvised coal

**In your own scripts**

    >>> from pass_phrase import pass_phrase
    >>> pass_phrase()
    'powerful eye swing wasteful town'