from collections import namedtuple

Range = namedtuple('Range', 'min max')


def compute_range(opt, variable):
    opt.push()
    min_obj = opt.minimize(variable)
    opt.check()
    opt.lower(min_obj)
    min_val = opt.model()[variable].as_long()
    opt.pop()

    opt.push()
    max_obj = opt.maximize(variable)
    opt.check()
    opt.upper(max_obj)
    max_val = opt.model()[variable].as_long()
    opt.pop()

    return Range(min=min_val, max=max_val)
