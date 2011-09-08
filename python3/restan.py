from escape import escape

__flattener_registry = dict()

def register_flattener(_class, flattener):
    __flattener_registry[_class] = flattener

def flatten(element):
    try:
        flattener = __flattener_registry[type(element)]
    except KeyError:
        raise KeyError("No flattener registered for %s" % type(element))
    return flattener(element)

class Tags(object):
    self_closing = ("area", "base", "basefont", "br", "col", "frame", "hr",
                    "input", "img", "link", "meta", "param"
                   )
    def __getattribute__(self, name):
        if name in object.__getattribute__(self, "self_closing"):
            return SelfClosingTag(name)
        else:
            return Tag(name)

tags = Tags()

class Tag(object):
    def __init__(self, name):
        self.name = name
        self.childs = ()
        self.attributes = ()
    def __getitem__(self, args):
        if type(args) != tuple:
            args = (args,)
        self.childs = args
        return self
    def __call__(self, **kwargs):
        self.attributes = map(lambda kv: TagAttribute(*kv), kwargs.items())
        return self

def flatten_tag(tag):
    attributes = " ".join(map(flatten, tag.attributes))
    if attributes: attributes = " " + attributes
    def flatten_child(child):
        if type(child) == str:
            # escape htmlchars only in strings
            return escape(child, quote=False)
        else:
            return flatten(child)
    childs_flat = "".join(map(flatten_child, tag.childs))
    return "<%s%s>%s</%s>" % (tag.name, attributes, childs_flat, tag.name)

register_flattener(Tag, flatten_tag)

class SelfClosingTag(Tag):
    def __getitem__(self, args):
        msg = "Tag %s is self closing and can't have childs" % self.name
        raise TypeError(msg)

def flatten_selfclosingtag(tag):
    attributes = " ".join(map(flatten, tag.attributes))
    if attributes: attributes = " " + attributes
    return "<%s%s/>" % (tag.name, attributes)

register_flattener(SelfClosingTag, flatten_selfclosingtag)

class TagAttribute(object):
    def __init__(self, name, value):
        if name.startswith("_"):
            name = name[1:]
        self.name = name
        self.value = value

def flatten_tagattribute(attribute):
    value = flatten(attribute.value)
    return '%s="%s"' % (attribute.name, escape(value, quote=True))

register_flattener(TagAttribute, flatten_tagattribute)

register_flattener(int, str)
register_flattener(float, str)
register_flattener(bool, lambda b: "1" if b else "0")

def flatten_list(l):
    return "".join(map(flatten, l))

register_flattener(list, flatten_list)

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
    return "(%s)" % ( ", ".join(map(__flatten_and_escape, call.params)) )

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
    return name + "".join(map(flatten, childs))

class Js(object):
    def __getattribute__(self, name):
        return JsNode(name)

register_flattener(JsNode, flatten_jsnode)
register_flattener(str, str)

js = Js()

__all__ = ["tags", "js", "flatten"]

