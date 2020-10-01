# Python binding for Indel Motion

## generate varlog data from python

```python
import pyindel
import numpy as np

x = np.linspace(-np.pi, np.pi, 1000)

doc = pyindel.VarlogDoc()
group1 = doc.add_group("group1")
group1.add_channel("sin", np.sin(x))
group1.add_channel("cos", np.cos(x), unit='mm', color='#202020')
doc.save("lalelu.xlog")
```


