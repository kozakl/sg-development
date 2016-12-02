# used for pymxs startup
import pymxs

def _AddGlobalUtil():
    _pymxs = pymxs
    ######################################################################################
    #  stdout/stderr support
    ######################################################################################
    class _ToListener(object):
        ''' Stream type class used to redirect standard output/error to the MAXScript listener '''
        def __init__(self, isOutput=True):
            self.isOutput = isOutput == True
            self._write = _pymxs.print_

        def write(self, txt):
            if self.isOutput:
                self._write(txt)
            else:
                self._write(txt, True)

        def flush(self):
            pass

    import sys
    sys.stdout = _ToListener()
    sys.stderr = _ToListener(False)

    ######################################################################################
    #  'with' context support
    ######################################################################################
    from contextlib import contextmanager

    # attime implementation
    @contextmanager
    def attime(time):
        ins = _pymxs.__ContextExpr('attime')
        ins(time)
        yield

    # atlevel implementation
    @contextmanager
    def atlevel(node_name):
        ins = _pymxs.__ContextExpr('atlevel')
        ins(node_name)
        yield

    # undo implementation
    @contextmanager
    def undo(onoff, label = "MAXScript"):
        if (onoff):
            ins = _pymxs.__ContextExpr('undoon')
            ins(lable)
            try:
                yield
            except Exception as e:
                if (not _pymxs.__ContextExpr.exception_handle(ins)):
                    raise e

        else:
            ins = _pymxs.__ContextExpr('undooff')
            ins(lable)
            yield

    @contextmanager
    def quiet(onoff):
        save_context = _pymxs.runtime.GetQuietMode()
        _pymxs.runtime.SetQuietMode(onoff)
        yield
        _pymxs.runtime.SetQuietMode(save_context)

    @contextmanager
    def redraw(onoff):
        save_context = _pymxs.runtime.IsSceneRedrawDisabled()
        if (onoff):
            _pymxs.runtime.EnableSceneRedraw()
        else:
            _pymxs.runtime.DisableSceneRedraw()
        yield
        if (save_context):
            _pymxs.runtime.DisableSceneRedraw()
        else:
            _pymxs.runtime.EnableSceneRedraw()

    @contextmanager
    def animate(onoff):
        save_context = _pymxs.runtime.animButtonState
        _pymxs.runtime.animButtonState = onoff
        yield
        _pymxs.runtime.animButtonState = save_context

    @contextmanager
    def mxstoken():
        try:
            _pymxs.__mxs_token__(True)
            yield
        finally:
            _pymxs.__mxs_token__()

    pymxs.atlevel = atlevel
    pymxs.attime = attime
    pymxs.animate = animate
    pymxs.quiet = quiet
    pymxs.redraw = redraw
    pymxs.undo = undo
    pymxs.mxstoken = mxstoken

_AddGlobalUtil()

del _AddGlobalUtil
del pymxs
