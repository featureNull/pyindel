from pyindel.varlog_group import VarlogGroup
from pyindel.varlog_channel import VarlogChannel
from pyindel.varlog_doc import VarlogDoc
from pyindel.deserialize import load_xlog

import numpy as np
import pytest
import os


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
        g.channel('unknown_channnel')

    with pytest.raises(RuntimeError):
        g.add_channel('channeltext', np.ones((1, 2)))


def test_varlogdoc():
    doc = VarlogDoc()
    assert len(doc.channels) == 0
    assert doc.rows == 0

    doc.add_group('xxx')
    assert doc.group('xxx') is not None
    assert len(doc.groups) == 1
    with pytest.raises(RuntimeError):
        doc.add_group('xxx')


def test_count_mismatch():
    doc = VarlogDoc()
    g = doc.add_group("g1")
    g.add_channel("c1", np.arange(2000))
    g.add_channel("c2", np.arange(1000))

    with pytest.raises(IndexError):
        doc.save("count_mismatch.xlog")


def test_save_simple_case():
    x = np.linspace(-np.pi, np.pi, 1000)

    doc = VarlogDoc()
    group1 = doc.add_group("group1")
    group1.add_channel("sin", np.sin(x))
    group1.add_channel("cos", np.cos(x), unit='mm', color='#202020')
    assert group1.channel('cos').unit == 'mm'
    assert len(doc.channels) == 2
    assert doc.rows == 1000

    doc.save("simple_case.xlog")


def test_save_real_case():
    doc = VarlogDoc()
    x = np.linspace(-np.pi, np.pi, 1000)
    group1 = doc.add_group("group1")
    group1.add_channel("sin", np.sin(x))
    group1.add_channel("cos", np.cos(x))

    group2 = doc.add_group("group2")
    group2.add_channel("rampe", np.arange(1000))

    assert len(doc.channels) == 3
    assert doc.rows == 1000

    doc.save("real_case.xlog")


def test_load_minimal():
    curdir = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(curdir, 'minimal.xlog')
    doc = load_xlog(fn)

    sin_ch = doc.group('group1').channel('sin')
    assert 0.0 == pytest.approx(sin_ch.data[0], 0.001)
    assert 1000 == sin_ch.data.size


def test_load_realcase_layout():
    curdir = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(curdir, 'realcase.xlog')
    doc = load_xlog(fn)
    # ergibt sich aus den daten
    assert 5 == len(doc.groups)
    assert 41 == len(doc.channels)


def test_load_realcase_unnamed_group():
    curdir = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(curdir, 'realcase.xlog')
    doc = load_xlog(fn)

    # check very first value of channel at beginning
    tbase = doc.group('').channel('Timebase')
    assert 106689471250 == tbase.data[0]
    
    # check very last value of a channel at the end (stichprobe)
    z_acti = doc.group('Z').channel('actI')
    assert -0.158721923828125 == pytest.approx(z_acti.data[-1], 0.001)
