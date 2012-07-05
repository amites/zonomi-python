import urllib2

import settings

try:
    from findip import findIP
except ImportError:
    def findIP():
        raise Exception('findIP not implemented.')


class Zonomi(object):
    """
    Simple wrapper for Zonomi DNS service API.
    """

    def __init__(self, **kwargs):
        self.api_key = kwargs.get('api_key', settings.api_key)
        self.base_url = kwargs.get('base_url',
                        'https://zonomi.com/app/dns')
        self.domain = kwargs.get('domain', False)
        self.ip = kwargs.get('ip', settings.ip)

    def buildArgStr(self, **kwargs):
        """
        Generator to compile a dictionary into a URI string.
        """
        arg_str = 'api_key=%s&' % self.api_key
        for items in kwargs.items():
            arg_str += '='.join(items) + '&'
        return arg_str[:-1]

    def multiArgStr(self, args_list):
        """
        Generator to build a list of dictionaries into a URI string.
        """
        arg_str = ''
        for args_dict in args_list:
            arg_str += self.buildArgStr(**args_dict)
        return arg_str

    def connect(self, command='dyndns', **kwargs):
        """
        Execute an API call to Zonomi.
        """
        if kwargs.get('arg_str', False):
            arg_str = kwargs.get('arg_str')
        else:
            arg_str = self.buildArgStr(**kwargs)

        try:
            response = urllib2.urlopen(
                        '{0[base_url]}/{0[page]}.jsp?{0[arg_str]}'.format({
                            'base_url' : self.base_url,
                            'page' : command,
                            'arg_str' : arg_str
                        }))

            page = response.read()
            return page
        except urllib2.HTTPError, e:
            return e

    def multiConnect(self, arg_dict, **kwargs):
        """
        Build and execute the URI string for multiple function API calls.
        """
        arg_str = 'api_key=%s&' % self.api_key
        for i, args in enumerate(arg_dict):
            try:
                args = dict(kwargs.items() + args.items())
            except AttributeError:
                print kwargs
                print arg_dict
            for var, val in args.iteritems():
                arg_str += '{0[var]}[{0[index]}]={0[val]}&'.format({
                    'var' : var,
                    'index' : i + 1,
                    'val' : val,
                })
        return self.connect('dyndns', arg_str=arg_str[:-1])

    def checkMultiDict(self, dict_obj):
        """
        Simple generator to build a list of dictionaries or raise an Exception.
        """
        if type(dict_obj) == dict:
            return [dict_obj, ]
        elif type(dict_obj) == list:
            if type(dict_obj[0]) == dict:
                return dict_obj
        raise Exception(str('Dict obj is invalid, must pass a dict or'
                                        ' list of dicts to function.'))

    def addZone(self, domain=False):
        """
        Add a new zone (domain) to your account.
        """
        if not domain:
            domain = self.domain
        return self.connect('addzone', name=domain)

    def addDomain(self, domain=False):
        """
        Shortcut to addZone.
        """
        return self.addZone(domain)

    def newZone(self, domain=False, ip=False):
        """
        Creates a new Zone and sets the IP address.
        """
        self.addZone(domain)
        self.setIP(domain, ip)
        self.setIP('*.%s' % domain, ip)

    def newDomain(self, domain=False, ip=False):
        """
        Shortcut to newZone.
        """
        return self.newZone(domain, ip)

    def setIP(self, domain=False, ip=False, type='A'):
        if not ip:
            if self.ip:
                ip = self.ip
            else:
                ip = findIP()

        if not domain:
            if self.domain:
                domain = self.domain
            else:
                raise Exception('No domain to set an IP for.')
        return self.connect('dyndns', name=domain, value=ip,
                                        action='SET', type=type)

    def setGmail(self, domain=False):
        """
        Shortcut to set MX entries for Google Apps on given domain.
        Will default to using the current class
        """
        gmail_mx = [
            {
                'value' : 'ALT1.ASPMX.L.GOOGLE.COM',
                'prio' : '5',
            },
            {
                'value' : 'ALT2.ASPMX.L.GOOGLE.COM',
                'prio' : '5',
            },
            {
                'value' : 'ASPMX.L.GOOGLE.COM',
                'prio' : '1',
            },
            {
                'value' : 'ASPMX2.GOOGLEMAIL.COM',
                'prio' : '10',
            },
            {
                'value' : 'ASPMX3.GOOGLEMAIL.COM',
                'prio' : '10',
            },
        ]
        return self.setMXRecords(gmail_mx, domain)


    def setMXRecords(self, mx_dict, domain=False):
        """
        Wrapper to set MX records for supplied domain using a required dict or
        dict list in format:
        [
            {
                'value' : 'DOMAIN',
                'prio' : 'INTEGER',
            },
        ]
        """
        if not domain:
            domain = self.domain
        return self.multiConnect(mx_dict, name=domain, type='MX',
                                        action='SET')

    def delZone(self, domain):
        """
        Deletes the supplied domain name entry.
        """
        return self.connect('dyndns', name=domain, action='DELETEZONE')

    def setARecords(self, ns_dict, domain=False):
        """
        Creates a new A record
        """
        if type(ns_dict) == dict:
            ns_dict = [ns_dict, ]
        return self.multiConnect(ns_dict, name=domain,
                                action='SET', type='A')

    def setZonomiNS(self, domain=False):
        """
        Create NS records to point to Zonomi for a vanity Nameserver.
        """
        if not domain:
            domain = self.domain
        ns_dict = [
            {
                'name' : 'ns1.%s' % domain,
                'value' : '74.50.54.250',
            },
            {
                'name' : 'ns2.%s' % domain,
                'value' : '94.76.200.250',
            },
            {
                'name' : 'ns3.%s' % domain,
                'value' : '60.234.72.250',
            },
            {
                'name' : 'ns4.%s' % domain,
                'value' : '66.199.224.250',
            },
        ]
        return self.multiConnect(ns_dict, action='SET', type='A')

