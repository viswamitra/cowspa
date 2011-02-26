import inspect
import pycerberus

class WrapperException(Exception):
    def __init__(self, retcode, result, *args, **kw):
        self.suggested_retcode = retcode
        self.suggested_result = result
        super(WrapperException, self).__init__(*args, **kw)

def console_debugger(f):
    def wrapper(*args, **kw):
        print f.__name__, 'called with :', args, kw
        res = f(*args, **kw)
        print f.__name__, 'returned :', res
        return res
    return wrapper

def straighten_args(args, in_args, in_kw):
    inp = dict(zip(args, in_args))
    inp.update(in_kw)
    return inp

validation_failed_retcode = 3

def validator(f):
    def wrapper(*args, **kw):
        f_args = inspect.getargspec(f).args
        inp_flat = straighten_args(f_args, args, kw)
        print "entring validation"
        try:
            f.validator.process(inp_flat)
            res = f(*args, **kw)
        except pycerberus.errors.InvalidDataError, err:
            retcode = validation_failed_retcode
            res = dict((k,v.message) for (k,v) in err.error_dict().items())
            raise WrapperException(retcode, res)
        except Exception, err:
            raise err
        return res
    return wrapper

def taskmaker(f):
    return f
