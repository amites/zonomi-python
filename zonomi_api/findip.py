#!/usr/bin/python

import urllib2

#
# Simple python script to return your public IP address using whatismyip.com
# if executed from command line will display IP
#

def findIP():
    '''
    Returns your IP address. Includes setting the header to match the request
    see http://www.whatismyip.com/faq/automation.asp
    '''
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0)'\
    + ' Gecko/20100101 Firefox/12.0' }
    return urllib2.urlopen(
        urllib2.Request(
            "http://automation.whatismyip.com/n09230945.asp",
            None, headers )
    ).read()


if __name__=="__main__":
    print findIP()
