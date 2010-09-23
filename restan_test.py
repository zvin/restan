import unittest
from restan import tags as T, js, flatten

class FlattenTagTestCase1(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div["foo bar"]),
          '<div>foo bar</div>'
        )

class FlattenTestCase2(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div["plop", T.span(style="border: 1px solid red;")["plip"]]),
          '<div>plop<span style="border: 1px solid red;">plip</span></div>'
        )

class FlattenTestCase3(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div["plop", T.br, T.span["plip"]]),
          '<div>plop<br/><span>plip</span></div>'
        )

class FlattenTestCase4(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(_id="lol")["plop", T.br, T.span["plip"]]),
          '<div id="lol">plop<br/><span>plip</span></div>'
        )

class FlattenTestCase5(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(onclick=js.alert("l'apostrophe"))["plop", T.br]),
          "<div onclick=\"alert('l\\'apostrophe')\">plop<br/></div>"
        )

class FlattenTestCase6(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(onclick=js.alert('"'))["plop"]),
          """<div onclick="alert('&quot;')">plop</div>"""
        )

class FlattenTestCase7(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(onclick=js.document.write("l'apostrophe"))["plop"]),
          "<div onclick=\"document.write('l\\'apostrophe')\">plop</div>"
        )

class FlattenTestCase8(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(onclick=js.foo["bar"]("baz").write("l'apostrophe"))["plop", T.br]),
          "<div onclick=\"foo['bar']('baz').write('l\\'apostrophe')\">plop<br/></div>"
        )

class FlattenTestCase9(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.div(onclick=js.foo[js.document.getElementById("plop")].write("l'apostrophe"))["plop"]),
          """<div onclick="foo[document.getElementById('plop')].write('l\\'apostrophe')\">plop</div>"""
        )

class FlattenTestCase10(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(js.document.write( T.p(onclick=js.alert("l'apostrophe"))["plop"] )),
          """document.write('<p onclick="alert(\\'l\\\\\\'apostrophe\\')">plop</p>')"""
        )

class FlattenTestCase11(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(js.document.write( T.p(onclick=js.document.write('''"l'apostrophe"'''))["plop"] )),
          """document.write('<p onclick="document.write(\\'&quot;l\\\\\\'apostrophe&quot;\\')">plop</p>')"""
        )

class FlattenTestCase12(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(js.foo.bar(1, 2.42, js.list["three"])),
          "foo.bar(1, 2.42, list['three'])"
        )

class FlattenTestCase13(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.p["-->foo<--"]),
          "<p>--&gt;foo&lt;--</p>"
        )

if __name__ == "__main__":
    unittest.main()

