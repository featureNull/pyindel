import pyindel
import os

curdir = os.path.dirname(os.path.abspath(__file__))
fn = os.path.join(curdir, './pyindel/realcase.xlog')
doc = pyindel.load_xlog(fn)

x_cmds =  doc.group("X").channel("cmdS")
y_cmds =  doc.group("Y").channel("cmdS")
z_cmds =  doc.group("Z").channel("cmdS")

print(z_cmds)

