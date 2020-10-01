import numpy as np
from lxml import etree
from pyindel.varlog_channel import VarlogChannel


class VarlogGroup:
    def __init__(self, name: str):
        self._name = name
        self.channels = []

    @property
    def name(self) -> str:
        return self._name

    def add_channel(self, name: str, data: np.ndarray, color=None, unit=None):
        for c in self.channels:
            if c.name == name:
                raise RuntimeError(f'{name} wurde schon vergeben')
        c = VarlogChannel(name, data)
        self.channels.append(c)
        c.color = color
        c.unit = unit
        return c

    def channel(self, name: str) -> VarlogChannel:
        for c in self.channels:
            if c.name == name:
                return c
        raise RuntimeError(f'channel {name} not found')

    def _add_to_xml_header(self, parent):
        node = etree.SubElement(parent, "group")
        node.set("name", str(self.name))
        for ch in self.channels:
            ch._add_to_xml_header(node)
