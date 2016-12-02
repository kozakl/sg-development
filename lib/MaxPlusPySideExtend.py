import xml.etree.ElementTree as exml
from io import BytesIO
from PySide.QtCore import *
from PySide.QtGui import *
import pysideuic

def LoadUiType(uiFile):
    # LoadUiType only accept ascii encoding chars
    uiFile = str(uiFile)
    parsed = exml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    ui_class_name = parsed.find('class').text
    with open(uiFile, 'r') as f:
        o = BytesIO()
        frame = {}
        pysideuic.compileUi(f, o)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        ui_class = frame['Ui_%s' % ui_class_name]
        base_class = eval(widget_class)
    return ui_class, base_class
