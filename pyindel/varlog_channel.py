import numpy as np
from lxml import etree


class VarlogChannel:
    def __init__(self, name: str, data: np.ndarray):
        self._name = name
        self.color = None
        self.unit = None
        self.data = data

    @property
    def name(self) -> str:
        return self._name

    @property
    def dtype(self):
        return self.data.dtype

    def _add_to_xml_header(self, parent):
        node = etree.SubElement(parent, "channel")
        node.set("name", str(self.name))

        if self.dtype == int:
            node.set("type", "0x0104")
            node.set("characteristics", "0x8")
        elif self.dtype == float:
            node.set("type", "0x0109")
            node.set("characteristics", "0x4C")
        else:
            raise ValueError(f"unsuported valuetype {self.dtype}")

        if self.unit is not None:
            node.set("unit", str(self.unit))

        if self.color is not None:
            node.set("color", str(self.color))
