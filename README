```python

from restan import tags as T, js, flatten

tree = T.p(
    onclick=js.document.write(T.div(onclick=js.alert('"'))["plop"])
)["lol"]

flatten(tree)
```

>>>'<p onclick="document.write(\'&lt;div onclick=&quot;alert(\\\'&amp;quot;\\\')&quot;&gt;plop&lt;/div&gt;\')">lol</p>'
