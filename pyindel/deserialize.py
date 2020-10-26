from pyindel.varlog_doc import VarlogDoc
from lxml import etree
import numpy as np


def load_xlog(fname: str):
    """Load xlog file
    Args:
        fname (str): .xlog file name
    Returns:
        VarlogDoc: varlog doc, which contains data from file
    """
    xml_header = ''
    csv_body = ''

    with open(fname, 'r') as f:
        endxml_tag = '</indelvarlog>'
        data = f.read()
        taginx = data.find(endxml_tag)
        xml_header = data[0: taginx + len(endxml_tag)]
        csv_body = data.split(endxml_tag)[1]
        csv_body = csv_body.strip().split('\n')

    root = etree.fromstring(xml_header.encode('utf-8'))
    doc = VarlogDoc()
    doc.sample_rate = root.get('samplingtime')
    count = int(root.get('count'))

    #
    # read xml header
    #
    for gtag in root.findall('group'):
        group = doc.add_group(gtag.get('name'))
        for chtag in gtag.findall('channel'):
            dtype = int if (chtag.get('type') == '0x0104') else float
            data = np.zeros(count, dtype=dtype)
            group.add_channel(chtag.get('name'), data,
                 color=chtag.get('color'), unit=chtag.get('unit'))

    #
    # read csv data
    #
    chs = doc.channels
    for inx, line in enumerate(csv_body):
        values = line.split('\t')
        assert len(values) == len(chs)
        # die schleife kann man pythonic machen
        for ch, val in zip(chs, values):
            ch.data[inx] = int(val) if ch.data.dtype == int else float(val)

    return doc
