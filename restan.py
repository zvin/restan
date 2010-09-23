from types import InstanceType
from itertools import imap
from cgi import escape

__flattener_registry = dict()

def register_flattener(_class, flattener):
    if _class == InstanceType:
        raise TypeError, "Flatteners are not allowed for old style classes"
    __flattener_registry[_class] = flattener

def flatten(element):
    flattener = __flattener_registry[type(element)]
    return flattener(element)

class Tags(object):
    self_closing = ("area", "base", "basefont", "br", "col", "frame", "hr",
                    "input", "img", "link", "meta", "param"
                   )
    def __getattribute__(self, name):
        self_closing = name in object.__getattribute__(self, "self_closing")
        return Tag(name, self_closing = self_closing)

tags = Tags()

class Tag(object):
    def __init__(self, name, self_closing=False):
        self.name = name
        self.self_closing = self_closing
        self.childs = ()
        self.attributes = {}
    def __getitem__(self, args):
        if self.self_closing:
            msg = "Tag %s is self closing and can't have childs" % self.name
            raise TypeError, msg
        if type(args) != tuple:
            args = (args,)
        self.childs = args
        return self
    def __call__(self, **kwargs):
        self.attributes = kwargs
        return self

def flatten_tag(tag):
    def flatten_attribute(name, value):
        if name.startswith("_"):
            name = name[1:]
        value = flatten(value)
        return '%s="%s"' % (name, value.replace('"', '&quot;'))
    attributes = " ".join(imap(lambda c: flatten_attribute(*c),
                               tag.attributes.iteritems()
                              )
                         )
    if attributes: attributes = " " + attributes
    if tag.self_closing:
        return "<%s%s/>" % (tag.name, attributes)
    else:
        def flatten_child(child):
            if type(child) in (str, unicode):
                # escape htmlchars only in strings
                return escape(child)
            else:
                return flatten(child)
        childs_flat = "".join(imap(flatten_child, tag.childs))
        return "<%s%s>%s</%s>" % (tag.name, attributes, childs_flat, tag.name)

register_flattener(Tag, flatten_tag)
register_flattener(int, str)
register_flattener(float, str)

class JsAttribute(object):
    def __init__(self, name):
        self.name = name

def flatten_jsattribute(attribute):
    return ".%s" % (attribute.name)

register_flattener(JsAttribute, flatten_jsattribute)

class JsCall(object):
    def __init__(self, *params):
        self.params = params

def __flatten_and_escape(param):
    """Used to escape JsCall and JsIndex parameters, do not use anywhere else"""
    result = flatten(param)
    if type(param) not in (JsNode, int, float):
        result = "'%s'" % (result.replace("\\", "\\\\").replace("'", "\\'"))
    return result

def flatten_jscall(call):
    return "(%s)" % ( ", ".join(imap(__flatten_and_escape, call.params)) )

register_flattener(JsCall, flatten_jscall)

class JsIndex(object):
    def __init__(self, key):
        self.key = key

def flatten_jsindex(index):
    return "[%s]" % __flatten_and_escape(index.key)

register_flattener(JsIndex, flatten_jsindex)

class JsNode(object):
    def __init__(self, name):
        self.name = name
        self.childs = []
    def __call__(self, *args):
        object.__getattribute__(self, "childs").append( JsCall(*args) )
        return self
    def __getattribute__(self, name):
        object.__getattribute__(self, "childs").append( JsAttribute(name) )
        return self
    def __getitem__(self, key):
        object.__getattribute__(self, "childs").append( JsIndex(key) )
        return self

def flatten_jsnode(node):
    name = object.__getattribute__(node, "name")
    childs = object.__getattribute__(node, "childs")
    return name + "".join(imap(flatten, childs))

class Js(object):
    def __getattribute__(self, name):
        return JsNode(name)

register_flattener(JsNode, flatten_jsnode)
register_flattener(str, str)
register_flattener(unicode, unicode)

js = Js()

__all__ = ["tags", "js", "flatten"]

