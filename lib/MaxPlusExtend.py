import MaxPlus

# The following classes expose the notification system to Python in a safe way.
class _NotificationHandler(MaxPlus.AbstractNotificationHandler):
    ''' Wraps a callback function as a notification handler '''
    def __init__(self, notifyCallback):
        MaxPlus.AbstractNotificationHandler.__init__(self)
        self.callback = notifyCallback
    def OnNotify(self, notifyCode):
        self.callback(notifyCode)

class NotificationManager(object):
    ''' Allows callback functions to be registered with notifications. '''
    Handlers = [] # This assures that Python garbage collection does not delete our handlers.

    @staticmethod
    def Register(notifyCode, notifyCallback):
       ''' Registers a callback function with the particular notification code.
           The returned handler object will not be collected, until it is unregistered. '''
       handler = _NotificationHandler(notifyCallback)
       NotificationManager.Handlers.append(handler)
       MaxPlus._INTERNAL_NotificationManager.AddHandler(notifyCode, handler)
       return handler

    @staticmethod
    def Unregister(handler):
       ''' Unregisters a handler. '''
       MaxPlus._INTERNAL_NotificationManager.RemoveHandler(handler)
       NotificationManager.Handlers.remove(handler)


class _CustomActionItem(MaxPlus.AbstractCustomActionItem):
    ''' Wraps a custom user action. '''
    def __init__(self, category, name, fxn):
        try:
            MaxPlus.AbstractCustomActionItem.__init__(self)
            self.category = category
            self.name = name
            self.fxn = fxn
            self.id = hash('Python_' + category + '_' + name + '_' + str(id(fxn)))
        except:
            print 'Error occured creating custom user action'
    def GetMenuText(self):
        return self.name
    def GetId(self):
        return self.id
    def GetCategoryText(self):
        return self.category
    def Execute(self):
        try:
            self.fxn()
        except:
            print 'Error occured executing user action'

class ActionFactory(object):
    ''' Creates basic action items.  '''
    ActionItems = [] # This assures that Python garbage collection does not delete our action items
    CustomActionItems = []  # This assures that Python garbage collection does not delete our action
                            # items

    @staticmethod
    def CreateFromAbstract(item):
        ''' Creates a new action item from an AbstractCustomActionItem '''
        try:
            r = MaxPlus._INTERNAL_CustomActionCallback.AddAction(item)
            ActionFactory.ActionItems.append(r)
            return r
        except:
            print 'An error occurred creating an abstract action item'

    @staticmethod
    def Create(category, name, fxn):
        ''' Creates a new action item from the category, name and function. '''
        try:
            item = _CustomActionItem(category, name, fxn)
            ActionFactory.CustomActionItems.append(item)
            return ActionFactory.CreateFromAbstract(item)
        except:
            print 'An error occurred creating an action item'

# \TODO: Add handling of Point, FPValue, and Value.
_FPValueGetters = {
    MaxPlus.FPTypeConstants.Float : MaxPlus.FPValue.GetFloat,
    MaxPlus.FPTypeConstants.Int : MaxPlus.FPValue.GetInt,
    MaxPlus.FPTypeConstants.Rgb : MaxPlus.FPValue.GetColor,
    MaxPlus.FPTypeConstants.Point3 : MaxPlus.FPValue.GetPoint3,
    MaxPlus.FPTypeConstants.BOOL : MaxPlus.FPValue.GetBool,
    MaxPlus.FPTypeConstants.Angle : MaxPlus.FPValue.GetFloat,
    MaxPlus.FPTypeConstants.PercentFraction : MaxPlus.FPValue.GetFloat,
    MaxPlus.FPTypeConstants.World : MaxPlus.FPValue.GetFloat,
    MaxPlus.FPTypeConstants.String : MaxPlus.FPValue.GetPChar,
    MaxPlus.FPTypeConstants.FileName : MaxPlus.FPValue.GetPChar,
    MaxPlus.FPTypeConstants.Hsv : MaxPlus.FPValue.GetPoint3,
    MaxPlus.FPTypeConstants.ColorChannel : MaxPlus.FPValue.GetFloat,
    MaxPlus.FPTypeConstants.TimeValue : MaxPlus.FPValue.GetInt,
    MaxPlus.FPTypeConstants.RadioButtonIndex : MaxPlus.FPValue.GetInt,
    MaxPlus.FPTypeConstants.Mtl : MaxPlus.FPValue.GetMtl,
    MaxPlus.FPTypeConstants.Texmap : MaxPlus.FPValue.GetTexmap,
    MaxPlus.FPTypeConstants.Bitmap : MaxPlus.FPValue.GetBitmap,
    MaxPlus.FPTypeConstants.Node : MaxPlus.FPValue.GetNode,
    MaxPlus.FPTypeConstants.RefTarg : MaxPlus.FPValue.GetReferenceTarget,
    MaxPlus.FPTypeConstants.Index : MaxPlus.FPValue.GetInt,
    MaxPlus.FPTypeConstants.Matrix3 : MaxPlus.FPValue.GetMatrix3,
    MaxPlus.FPTypeConstants.PBlock2 : MaxPlus.FPValue.GetReferenceTarget,
    MaxPlus.FPTypeConstants.Point4 : MaxPlus.FPValue.GetPoint4,
    MaxPlus.FPTypeConstants.FRgb : MaxPlus.FPValue.GetAColor,
    MaxPlus.FPTypeConstants.Enum : MaxPlus.FPValue.GetInt,
    # MaxPlus.FPTypeConstants.Void : MaxPlus.FPValue.GetVoid,
    MaxPlus.FPTypeConstants.Interval : MaxPlus.FPValue.GetInterval,
    MaxPlus.FPTypeConstants.AngAxis : MaxPlus.FPValue.GetAngAxis,
    MaxPlus.FPTypeConstants.Quat : MaxPlus.FPValue.GetQuat,
    MaxPlus.FPTypeConstants.Ray : MaxPlus.FPValue.GetRay,
    MaxPlus.FPTypeConstants.Point2 : MaxPlus.FPValue.GetPoint2,
    MaxPlus.FPTypeConstants.BitArray : MaxPlus.FPValue.GetBitArray,
    MaxPlus.FPTypeConstants.ClassDesc : MaxPlus.FPValue.GetClassDesc,
    MaxPlus.FPTypeConstants.Mesh : MaxPlus.FPValue.GetMesh,
    MaxPlus.FPTypeConstants.Object : MaxPlus.FPValue.GetObject,
    MaxPlus.FPTypeConstants.Control : MaxPlus.FPValue.GetControl,
    MaxPlus.FPTypeConstants.Point : MaxPlus.FPValue.GetIPoint2,
    MaxPlus.FPTypeConstants.Str : MaxPlus.FPValue.GetStr,
    MaxPlus.FPTypeConstants.IObject : MaxPlus.FPValue.GetIObject,
    MaxPlus.FPTypeConstants.FPInterface : MaxPlus.FPValue.GetFPInterface,
    MaxPlus.FPTypeConstants.HWND : MaxPlus.FPValue.GetInt64,
    MaxPlus.FPTypeConstants.Name : MaxPlus.FPValue.GetPChar,
    MaxPlus.FPTypeConstants.Color : MaxPlus.FPValue.GetColor,
    # MaxPlus.FPTypeConstants.FPValue : MaxPlus.FPValue.GetFPValue,
    # MaxPlus.FPTypeConstants.Value : MaxPlus.FPValue.GetValue,
    MaxPlus.FPTypeConstants.DWORD : MaxPlus.FPValue.GetDWORD,
    MaxPlus.FPTypeConstants.Bool : MaxPlus.FPValue.GetBool,
    MaxPlus.FPTypeConstants.IntPtr : MaxPlus.FPValue.GetInt64,
    MaxPlus.FPTypeConstants.Int64 : MaxPlus.FPValue.GetInt64,
    MaxPlus.FPTypeConstants.Double : MaxPlus.FPValue.GetDouble,
    MaxPlus.FPTypeConstants.MSFloat : MaxPlus.FPValue.GetFloat,

    MaxPlus.FPTypeConstants.FloatTab : MaxPlus.FPValue.GetFloatList,
    MaxPlus.FPTypeConstants.IntTab : MaxPlus.FPValue.GetIntList,
    MaxPlus.FPTypeConstants.RgbTab : MaxPlus.FPValue.GetColorList,
    MaxPlus.FPTypeConstants.Point3Tab : MaxPlus.FPValue.GetPoint3List,
    MaxPlus.FPTypeConstants.BOOLTab : MaxPlus.FPValue.GetBoolList,
    MaxPlus.FPTypeConstants.AngleTab : MaxPlus.FPValue.GetFloatList,
    MaxPlus.FPTypeConstants.PercentFractionTab : MaxPlus.FPValue.GetFloatList,
    MaxPlus.FPTypeConstants.WorldTab : MaxPlus.FPValue.GetFloatList,
    MaxPlus.FPTypeConstants.StringTab : MaxPlus.FPValue.GetPCharList,
    MaxPlus.FPTypeConstants.FileNameTab : MaxPlus.FPValue.GetPCharList,
    MaxPlus.FPTypeConstants.HsvTab : MaxPlus.FPValue.GetPoint3List,
    MaxPlus.FPTypeConstants.ColorChannelTab : MaxPlus.FPValue.GetFloatList,
    MaxPlus.FPTypeConstants.TimeValueTab : MaxPlus.FPValue.GetIntList,
    MaxPlus.FPTypeConstants.RadioButtonIndexTab : MaxPlus.FPValue.GetIntList,
    MaxPlus.FPTypeConstants.MtlTab : MaxPlus.FPValue.GetMtlList,
    MaxPlus.FPTypeConstants.TexmapTab : MaxPlus.FPValue.GetTexmapList,
    MaxPlus.FPTypeConstants.BitmapTab : MaxPlus.FPValue.GetBitmapList,
    MaxPlus.FPTypeConstants.NodeTab : MaxPlus.FPValue.GetNodeList,
    MaxPlus.FPTypeConstants.RefTargTab : MaxPlus.FPValue.GetReferenceTargetList,
    MaxPlus.FPTypeConstants.IndexTab : MaxPlus.FPValue.GetIntList,
    MaxPlus.FPTypeConstants.Matrix3Tab : MaxPlus.FPValue.GetMatrix3List,
    MaxPlus.FPTypeConstants.PBlock2Tab : MaxPlus.FPValue.GetReferenceTargetList,
    MaxPlus.FPTypeConstants.Point4Tab : MaxPlus.FPValue.GetPoint4List,
    MaxPlus.FPTypeConstants.FRgbTab : MaxPlus.FPValue.GetAColorList,
    MaxPlus.FPTypeConstants.EnumTab : MaxPlus.FPValue.GetIntList,
    # MaxPlus.FPTypeConstants.VoidTab : MaxPlus.FPValue.GetVoidList,
    MaxPlus.FPTypeConstants.IntervalTab : MaxPlus.FPValue.GetIntervalList,
    MaxPlus.FPTypeConstants.AngAxisTab : MaxPlus.FPValue.GetAngAxisList,
    MaxPlus.FPTypeConstants.QuatTab : MaxPlus.FPValue.GetQuatList,
    MaxPlus.FPTypeConstants.RayTab : MaxPlus.FPValue.GetRayList,
    MaxPlus.FPTypeConstants.Point2Tab : MaxPlus.FPValue.GetPoint2List,
    MaxPlus.FPTypeConstants.BitArrayTab : MaxPlus.FPValue.GetBitArrayList,
    MaxPlus.FPTypeConstants.ClassDescTab : MaxPlus.FPValue.GetClassDescList,
    MaxPlus.FPTypeConstants.MeshTab : MaxPlus.FPValue.GetMeshList,
    MaxPlus.FPTypeConstants.ObjectTab : MaxPlus.FPValue.GetObjectList,
    MaxPlus.FPTypeConstants.ControlTab : MaxPlus.FPValue.GetControlList,
    MaxPlus.FPTypeConstants.PointTab : MaxPlus.FPValue.GetIPoint2List,
    MaxPlus.FPTypeConstants.StrTab : MaxPlus.FPValue.GetStrList,
    MaxPlus.FPTypeConstants.IObjectTab : MaxPlus.FPValue.GetIObjectList,
    MaxPlus.FPTypeConstants.FPInterfaceTab : MaxPlus.FPValue.GetFPInterfaceList,
    MaxPlus.FPTypeConstants.HWNDTab : MaxPlus.FPValue.GetInt64List,
    MaxPlus.FPTypeConstants.NameTab : MaxPlus.FPValue.GetPCharList,
    MaxPlus.FPTypeConstants.ColorTab : MaxPlus.FPValue.GetColorList,
    MaxPlus.FPTypeConstants.FPValueTab : MaxPlus.FPValue.GetFPValueList,
    # MaxPlus.FPTypeConstants.ValueTab : MaxPlus.FPValue.GetValueList,
    MaxPlus.FPTypeConstants.DWORDTab : MaxPlus.FPValue.GetDWORDList,
    MaxPlus.FPTypeConstants.BoolTab : MaxPlus.FPValue.GetBoolList,
    MaxPlus.FPTypeConstants.IntPtrTab : MaxPlus.FPValue.GetInt64List,
    MaxPlus.FPTypeConstants.Int64Tab : MaxPlus.FPValue.GetInt64List,
    MaxPlus.FPTypeConstants.DoubleTab : MaxPlus.FPValue.GetDoubleList,
}

FPTypeNames = {}
for k in dir(MaxPlus.FPTypeConstants):
    v = getattr(MaxPlus.FPTypeConstants, k)
    if type(v) == int:
        FPTypeNames[v] = k

def _FPType_GetNormalizedType(type_id):
    return type_id & ~MaxPlus.FPTypeConstants._ValueIsByValueOrReferenceOrPointer

def FPTypeGetName(type_id):
    ''' Returns the name associated with the FPValue type, 'unknown' if type not valid. '''
    type_id = _FPType_GetNormalizedType(type_id)
    return FPTypeNames.get(type_id, 'unknown')

def FPValue_Get(self):
    ''' Returns the value stored in FPValue of the correct type. '''
    type_id = _FPType_GetNormalizedType(self.Type)
    if not type_id in _FPValueGetters:
        raise RuntimeError('unable to find an appropriate get function for type {0}'.format(type_id))
    return _FPValueGetters[type_id](self, True)

# Add a new function to the FPValue class.
if not hasattr(MaxPlus.FPValue, "Get"):
    MaxPlus.FPValue.Get = FPValue_Get

# Create a new function for getting the value from a parameter as the actual
# type: not just an FPValue
def Parameter_GetValue_Typed(self):
    ''' Gets the value from a Parameter as the actual type, not as an FPValue '''
    fpv = self._GetValue()
    return fpv.Get()

# We are renaming the original 'GetValue' function on Parameter (which returns
# an FPValue) to '_GetValue'
# and replacing with a new typed version
if not hasattr(MaxPlus.Parameter, "_GetValue"):
    MaxPlus.Parameter._GetValue = MaxPlus.Parameter.GetValue
    MaxPlus.Parameter.GetValue = Parameter_GetValue_Typed

# Create a new function for setting the value of a parameter from the actual
# type: not just an FPValue
def Parameter_SetValue_Typed(self, x):
    ''' Sets the value from a Parameter as the actual type, not as an FPValue '''
    fpv = MaxPlus.FPValue()
    type = self.Type
    if type == MaxPlus.FPTypeConstants.MSFloat:
        type = MaxPlus.FPTypeConstants.Float
    if type == MaxPlus.FPTypeConstants.BOOL:
        type = MaxPlus.FPTypeConstants.Bool
    if type == MaxPlus.FPTypeConstants.BOOLTab:
        type = MaxPlus.FPTypeConstants.BoolTab
    fpv.Set(x, type, True)
    self._SetValue(fpv)

# Rename the original SetValue function to _SetValue and replacing with a new
# typed version
if not hasattr(MaxPlus.Parameter, "_SetValue"):
    MaxPlus.Parameter._SetValue = MaxPlus.Parameter.SetValue
    MaxPlus.Parameter.SetValue = Parameter_SetValue_Typed

# Make sure the property is updated
MaxPlus.Parameter.Value = MaxPlus._swig_property(MaxPlus.Parameter.GetValue, MaxPlus.Parameter.SetValue)

# Create a new function for getting the value from an ArrayParameter as the
# actual type: not just an FPValue
def ArrayParameter_GetValue_Typed(self):
    ''' Gets the value from an ArrayParameter as the actual type, not as an FPValue '''
    fpv = self._GetValue()
    return fpv.Get()

# We are renaming the original 'GetValue' function on ArrayParameter (which
# returns an FPValue) to '_GetValue' and replacing with a new typed version
if not hasattr(MaxPlus.ArrayParameter, "_GetValue"):
    MaxPlus.ArrayParameter._GetValue = MaxPlus.ArrayParameter.GetValue
    MaxPlus.ArrayParameter.GetValue = ArrayParameter_GetValue_Typed

# Create a new function for setting the value of an ArrayParameter from the
# actual type: not just an FPValue
def ArrayParameter_SetValue_Typed(self, x):
    ''' Sets the value from an ArrayParameter as the actual type, not as an FPValue '''
    fpv = MaxPlus.FPValue()
    type = self.Type
    fpv.Set(x, type)
    self._SetValue(fpv)

# Rename the original SetValue function to _SetValue and replacing with a new
# typed version
if not hasattr(MaxPlus.ArrayParameter, "_SetValue"):
    MaxPlus.ArrayParameter._SetValue = MaxPlus.ArrayParameter.SetValue
    MaxPlus.ArrayParameter.SetValue = ArrayParameter_SetValue_Typed

# Make sure the property is updated
MaxPlus.ArrayParameter.Value = MaxPlus._swig_property(MaxPlus.ArrayParameter.GetValue, MaxPlus.ArrayParameter.SetValue)

import ctypes
from PySide import QtGui

# Attach a given parentless QWidget by its Qt winId to the win32 3ds max main
# window.
def AttachQWidgetToMax(qWidget, isModelessDlg=True):
    ''' Attach a given parentless QWidget by its Qt winId to the win32 3ds max main window.
    This is internally done by creating an in-between QWinWidget, which will be child
    of the 3d max window, and a parenting of the QWidget to the QWinWidget.
    For the given QWidget the 3ds max keyboards accelerators will be disabled when
    the widget gets the focus.
    By setting isModelessDlg to true, 3ds max will properly disable/enable the QWidget
    when another modal 3ds max dialog pops up. '''

    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    intHwnd = ctypes.pythonapi.PyCObject_AsVoidPtr(qWidget.winId())
    MaxPlus.QtHelpers.AttachQWidgetToMax(intHwnd, isModelessDlg)

# Cached QMaxWindow
_gCachedQMaxWindow = None

def _PyCObjectToInt(obj):
    ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    return ctypes.pythonapi.PyCObject_AsVoidPtr(obj)

def GetQMaxWindow():
    '''Get the 3ds Max internal QWidget window that could be used for parenting your QWidget.'''

    if _gCachedQMaxWindow:
        return _gCachedQMaxWindow

    maxHwnd = MaxPlus.QtHelpers.GetQMaxWindowWinId()
    for w in QtGui.QApplication.allWidgets():
        if _PyCObjectToInt(w.effectiveWinId()) == maxHwnd:
            globals()['_gCachedQMaxWindow'] = w
            break
    return _gCachedQMaxWindow

def MakeQWidgetDockable(qwidget, flag=15):
    '''Make given QWidget dockable'''

    MaxPlus.QtHelpers.MakeQWidgetDockable(_PyCObjectToInt(qwidget.winId()), flag)

def CreateIntList(list_arg):
    res = MaxPlus.IntList()
    if not isinstance(list_arg, list):
        raise TypeError("argument is not list")
    res.SetCount(len(list_arg))
    resi = 0
    for e in list_arg:
        if isinstance(e, (int, long)):
            res[resi] = e
        else:
            raise ValueError("list contains non int/long element")
        resi = resi + 1
    return res

def CreateBoolList(list_arg):
    res = MaxPlus.BoolList()
    if not isinstance(list_arg, list):
        raise TypeError("argument is not list")
    res.SetCount(len(list_arg))
    resi = 0
    for e in list_arg:
        if isinstance(e, (bool, int, long)):
            res[resi] = bool(e)
        else:
            raise ValueError("list contains non bool/int/long element")
        resi = resi + 1
    return res

def LoadUiType(uiFile):
    """
    Pyside "loadUiType" command like PyQt4 has one, so we have to convert the
    ui file to py code in-memory first and then execute it in a special frame
    to retrieve the form_class.
    """
    import MaxPlusPySideExtend as m
    return m.LoadUiType(uiFile)
