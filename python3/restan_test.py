import unittest
from restan import tags as T, js, flatten

class FlattenTestCase1(unittest.TestCase):
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

class FlattenTestCase14(unittest.TestCase):
    def runTest(self):
        p = T.p["A string; ",
                5, " (An integer) ",
                1.0, " (A float) ",
                True, " (A bool) ",
                ["A ", "List; "],
               ]
        self.assertEqual(flatten(p), "<p>A string; 5 (An integer) 1.0 (A float) 1 (A bool) A List; </p>")

class FlattenTestCase15(unittest.TestCase):
    def runTest(self):
        p = T.p(foo="<>&\"'")["<>&\"'"]
        self.assertEqual(flatten(p), '<p foo="&lt;&gt;&amp;&quot;\'">&lt;&gt;&amp;"\'</p>')

class FlattenTestCase16(unittest.TestCase):
    def runTest(self):
        self.assertEqual(
          flatten(T.p(onclick=js.document.write(T.div(onclick=js.alert('"'))["plop"]))["lol"]),
          '<p onclick="document.write(\'&lt;div onclick=&quot;alert(\\\'&amp;quot;\\\')&quot;&gt;plop&lt;/div&gt;\')">lol</p>'
        )
# TODO
#class FlattenTestCase17(unittest.TestCase):
#    def runTest(self):
#        self.assertRaises(
#            T.p["one"]["two"],
#            Exception
#        )

#class FlattenTestCase18(unittest.TestCase):
#    def runTest(self):
#        p = T.p
#        print flatten(p[p])
#        self.assertRaises(
#            p[p],
#            Exception
#        )

if __name__ == "__main__":
    unittest.main()

