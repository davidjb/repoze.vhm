##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import unittest

class TestXHeaders(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.vhm.middleware import VHMFilter
        return VHMFilter

    def _makeOne(self, app):
        return self._getTargetClass()(app)

    def test___call___no_markers_unchanged(self):
        # Environments which do not have markers don't get munged.
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'example.com',
                   'SERVER_PORT': '8888',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected.get('wsgi.url_scheme'), 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '8888')
        self.assertEqual(expected['SCRIPT_NAME'], '/')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected.get('repoze.vhm.virtual_url'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_host_base'), None)

    def test___call___X_VHM_HOST_only_explicit_port(self):
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        X_VHM_HOST = 'http://example.com:80/script'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                   'HTTP_X_VHM_HOST': X_VHM_HOST,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/script/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___X_VHM_HOST_only_default_port(self):
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        X_VHM_HOST = 'http://example.com:80/script'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                   'HTTP_X_VHM_HOST': X_VHM_HOST,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/script/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___X_VHM_ROOT(self):
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        X_VHM_ROOT = '/a/b'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                   'HTTP_X_VHM_ROOT': X_VHM_ROOT,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected.get('wsgi.url_scheme'), 'http')
        self.assertEqual(expected['SERVER_NAME'], 'localhost')
        self.assertEqual(expected['SERVER_PORT'], '8080')
        self.assertEqual(expected['SCRIPT_NAME'], '/')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://localhost:8080/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), '/a/b')
        self.assertEqual(expected.get('repoze.vhm.virtual_host_base'), None)

class TestExplicit(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.vhm.middleware import VHMExplicitFilter
        return VHMExplicitFilter

    def _makeOne(self, app, host=None, root=None):
        return self._getTargetClass()(app, host, root)

    def test___call___no_markers_unchanged(self):
        # Environments which do not have markers don't get munged.
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'example.com',
                   'SERVER_PORT': '8888',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected.get('wsgi.url_scheme'), 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '8888')
        self.assertEqual(expected['SCRIPT_NAME'], '/')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected.get('repoze.vhm.virtual_url'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_host_base'), None)

    def test___call___host_only_explicit_port(self):
        expected = {}
        app = VHMTestApp(expected)
        X_VHM_HOST = 'http://example.com:80/script'
        filter = self._makeOne(app, host=X_VHM_HOST)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/script/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___host_only_default_port(self):
        expected = {}
        app = VHMTestApp(expected)
        X_VHM_HOST = 'http://example.com:80/script'
        filter = self._makeOne(app, host=X_VHM_HOST)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/script/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___root(self):
        expected = {}
        app = VHMTestApp(expected)
        X_VHM_ROOT = '/a/b'
        filter = self._makeOne(app, root=X_VHM_ROOT)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected.get('wsgi.url_scheme'), 'http')
        self.assertEqual(expected['SERVER_NAME'], 'localhost')
        self.assertEqual(expected['SERVER_PORT'], '8080')
        self.assertEqual(expected['SCRIPT_NAME'], '/')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://localhost:8080/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), '/a/b')
        self.assertEqual(expected.get('repoze.vhm.virtual_host_base'), None)


class TestVHMPathFilter(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.vhm.middleware import VHMPathFilter
        return VHMPathFilter

    def _makeOne(self, app):
        return self._getTargetClass()(app)

    def test___call___no_markers_unchanged(self):
        # Environments which do not have markers don't get munged.
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'example.com',
                   'SERVER_PORT': '8888',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected.get('wsgi.url_scheme'), 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '8888')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected.get('repoze.vhm.virtual_url'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected.get('repoze.vhm.virtual_host_base'), None)

    def test___call___VirtualHostBase_only_default_port(self):
        # VHB: consume next two tokens, converts to new scheme / netloc.
        #      Note we preserve the port here (elided by 'setServerURL').
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        PREFIX = '/VirtualHostBase/http/example.com:80'
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': PREFIX + REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___VirtualHostBase_only_strange_port(self):
        # VHB: consume next two tokens, converts to new scheme / netloc.
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        PREFIX = '/VirtualHostBase/http/example.com:8000'
        REAL_PATH = '/a/b/c/'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': PREFIX + REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '8000')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com:8000/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), None)
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:8000')

    def test___call___VirtualHostRoot_no_subpath(self):
        # VHR immediately following VHB + 2 -> no vroot.
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        PREFIX = '/VirtualHostBase/https/example.com:443/VirtualHostRoot'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': PREFIX + REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'https')
        self.assertEqual(expected['repoze.vhm.virtual_root'], '/')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '443')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'https://example.com/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), '/')
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:443')

    def test___call___VirtualHostRoot_w_subpath(self):
        # Tokens after VHB + 2, before VHR -> vroot
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        PREFIX = '/VirtualHostBase/http/example.com:80/sub1/VirtualHostRoot'
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': PREFIX + REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['repoze.vhm.virtual_root'], '/sub1')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/script')
        self.assertEqual(expected['PATH_INFO'], '/sub1' + REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), '/sub1')
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

    def test___call___VirtualHostRoot__vh__externals(self):
        # special tokens after VHR -> script name ("external" prefix).
        expected = {}
        app = VHMTestApp(expected)
        filter = self._makeOne(app)
        REAL_PATH = '/a/b/c/'
        PREFIX = ('/VirtualHostBase/http/example.com:80/VirtualHostRoot'
                  '/_vh_sub1/_vh_sub2')
        environ = {'wsgi.url_scheme': 'http',
                   'SERVER_NAME': 'localhost',
                   'SERVER_PORT': '8080',
                   'SCRIPT_NAME': '/script',
                   'PATH_INFO': PREFIX + REAL_PATH,
                  }

        filter(environ, noopStartResponse)

        self.assertEqual(expected['wsgi.url_scheme'], 'http')
        self.assertEqual(expected['SERVER_NAME'], 'example.com')
        self.assertEqual(expected['SERVER_PORT'], '80')
        self.assertEqual(expected['SCRIPT_NAME'], '/sub1/sub2')
        self.assertEqual(expected['PATH_INFO'], REAL_PATH)
        self.assertEqual(expected['repoze.vhm.virtual_url'], 'http://example.com/sub1/sub2/a/b/c')
        self.assertEqual(expected.get('repoze.vhm.virtual_root'), '/')
        self.assertEqual(expected['repoze.vhm.virtual_host_base'],
                         'example.com:80')

def noopStartResponse(status, headers):
    pass

class VHMTestApp:
    def __init__(self, _called_environ):
        self._called_environ = _called_environ

    def __call__(self, environ, start_response):
        self._called_environ.clear()
        self._called_environ.update(environ)
        return self.__class__.__name__
