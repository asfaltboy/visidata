from visidata import VisiData
import visidata

alias = visidata.BaseSheet.bindkey

def deprecated(ver):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # ideally would include a stacktrace
            visidata.warning(f'{func.__name__} deprecated since v{ver}')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@deprecated('1.6')
@VisiData.api
def __call__(vd):
    'Deprecated; use plain "vd"'
    return vd


@deprecated('1.6')
def copyToClipboard(value):
    return visidata.clipboard().copy(value)


@deprecated('1.6')
def replayableOption(optname, default, helpstr):
    option(optname, default, helpstr, replay=True)

@deprecated('1.6')
def SubrowColumn(*args, **kwargs):
    return visidata.SubColumnFunc(*args, **kwargs)

@deprecated('1.6')
def DeferredSetColumn(*args, **kwargs):
    return Column(*args, defer=True, **kwargs)


alias('edit-cells', 'setcol-input')  # 1.6
alias('fill-nulls', 'setcol-fill')  # 1.6
alias('paste-cells', 'setcol-clipboard')  # 1.6
alias('frequency-rows', 'frequency-summary')  # 1.6
alias('dup-cell', 'dive-cell')  # 1.6
alias('dup-row', 'dive-row')  # 1.6