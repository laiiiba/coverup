FEW_SHOT_EXAMPLE_1_CODE = '''\
def chunked(iterable, n, strict=False):
    """Break *iterable* into lists of length *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6], 3))
        [[1, 2, 3], [4, 5, 6]]

    By the default, the last yielded list will have fewer than *n* elements
    if the length of *iterable* is not divisible by *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6, 7, 8], 3))
        [[1, 2, 3], [4, 5, 6], [7, 8]]

    To use a fill-in value instead, see the :func:`grouper` recipe.

    If the length of *iterable* is not divisible by *n* and *strict* is
    ``True``, then ``ValueError`` will be raised before the last
    list is yielded.

    """
    iterator = iter(partial(take, n, iter(iterable)), [])
    if strict:
        if n is None:
            raise ValueError('n must not be None when using strict mode.')

        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError('iterable is not divisible by n.')
                yield chunk

        return ret()
    else:
        return iterator
'''

FEW_SHOT_EXAMPLE_1_TESTS = '''\
import pytest
from more_itertools import chunked

def test_even():
    """Test when ``n`` divides evenly into the length of the iterable."""
    assert list(chunked('ABCDEF', 3)) == [['A', 'B', 'C'], ['D', 'E', 'F']]

def test_odd():
    """Test when ``n`` does not divide evenly into the length of the iterable."""
    assert list(chunked('ABCDE', 3)) == [['A', 'B', 'C'], ['D', 'E']]

def test_none():
    """Test when ``n`` has the value ``None``."""
    assert list(chunked('ABCDE', None)) == [['A', 'B', 'C', 'D', 'E']]

def test_strict_false():
    """Test when ``n`` does not divide evenly into the length of the iterable and strict is false."""
    assert list(chunked('ABCDE', 3, strict=False)) == [['A', 'B', 'C'], ['D', 'E']]

def test_strict_being_true():
    """Test when ``n`` does not divide evenly into the length of the iterable and strict is True (raising an exception)."""
    with pytest.raises(ValueError, match="iterable is not divisible by n"):
        list(chunked('ABCDE', 3, strict=True))

    assert list(chunked('ABCDEF', 3, strict=True)) == [['A', 'B', 'C'], ['D', 'E', 'F']]

def test_strict_being_true_with_size_none():
    """Test when ``n`` has value ``None`` and the keyword strict is True (raising an exception)."""
    with pytest.raises(ValueError, match="n must not be None when using strict mode."):
        list(chunked('ABCDE', None, strict=True))
'''

FEW_SHOT_EXAMPLE_2_CODE = '''\
def nth_or_last(iterable, n, default=_marker):
    """Return the nth or the last item of *iterable*,
    or *default* if *iterable* is empty.

        >>> nth_or_last([0, 1, 2, 3], 2)
        2
        >>> nth_or_last([0, 1], 2)
        1
        >>> nth_or_last([], 0, 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.
    """
    return last(islice(iterable, n + 1), default=default)
'''
FEW_SHOT_EXAMPLE_2_TESTS = '''\
import pytest
from more_itertools import nth_or_last

def test_basic():
    assert nth_or_last(range(3), 1) == 1
    assert nth_or_last(range(3), 3) == 2

def test_default_value():
    default = 42
    assert nth_or_last(range(0), 3, default) == default

def test_empty_iterable_no_default():
    with pytest.raises(ValueError):
        nth_or_last(range(0), 0)
'''