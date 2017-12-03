#!/usr/bin/env python

"""
Scrape all PDF files from 2013 to 2017.
Files are saved in the current directory.

Note: The first file ever is "CERTA-2004-ACT-001.pdf".
"""

import requests

def save_to_disk(y, w):
    if (y < 2014) or ((y == 2014) and (w <= 3)):
        filename = 'CERTA'
    else:
        filename = 'CERTFR'
    filename += '-%d-ACT-%03d.pdf' % (y, w)
    url = 'http://www.cert.ssi.gouv.fr/pdf/%s' % filename
    print 'Fetching %s ...' % (url)
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as fp:
            fp.write(r.content)
            fp.close()
    else:
        print 'Error %d' % (r.status_code)
    return


if __name__ == '__main__':
    for year in range(2013, 2018):
        for week in range(1, 53):
            save_to_disk(year, week)