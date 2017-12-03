#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Convert all '.pdf' files from current directory and downwards into '.txt' files, using an external command.

Non-ASCII characters are simplified into their ASCII counterpart, and non-meaningful lines are removed.
"""

import codecs
import os
import sys
import tempfile


# We will shell out to this command for converting a PDF file into a TXT file.
PDF2TXT_COMMAND = 'pdf2txt'


xtd = {
    # Letters
    ord(u"à"): u"a", ord(u"â"): u"a", ord(u"å"): u"a", ord(u"á"): u"a", ord(u"ä"): u"a", ord(u"ă"): u"a",
    ord(u"À"): u"A",
    ord(u"ç"): u"c",
    ord(u"Ç"): u"C",
    ord(u"é"): u"e", ord(u"è"): u"e", ord(u"ê"): u"e", ord(u"ë"): u"e", ord(u"ę"): u"e",
    ord(u"É"): u"E", ord(u"Ê"): u"E",
    ord(u"î"): u"i", ord(u"ï"): u"i", ord(u"í"): u"i",
    ord(u"ł"): u"l",
    ord(u"ô"): u"o", ord(u"ö"): u"o", ord(u"ó"): u"o", ord(u"ò"): u"o",
    ord(u"š"): u"s",
    ord(u"û"): u"u", ord(u"ü"): u"u", ord(u"ù"): u"u",
    ord(u"Ú"): u"U",
    # Various quotes and backticks.
    ord(u"’"): u"'", ord(u"‘"): u"'",
    ord(u"«"): u'"', ord(u"»"): u'"',
    ord(u"“"): u'"', ord(u"”"): u'"',
    ord(u"′"): u"'",
    # So many ways to dash.
    ord(u"–"): u"-", ord(u"—"): u"-", ord(u"−"): u"-", ord(u"−"): u"-",
    # Ligatures.
    ord(u"œ"): u"oe", ord(u"ﬁ"): u"fi", ord(u"ﬂ"): u"fl",
    # Probably a PDF conversion bug *or* a source issue.
    ord(u"Ó"): u"e", ord(u"Å"): u"oe", ord(u"Š"): u"",
    # Non-letters.
    ord(u"…"): u"...", ord(u"."): u".", ord(u"®"): u"(R)", ord(u"™"): u"(tm)",
    ord(u"≠"): u"!=", ord(u"≤"): u"<=", ord(u"≥"): u">=",
    ord(u"➀"): u"1", ord(u"➁"): u"2", ord(u"➂"): u"3", ord(u"➃"): u"4", ord(u"➄"): u"5",
    ord(u"§"): u"#", ord(u"∕"): u"/",
    ord(u"∘"): u"o", ord(u"∗"): u"*", ord(u"⋆"): u"*",
    ord(u"←"): u"-", ord(u"➞"): u"-", ord(u"✓"): u"-", ord(u"✗"): u"x",
    ord(u"°"): u"o", ord(u"∞"): u"oo", ord(u"×"): u"x",
    ord(u"μ"): u"u", ord(u"⊕"): u"^",
    ord(u"∈"): u"E", ord(u"¬"): u"~", ord(u"∧"): u"^", ord(u"∨"): u"v",
    ord(u"⋃"): u"U", ord(u"∪"): u"u", ord(u"∀"): u"V", ord(u"δ"): u"d",
    ord(u"≈"): u"~",
    # Euro sign.
    8364: u"E",
    # 𝔽F(p).
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


# Too many CR/LF are hampering readability.
def remove_extra_crlf(data):
    out = ''
    loc_prev = 0

    while True:
        loc_start = data.find('\n', loc_prev)
        if loc_start == -1:
            break

        # 1. Copy input data to output.
        out += data[loc_prev:loc_start]

        # 2. Count amount of '\n'.
        loc_end = loc_start
        while data[loc_end] == '\n':
            if loc_end == len(data)-1:
                break
            loc_end += 1

        if loc_end - loc_start <= 1:
            out += '\n'
        else:
            out += '\n\n'

        loc_prev = loc_end
        if loc_prev == len(data) - 1:
            break

    out += data[loc_prev:]
    return out


# Lines with no meaningful information (e.g. "* * *") can be deleted.
# CR/LF lines are kept and will be processed later on.
def can_delete(l):
    blank = True
    for c in l:
        if c not in ' *\t\r\n':
            # Meaningful character found.
            return False
        if c in ' *':
            blank = False
    if blank:
        return False
    else:
        # No meaningful character found ; yet not a blank line.
        return True


def ebook2plaintext(filename):
    f = '.'.join(filename.split('.')[:-1])
    print 'Converting %s.pdf to %s.txt ...' % (f, f)
	
    tf = tempfile.NamedTemporaryFile()

    # Step 1. Convert PDF file to UTF-8 text.
    status = os.system(PDF2TXT_COMMAND + ' ' + f + '.pdf > ' + tf.name)
    if status != 0:
        print 'Error in PDF conversion!'
        raise ValueError

    # Step 2. Convert UTF-8 text to ASCII text.
    with codecs.open(tf.name, mode='r', encoding='utf-8') as fp:
        d0 = fp.read()
        fp.close()

    # We need to convert character by character, otherwise character sequences do not work :/
    d1 = ''
    for c in d0:
        # This can raise KeyError if the input character is unknown.
        d1 += ascii_convert(c)

    # Step 3. Simplify ASCII text.
    # Lines with no meaningful information will be deleted.
    d2 = ''
    for line in d1.split('\n'):
        if not can_delete(line):
            d2 += line
            d2 += '\n'
    # Remove superfluous '\n'.
    d2 = remove_extra_crlf(d2)

    with open(f + '.txt', 'w') as fp:
        fp.write(d2)
        fp.close()


if __name__ == '__main__':
    count = 0
    base = '.'
    for root, dirs, files in os.walk(base):
        for f in files:
            filename = base + '/' + f
            if filename.endswith('.pdf'):
                ebook2plaintext(filename)
                count += 1
    print 'Processed %d files without issue' % (count)
