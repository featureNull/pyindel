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

## load varlog data into python

```python
import pyindel
import matplotlib.pyplot as plt

doc = pyindel.load_xlog('myfile.xlog')
x_cmds = doc.group("X").channel("cmdS").data
y_cmds = doc.group("Y").channel("cmdS").data
z_cmds = doc.group("Z").channel("cmdS").data

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(x_cmds, y_cmds, z_cmds, 'gray')
plt.show()
```
