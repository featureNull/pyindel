import pyindel
import os
import matplotlib.pyplot as plt

curdir = os.path.dirname(os.path.abspath(__file__))

fn = os.path.join(curdir, './pyindel/realcase.xlog')
doc = pyindel.load_xlog(fn)
x_cmds = doc.group("X").channel("cmdS").data
y_cmds = doc.group("Y").channel("cmdS").data
z_cmds = doc.group("Z").channel("cmdS").data

# strip curve
begin = 2000
end = 5000
x_cmds = x_cmds[begin:end]
y_cmds = y_cmds[begin:end]
z_cmds = z_cmds[begin:end]

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot3D(x_cmds, y_cmds, z_cmds, 'gray')
plt.show()
