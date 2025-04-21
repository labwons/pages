from functools import wraps
from inspect import signature


def validate_argument(*values):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound =  signature(func).bind(*args, **kwargs)
            bound.apply_defaults()
            param = [key for key in bound.arguments if key != 'self']
            if len(param) != 1:
                raise ValueError(f'Unable to validate for more than one parameters')

            if bound.arguments.get(param[0], None) not in values:
                raise ValueError(f"Invalid value for parameter: @{param}. Allowed values are: {values}")
            return func(*args, **kwargs)
        return wrapper
    return decorate
