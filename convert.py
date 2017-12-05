#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Convert text files from UTF-8 to US-ASCII.
"""

import codecs
import os
import sys
import tempfile


xtd = {
    # Letters
    ord(u"à"): u"a", ord(u"â"): u"a", ord(u"å"): u"a", ord(u"á"): u"a", ord(u"ä"): u"a", ord(u"ă"): u"a",
    ord(u"À"): u"A", ord(u"Á"): u"A",
    ord(u"ç"): u"c",
    ord(u"Ç"): u"C",
    ord(u"é"): u"e", ord(u"è"): u"e", ord(u"ê"): u"e", ord(u"ë"): u"e", ord(u"ę"): u"e",
    ord(u"É"): u"E", ord(u"Ê"): u"E", ord(u"È"): u"E",
    ord(u"î"): u"i", ord(u"ï"): u"i", ord(u"í"): u"i",
    ord(u"Î"): u"I",
    ord(u"ł"): u"l",
    ord(u"ô"): u"o", ord(u"ö"): u"o", ord(u"ó"): u"o", ord(u"ò"): u"o",
    ord(u"Ô"): u"O",
    ord(u"š"): u"s",
    ord(u"û"): u"u", ord(u"ü"): u"u", ord(u"ù"): u"u", ord(u"ú"): u"u",
    ord(u"Ú"): u"U",
    # Various quotes and backticks.
    ord(u"’"): u"'", ord(u"‘"): u"'",
    ord(u"«"): u'"', ord(u"»"): u'"',
    ord(u"“"): u'"', ord(u"”"): u'"',
    ord(u"′"): u"'",
    # So many ways to dash.
    ord(u"–"): u"-", ord(u"—"): u"-", ord(u"−"): u"-", ord(u"−"): u"-", ord(u"·"): u"-",
    # Ligatures.
    ord(u"æ"): u"ae",
    ord(u"ﬁ"): u"fi", ord(u"ﬂ"): u"fl",
    ord(u"œ"): u"oe",
    # Conversion bugs from the original documents.
    ord(u"Ó"): u"e", ord(u"Å"): u"oe", ord(u"Š"): u"", ord(u"ø"): u"o",
    # Non-letters.
    ord(u"…"): u"...", ord(u"."): u".", ord(u"®"): u"(R)", ord(u"™"): u"(tm)", ord(u"ˆ"): u"^",
    ord(u"≠"): u"!=", ord(u"≤"): u"<=", ord(u"≥"): u">=",
    ord(u"➀"): u"1", ord(u"➁"): u"2", ord(u"➂"): u"3", ord(u"➃"): u"4", ord(u"➄"): u"5",
    ord(u"§"): u"#", ord(u"∕"): u"/",
    ord(u"∘"): u"o", ord(u"∗"): u"*", ord(u"⋆"): u"*",
    ord(u"←"): u"-", ord(u"➞"): u"-", ord(u"✓"): u"-", ord(u"✗"): u"x",
    ord(u"°"): u"o", ord(u"∞"): u"oo", ord(u"×"): u"x",
    ord(u"μ"): u"u", ord(u"⊕"): u"^",
    ord(u"∈"): u"E", ord(u"¬"): u"~", ord(u"∧"): u"^", ord(u"∨"): u"v",
    ord(u"⋃"): u"U", ord(u"∪"): u"u", ord(u"∀"): u"V", ord(u"δ"): u"d",
    ord(u"≈"): u"~", ord(u"˜"): u"~",
    ord(u"€"): u"E",
    # 𝔽(p).
    8739: u"F", 55349: u"p", 56637: u"F",
    # There is no optimal conversion for those.
    ord(u"≡"): u"", ord(u"↑"): u""
}


# Map a single character from UTF-8 to ASCII.
def asciify(error):
    return xtd[ord(error.object[error.start])], error.end


# Call asciify() in case of a conversion error.
codecs.register_error('asciify', asciify)


# Convert full text from UTF-8 to ASCII.
def ascii_convert(data):
    return data.encode('ascii', 'asciify')


def utf2ascii(filename):
    f = '.'.join(filename.split('.')[:-1])
    print 'Converting %s.txt to %s.ascii ...' % (f, f)

    with codecs.open(f + '.txt', mode='r', encoding='utf-8') as fp:
        step1 = fp.read()
        fp.close()

    # We need to convert character by character, otherwise character sequences do not work :/
    step2 = ''
    for c in step1:
        # This can raise KeyError if the input character is unknown.
        try:
            step2 += ascii_convert(c)
        except KeyError:
            print step2
            print "bug=", ord(c)
            raise ValueError

    with open(f + '.ascii', 'w') as fp:
        fp.write(step2)
        fp.close()


if __name__ == '__main__':
    count = 0
    base = 'txt'
    for root, dirs, files in os.walk(base):
        for f in files:
            filename = root + '/' + f
            if filename.endswith('.txt'):
                utf2ascii(filename)
                count += 1
    print 'Processed %d files without issue' % (count)
