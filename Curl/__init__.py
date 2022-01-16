from io import StringIO
import urllib
import pycurl
import os
import io
import urllib.parse


class Curl:
    _curl = None
    _timeout = 30
    _connect_timeout = ''
    _referer = ''
    _useragent = ''
    _httpheader = []
    _encoding = ''
    _cookie_file = ''
    _proxy = ''
    _proxyport = ''
    _proxytype = ''
    _proxyuser = ''
    _proxypass = ''
    _followlocation = 1
    _header = 0
    _nosignal = 0
    _auth = {
        'username': '',
        'password': ''
    }
    result = ''
    headers = ''
    http_code = ''
    last_url = ''

    def __init__(self):
        self.open()

    def get(self, url):
        self._do_request(url)

    def post(self, url, postfileds=None):
        if type(postfileds).__name__ == 'dict':
            postfileds = urllib.parse.urlencode(postfileds)

        self._do_request(url, postfileds)

    def _do_request(self, url, postfields=None):
        result = io.BytesIO()
        headers = io.BytesIO()

        self._curl.setopt(pycurl.URL, url)
        self._curl.setopt(pycurl.TIMEOUT, self._timeout)

        if self._connect_timeout:
            self._curl.setopt(pycurl.CONNECTTIMEOUT, self._connect_timeout)

        if self._referer:
            self._curl.setopt(pycurl.REFERER, self._referer)

        if self._useragent:
            self._curl.setopt(pycurl.USERAGENT, self._useragent)

        if self._httpheader:
            self._curl.setopt(pycurl.HTTPHEADER, self._httpheader)

        if self._encoding:
            self._curl.setopt(pycurl.ENCODING, self._encoding)

        if self._cookie_file:
            self._curl.setopt(pycurl.COOKIEFILE, self._cookie_file)
            self._curl.setopt(pycurl.COOKIEJAR, self._cookie_file)

        if self._auth['username'] and self._auth['password']:
            self._curl.setopt(pycurl.USERPWD, '%s:%s' % (self._auth['username'], self._auth['password']))

        if self._proxy and self._proxyport:
            self._curl.setopt(pycurl.PROXY, self._proxy)
            self._curl.setopt(pycurl.PROXYPORT, int(self._proxyport))

            if self._proxyuser and self._proxypass:
                self._curl.setopt(pycurl.PROXYAUTH, pycurl.HTTPAUTH_ANY)
                self._curl.setopt(pycurl.PROXYUSERPWD, '%s:%s' % (self._proxyuser, self._proxypass))

            if self._proxytype == 'SOCKS4':
                self._curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS4)
            elif self._proxytype == 'SOCKS5':
                self._curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)

        self._curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        self._curl.setopt(pycurl.SSL_VERIFYHOST, 0)

        if postfields:
            self._curl.setopt(pycurl.POST, 1)
            self._curl.setopt(pycurl.POSTFIELDS, postfields)
        else:
            self._curl.setopt(pycurl.HTTPGET, 1)

        self._curl.setopt(pycurl.FOLLOWLOCATION, self._followlocation)
        self._curl.setopt(pycurl.HEADER, self._header)
        self._curl.setopt(pycurl.NOSIGNAL, self._nosignal)
        self._curl.setopt(pycurl.WRITEFUNCTION, result.write)
        self._curl.setopt(pycurl.HEADERFUNCTION, headers.write)
        self._curl.perform()

        self.http_code = self._curl.getinfo(pycurl.HTTP_CODE)
        self.last_url = self._curl.getinfo(pycurl.EFFECTIVE_URL)

        self.result = result.getvalue()
        result.close()

        self.headers = headers.getvalue()
        headers.close()

    def set_timeout(self, timeout):
        self._timeout = timeout

    def set_connect_timeout(self, connect_timeout):
        self._connect_timeout = connect_timeout

    def set_referer(self, referer):
        self._referer = referer

    def set_useragent(self, useragent):
        self._useragent = useragent

    def set_httpheader(self, httpheader):
        self._httpheader = httpheader

    def set_encoding(self, encoding):
        self._encoding = encoding

    def set_cookie_file(self, cookie_file):
        self._cookie_file = cookie_file

    def set_followlocation(self, followlocation):
        self._followlocation = followlocation

    def set_header(self, header):
        self._header = header

    def set_nosignal(self, nosignal):
        self._nosignal = nosignal

    def set_auth(self, username, password):
        self._auth = {
            'username': username,
            'password': password
        }

    def set_proxy(self, proxy, proxyport, proxytype='', proxyuser='', proxypass=''):
        self._proxy = proxy
        self._proxyport = proxyport
        self._proxytype = proxytype

        if proxyuser and proxypass:
            self._proxyuser = proxyuser
            self._proxypass = proxypass

    def remove_proxy(self):
        self._proxy = ''
        self._proxyport = ''
        self._proxytype = ''

    def open(self):
        if not self._curl:
            self._curl = pycurl.Curl()

        self._timeout = 30
        self._connect_timeout = ''
        self._referer = ''
        self._useragent = ''
        self._httpheader = []
        self._encoding = ''
        self._cookie_file = ''
        self._proxy = ''
        self._proxyport = ''
        self._proxytype = ''
        self._proxyuser = ''
        self._proxypass = ''
        self._followlocation = 1
        self._header = 0
        self._nosignal = 0
        self._auth = {
            'username': '',
            'password': ''
        }
        self.result = ''
        self.headers = ''
        self.http_code = ''
        self.last_url = ''

    def close(self):
        if self._curl:
            self._curl.close()
            self._curl = None

    def get_cookie(self):
        try:
            if os.path.isfile(self._cookie_file):
                with file(self._cookie_file) as f:
                    return f.read()
        except (SystemExit, KeyboardInterrupt, GeneratorExit, Exception):
            pass

        return ''

    def delete_cookie(self):
        try:
            if os.path.isfile(self._cookie_file):
                os.unlink(self._cookie_file)
        except (SystemExit, KeyboardInterrupt, GeneratorExit, Exception):
            pass

    def __del__(self):
        self.close()
        self.delete_cookie()
