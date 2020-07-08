
from run import theory

T = theory()

models = [
    {'b': False, 'c': True, 'a': True},
    {'b': True, 'c': True, 'a': True},
    {'c': False, 'b': True, 'a': False},
    {'c': True, 'b': True, 'a': False}
]

non_models = [
    {'a': True, 'c': False, 'b': True},
    {'a': True, 'c': False, 'b': False},
    {'a': False, 'c': True, 'b': False},
    {'a': False, 'c': False, 'b': False}
]

for m in models:
    assert T.satisfied_by(m), "Error: This should be a model but isn't\n\t %s" % str(m)

for m in non_models:
    assert not T.satisfied_by(m), "Error: This shouldn't be a model but is\n\t %s" % str(m)
