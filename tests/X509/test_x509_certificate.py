# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import mock

import sys
import textwrap

from anchor.X509 import certificate
from anchor.X509 import errors as x509_errors
from anchor.X509 import name as x509_name


# find the class representing an open file; it depends on the python version
# it's used later for mocking
if sys.version_info[0] < 3:
    file_class = file
else:
    import _io
    file_class = _io.TextIOWrapper


class TestX509Cert(unittest.TestCase):
    cert_data = textwrap.dedent("""
        -----BEGIN CERTIFICATE-----
        MIICKjCCAZOgAwIBAgIIfeW6dwGe6wMwDQYJKoZIhvcNAQEFBQAwUjELMAkGA1UE
        BhMCQVUxEzARBgNVBAgTClNvbWUtU3RhdGUxFjAUBgNVBAoTDUhlcnAgRGVycCBw
        bGMxFjAUBgNVBAMTDWhlcnAuZGVycC5wbGMwHhcNMTUwMTE0MTQxMDE5WhcNMTUw
        MTE1MTQxMDE5WjCBlDELMAkGA1UEBhMCVUsxDzANBgNVBAgTBk5hcm5pYTESMBAG
        A1UEBxMJRnVua3l0b3duMRcwFQYDVQQKEw5BbmNob3IgVGVzdGluZzEQMA4GA1UE
        CxMHdGVzdGluZzEUMBIGA1UEAxMLYW5jaG9yLnRlc3QxHzAdBgkqhkiG9w0BCQEW
        EHRlc3RAYW5jaG9yLnRlc3QwTDANBgkqhkiG9w0BAQEFAAM7ADA4AjEA6m/GQLE0
        1NzzoZWc/ita9qeI6cdp6ZduEE6gXGEzBqCGKru7lX1kqRRl9u74v5lJAgMBAAGj
        GjAYMAkGA1UdEwQCMAAwCwYDVR0PBAQDAgXgMA0GCSqGSIb3DQEBBQUAA4GBAGeX
        hSul19/DgwM5m3cj6y9+dkOhXCdImG1O6wjDHxa/xU+hlPJwGZr5zrcBsk/8jaIP
        z1FWAhsmZBl0zSJY7XEZ9jmw7JIaCy3XpYMVEA2LGEofydr7N3CRqIE5ehdAh5rz
        gTLni27WuVJFVBNoTU1JfoxBSm/RBLdTj92g9N5g
        -----END CERTIFICATE-----""")

    def setUp(self):
        super(TestX509Cert, self).setUp()
        self.cert = certificate.X509Certificate()
        self.cert.from_buffer(TestX509Cert.cert_data)

    def tearDown(self):
        pass

    def test_bad_data_throws(self):
        bad_data = (
            "some bad data is "
            "EHRlc3RAYW5jaG9yLnRlc3QwTDANBgkqhkiG9w0BAQEFAAM7ADA4AjEA6m")

        cert = certificate.X509Certificate()
        self.assertRaises(x509_errors.X509Error,
                          cert.from_buffer,
                          bad_data)

    def test_get_subject_countryName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_countryName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "countryName")
        self.assertEqual(entries[0].get_value(), "UK")

    def test_get_subject_stateOrProvinceName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_stateOrProvinceName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "stateOrProvinceName")
        self.assertEqual(entries[0].get_value(), "Narnia")

    def test_get_subject_localityName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_localityName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "localityName")
        self.assertEqual(entries[0].get_value(), "Funkytown")

    def test_get_subject_organizationName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_organizationName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "organizationName")
        self.assertEqual(entries[0].get_value(), "Anchor Testing")

    def test_get_subject_organizationUnitName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_organizationalUnitName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "organizationalUnitName")
        self.assertEqual(entries[0].get_value(), "testing")

    def test_get_subject_commonName(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_commonName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "commonName")
        self.assertEqual(entries[0].get_value(), "anchor.test")

    def test_get_subject_emailAddress(self):
        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_pkcs9_emailAddress)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "emailAddress")
        self.assertEqual(entries[0].get_value(), "test@anchor.test")

    def test_get_issuer_countryName(self):
        name = self.cert.get_issuer()
        entries = name.get_entries_by_nid(x509_name.NID_countryName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "countryName")
        self.assertEqual(entries[0].get_value(), "AU")

    def test_get_issuer_stateOrProvinceName(self):
        name = self.cert.get_issuer()
        entries = name.get_entries_by_nid(x509_name.NID_stateOrProvinceName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "stateOrProvinceName")
        self.assertEqual(entries[0].get_value(), "Some-State")

    def test_get_issuer_organizationName(self):
        name = self.cert.get_issuer()
        entries = name.get_entries_by_nid(x509_name.NID_organizationName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "organizationName")
        self.assertEqual(entries[0].get_value(), "Herp Derp plc")

    def test_get_issuer_commonName(self):
        name = self.cert.get_issuer()
        entries = name.get_entries_by_nid(x509_name.NID_commonName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "commonName")
        self.assertEqual(entries[0].get_value(), "herp.derp.plc")

    def test_set_subject(self):
        name = x509_name.X509Name()
        name.add_name_entry(x509_name.NID_countryName, 'UK')
        self.cert.set_subject(name)

        name = self.cert.get_subject()
        entries = name.get_entries_by_nid(x509_name.NID_countryName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "countryName")
        self.assertEqual(entries[0].get_value(), "UK")

    def test_set_issuer(self):
        name = x509_name.X509Name()
        name.add_name_entry(x509_name.NID_countryName, 'UK')
        self.cert.set_issuer(name)

        name = self.cert.get_issuer()
        entries = name.get_entries_by_nid(x509_name.NID_countryName)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].get_name(), "countryName")
        self.assertEqual(entries[0].get_value(), "UK")

    def test_read_from_file(self):
        open_name = 'anchor.X509.certificate.open'
        with mock.patch(open_name, create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file_class)
            m_file = mock_open.return_value.__enter__.return_value
            m_file.read.return_value = TestX509Cert.cert_data

            cert = certificate.X509Certificate()
            cert.from_file("some_path")
            name = cert.get_subject()
            entries = name.get_entries_by_nid(x509_name.NID_countryName)
            self.assertEqual(entries[0].get_value(), "UK")

    def test_get_fingerprint(self):
        fp = self.cert.get_fingerprint()
        self.assertEqual(fp, "56D61AC583BDDD4B44EEB479EF6C998F")

    def test_sign_bad_md(self):
        self.assertRaises(x509_errors.X509Error,
                          self.cert.sign,
                          None, "BAD")

    def test_sign_bad_key(self):
        self.assertRaises(x509_errors.X509Error,
                          self.cert.sign,
                          self.cert._ffi.NULL)

    def test_get_version(self):
        v = self.cert.get_version()
        self.assertEqual(v, 2)

    def test_set_version(self):
        self.cert.set_version(5)
        v = self.cert.get_version()
        self.assertEqual(v, 5)

    def test_get_not_before(self):
        val = self.cert.get_not_before()
        self.assertEqual(1421244619.0, val)

    def test_set_not_before(self):
        self.cert.set_not_before(0)  # seconds since epoch
        val = self.cert.get_not_before()
        self.assertEqual(0, val)

    def test_get_not_after(self):
        val = self.cert.get_not_after()
        self.assertEqual(1421331019.0, val)

    def test_set_not_after(self):
        self.cert.set_not_after(0)  # seconds since epoch
        val = self.cert.get_not_after()
        self.assertEqual(0, val)
