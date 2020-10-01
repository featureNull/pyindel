from pyindel.varlog_group import VarlogGroup
from pyindel.varlog_channel import VarlogChannel
from pyindel.varlog_doc import VarlogDoc

import numpy as np
import pytest
import time


def test_varlogchannel():
    c = VarlogChannel('channeltext', np.ones((1, 2)))
    assert c.dtype == float
    assert c.name == 'channeltext'
    c.unit = 'mm'
    assert c.unit == 'mm'


def test_varloggroup():
    g = VarlogGroup('grouptext')
    assert g.name == 'grouptext'
    g.add_channel('channeltext', np.ones((1, 2)))
    assert len(g.channels) == 1
    assert g.channel('channeltext').name == 'channeltext'

    with pytest.raises(RuntimeError):
        g.channel('fvbsdfvn')

    with pytest.raises(RuntimeError):
        g.add_channel('channeltext', np.ones((1, 2)))


def test_varlogdoc():
    doc = VarlogDoc()
    assert len(doc.channels) == 0
    assert doc.rows == 0

    doc.add_group('xxx')
    assert doc.group('xxx') != None
    assert len(doc.groups) == 1
    with pytest.raises(RuntimeError):
        doc.add_group('xxx')

def test_simple_case():
    x = np.linspace(-np.pi, np.pi, 1000)
    
    doc = VarlogDoc()
    group1 = doc.add_group("group1")
    group1.add_channel("sin", np.sin(x))
    group1.add_channel("cos", np.cos(x), unit='mm', color='#202020')
    assert group1.channel('cos').unit == 'mm'
    assert len(doc.channels) == 2
    assert doc.rows == 1000

    doc.save("lalelu.xlog")

def test_real_case():
    doc = VarlogDoc()
    x = np.linspace(-np.pi, np.pi, 1000)
    group1 = doc.add_group("group1")
    group1.add_channel("sin", np.sin(x))
    group1.add_channel("cos", np.cos(x))
    
    group2 = doc.add_group("group2")
    group2.add_channel("rampe", np.arange(1000))

    assert len(doc.channels) == 3
    assert doc.rows == 1000

    doc.save("lalelu2.xlog")

def test_count_mismatch():
    doc = VarlogDoc()
    g = doc.add_group("g1")
    g.add_channel("c1", np.arange(2000), unit="suppe")
    g.add_channel("c2", np.arange(1000), unit="suppe")

    with pytest.raises(IndexError):
        doc.save("lalelu2.xlog")