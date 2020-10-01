from lxml import etree

from pyindel.varlog_group import VarlogGroup

class VarlogDoc:
    def __init__(self):
        self.sample_rate = '10ms'
        self.groups = []

    def add_group(self, name: str):
        for g in self.groups:
            if g.name == name:
                raise RuntimeError(f'{name} wurde schon vergeben')
        g = VarlogGroup(name)
        self.groups.append(g)
        return g

    def group(self, name: str) -> VarlogGroup:
        for g in self.groups:
            if g.name:
                return g
        raise RuntimeError(f'group {name} not found')

    @property
    def channels(self):
        res = []
        for gr in self.groups:
            [res.append(ch) for ch in gr.channels]
        return res

    @property
    def rows(self) -> int:
        if len(self.channels) == 0:
            return 0
        else:
            return len(self.channels[0].data)

    def save(self, fname):
        xmlspec = '<?xml version="1.0" encoding="utf-8"?>\n'
        xmlheader = self._build_xml_header()
        header_bytes = etree.tostring(xmlheader, pretty_print=True)
        cvsbody = self._build_csv_body()

        if isinstance(fname, str):
            with open(fname, "wt") as f:
                f.write(xmlspec)
                f.write(header_bytes.decode("utf-8"))
                f.write(cvsbody)
        else:
            # from numpy, nimmt auch file handles oder sowas
            f.write(header_bytes.decode("utf-8"))
            f.write(cvsbody)

    def _build_xml_header(self) -> etree.Element:
        root = etree.Element("indelvarlog")
        root.set("target", "default")
        root.set("task", "LocalBus")
        root.set("count", str(self.rows))
        root.set("samplingtime", str(self.sample_rate))
        root.set("timebaseenabled", "false")

        for group in self.groups:
            group._add_to_xml_header(root)
        return root

    def _build_csv_body(self):
        doctext = []
        for ir in range(self.rows):
            linetext = [str(c.data[ir]) for c in self.channels]
            doctext.append("\t".join(linetext))
        return "\n".join(doctext)
