#!/usr/bin/env python
# encoding: utf-8

import random
import optparse
import sys
import re
import os
import math
import datetime

__LICENSE__ = """
The MIT License (MIT)

Copyright (c) 2012 Aaron Bassett, http://aaronbassett.com

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# random.SystemRandom() should be cryptographically secure
try:
    rng = random.SystemRandom
except AttributeError:
    sys.stderr.write("WARNING: System does not support cryptographically "
                     "secure random number generator or you are using Python "
                     "version < 2.4.\n"
                     "Continuing with less-secure generator.\n")
    rng = random.Random


# Python 3 compatibility
if sys.version[0] == "3":
    raw_input = input


def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """
    
    if options.num <= 0:
        sys.stderr.write("Little point running the script if you "
                         "don't generate even a single pass phrase.\n")
        sys.exit(1)

    if options.max_length < options.min_length:
        sys.stderr.write("The maximum length of a word can not be "
                         "lesser then minimum length.\n"
                         "Check the specified settings.\n")
        sys.exit(1)

    if len(args) >= 1:
        parser.error("Too many arguments.")

    for word_type in ["adjectives", "nouns", "verbs"]:
        wordfile = getattr(options, word_type, None)
        if wordfile is not None:
            if not os.path.exists(os.path.abspath(wordfile)):
                sys.stderr.write("Could not open the specified {0} word file.\n".format(word_type))
                sys.exit(1)
        else:
            common_word_file_locations = ["{0}.txt", "~/.pass-phrase/{0}.txt"]

            for loc in common_word_file_locations:
                wordfile = loc.format(word_type)
                if os.path.exists(wordfile):
                    setattr(options, word_type, wordfile)
                    break

        if getattr(options, word_type, None) is None:
            sys.stderr.write("Could not find {0} word file, or word file does not exist.\n".format(word_type))
            sys.exit(1)


def generate_wordlist(wordfile=None,
                      min_length=0,
                      max_length=20,
                      valid_chars='.'):
    """
    Generate a word list from either a kwarg wordfile, or a system default
    valid_chars is a regular expression match condition (default - all chars)
    """

    words = []

    regexp = re.compile("^%s{%i,%i}$" % (valid_chars, min_length, max_length))

    # At this point wordfile is set
    wordfile = os.path.expanduser(wordfile)  # just to be sure
    wlf = open(wordfile)

    for line in wlf:
        thisword = line.strip()
        if regexp.match(thisword) is not None:
            words.append(thisword)

    wlf.close()
    
    if len(words) < 1:
        sys.stderr.write("Could not get enough words!\n")
        sys.stderr.write("This could be a result of either {0} being too small,\n".format(wordfile))
        sys.stderr.write("or your settings too strict.\n")
        sys.exit(1)

    return words
    

def craking_time(seconds):
    minute = 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    
    if seconds < 60:
        return "less than a minute"
    elif seconds < 60 * 5:
        return "less than 5 minutes"
    elif seconds < 60 * 10:
        return "less than 10 minutes"
    elif seconds < 60 * 60:
        return "less than an hour"
    elif seconds < 60 * 60 * 24:
        hours, r = divmod(seconds, 60 * 60)
        return "about %i hours" % hours
    elif seconds < 60 * 60 * 24 * 14:
        days, r = divmod(seconds, 60 * 60 * 24)
        return "about %i days" % days
    elif seconds < 60 * 60 * 24 * 7 * 8:
        weeks, r = divmod(seconds, 60 * 60 * 24 * 7)
        return "about %i weeks" % weeks
    elif seconds < 60 * 60 * 24 * 365 * 2:
        months, r = divmod(seconds, 60 * 60 * 24 * 7 * 4)
        return "about %i months" % months
    else:
        years, r = divmod(seconds, 60 * 60 * 24 * 365)
        return "about %i years" % years


def verbose_reports(**kwargs):
    """
    Report entropy metrics based on word list size"
    """
    
    options = kwargs.pop("options")
    f = {}

    for word_type in ["adjectives", "nouns", "verbs"]:
        print("The supplied {word_type} list is located at {loc}.".format(
            word_type=word_type,
            loc=os.path.abspath(getattr(options, word_type))
        ))
        
        words = kwargs[word_type]
        f[word_type] = {}
        f[word_type]["length"] = len(words)
        f[word_type]["bits"] = math.log(f[word_type]["length"], 2)

        if (int(f[word_type]["bits"]) == f[word_type]["bits"]):
            print("Your %s word list contains %i words, or 2^%i words."
                  % (word_type, f[word_type]["length"], f[word_type]["bits"]))
        else:
            print("Your %s word list contains %i words, or 2^%0.2f words."
                  % (word_type, f[word_type]["length"], f[word_type]["bits"]))
    
    entropy = f["adjectives"]["bits"] +\
              f["nouns"]["bits"] +\
              f["verbs"]["bits"] +\
              f["adjectives"]["bits"] +\
              f["nouns"]["bits"]
    
    print("A passphrase from this list will have roughly "
          "%i (%0.2f + %0.2f + %0.2f + %0.2f + %0.2f) bits of entropy, " % (
              entropy,
              f["adjectives"]["bits"],
              f["nouns"]["bits"],
              f["verbs"]["bits"],
              f["adjectives"]["bits"],
              f["nouns"]["bits"]
          ))

    combinations = math.pow(2, int(entropy)) / 1000
    time_taken = craking_time(combinations)
    
    print "Estimated time to crack this pass phrase (at 1,000 guesses per second): %s\n" % time_taken

def generate_passphrase(adjectives, nouns, verbs, interactive=False):
    return "{0} {1} {2} {3} {4}".format(
        rng().choice(adjectives),
        rng().choice(nouns),
        rng().choice(verbs),
        rng().choice(adjectives),
        rng().choice(nouns)
    )


def passphrase(adjectives, nouns, verbs, num=1):
    """
    Returns a random pass-phrase made up of
    adjective noun verb adjective noun
    
    I find this basic structure easier to 
    remember than XKCD style purely random words
    """
    
    phrases = []

    for i in range(0, num):
        phrases.append(generate_passphrase(adjectives, nouns, verbs))

    return "\n".join(phrases)


if __name__ == "__main__":

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    
    parser.add_option("--adjectives", dest="adjectives",
                      default=None,
                      help="List of valid adjectives for password")
                      
    parser.add_option("--nouns", dest="nouns",
                      default=None,
                      help="List of valid nouns for password")
                      
    parser.add_option("--verbs", dest="verbs",
                      default=None,
                      help="List of valid verbs for password")
                      
    parser.add_option("-n", "--num", dest="num",
                      default=1, type="int",
                      help="Number of passphrases to generate")
                      
    parser.add_option("--min", dest="min_length",
                      default=0, type="int",
                      help="Minimum length of a valid word to use in passphrase")
                      
    parser.add_option("--max", dest="max_length",
                      default=20, type="int",
                      help="Maximum length of a valid word to use in passphrase")
                      
    parser.add_option("--valid_chars", dest="valid_chars",
                      default='.',
                      help="Valid chars, using regexp style (e.g. '[a-z]')")
    parser.add_option("-V", "--verbose", dest="verbose",
                      default=False, action="store_true",
                      help="Report various metrics for given options")
    
    (options, args) = parser.parse_args()
    validate_options(options, args)
    
    # Generate word lists
    adjectives = generate_wordlist(wordfile=options.adjectives,
                              min_length=options.min_length,
                              max_length=options.max_length,
                              valid_chars=options.valid_chars)
    
    nouns = generate_wordlist(wordfile=options.nouns,
                              min_length=options.min_length,
                              max_length=options.max_length,
                              valid_chars=options.valid_chars)
    
    verbs = generate_wordlist(wordfile=options.verbs,
                              min_length=options.min_length,
                              max_length=options.max_length,
                              valid_chars=options.valid_chars)
    
    if options.verbose:
        verbose_reports(adjectives=adjectives,
                        nouns=nouns,
                        verbs=verbs,
                        options=options)
    
    print(passphrase(
            adjectives,
            nouns,
            verbs,
            num=int(options.num)
        )
    )
