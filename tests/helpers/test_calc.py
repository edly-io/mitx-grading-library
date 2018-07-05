"""
Tests of calc.py
"""
from __future__ import division
import math
import random
from pytest import raises, approx
from mitxgraders import CalcError
from mitxgraders.helpers.calc import evaluator, UnableToParse, UndefinedVariable, ArgumentError
from mitxgraders.helpers.mathfunc import (cot, arcsec, arccsc, arccot, sech, csch, coth,
                                          arcsech, arccsch, arccoth, sec, csc)

def test_calcpy():
    """Tests of calc.py that aren't covered elsewhere"""

    # Test unhandled exception
    def badfunc(a):
        raise ValueError("Badness!")
    msg = (r"There was an error evaluating f\(...\). "
           "Its input does not seem to be in its domain.")
    with raises(CalcError, match=msg):
        evaluator("1+f(2)", {}, {"f": badfunc}, {})

    # Test formula with None
    result = evaluator(None, {}, {}, {})
    assert result[0] == approx(float('nan'), nan_ok=True)
    assert result[1] == set()

    # Test formulae with parallel operator
    result = evaluator("1 || 1 || 1", {}, {}, {})
    assert result[0] == 1/3
    assert result[1] == set()

    result = evaluator("1 || 1 || 0", {}, {}, {})
    assert result[0] == approx(float('nan'), nan_ok=True)
    assert result[1] == set()

    # Test incorrect case variables
    msg = r"Invalid Input: X not permitted in answer as a variable \(did you mean x\?\)"
    with raises(UndefinedVariable, match=msg):
        evaluator("X", {"x": 1}, {}, {})

def test_math():
    """Test the math functions that we've implemented"""
    x = random.uniform(0, 1)
    assert cot(x) == approx(1/math.tan(x))
    assert sec(x) == approx(1/math.cos(x))
    assert csc(x) == approx(1/math.sin(x))
    assert sech(x) == approx(1/math.cosh(x))
    assert csch(x) == approx(1/math.sinh(x))
    assert coth(x) == approx(1/math.tanh(x))
    assert arcsec(sec(x)) == approx(x)
    assert arccsc(csc(x)) == approx(x)
    assert arccot(cot(x)) == approx(x)
    assert arcsech(sech(x)) == approx(x)
    assert arccsch(csch(x)) == approx(x)
    assert arccoth(coth(x)) == approx(x)

    x = random.uniform(-1, 0)
    assert cot(x) == approx(1/math.tan(x))
    assert sec(x) == approx(1/math.cos(x))
    assert csc(x) == approx(1/math.sin(x))
    assert sech(x) == approx(1/math.cosh(x))
    assert csch(x) == approx(1/math.sinh(x))
    assert coth(x) == approx(1/math.tanh(x))
    assert -arcsec(sec(x)) == approx(x)
    assert arccsc(csc(x)) == approx(x)
    assert arccot(cot(x)) == approx(x)
    assert -arcsech(sech(x)) == approx(x)
    assert arccsch(csch(x)) == approx(x)
    assert arccoth(coth(x)) == approx(x)

def test_varnames():
    """Test variable names in calc.py"""
    # Tensor variable names
    assert evaluator("U^{ijk}", {"U^{ijk}": 2}, {}, {})[0] == 2
    assert evaluator("U_{ijk}/2", {"U_{ijk}": 2}, {}, {})[0] == 1
    assert evaluator("U_{ijk}^{123}", {"U_{ijk}^{123}": 2}, {}, {})[0] == 2
    assert evaluator("U_{ijk}^{123}'''''", {"U_{ijk}^{123}'''''": 2}, {}, {})[0] == 2
    assert evaluator("U_{ijk}^2", {"U_{ijk}": 2}, {}, {})[0] == 4
    assert evaluator("U^{ijk}^2", {"U^{ijk}": 2}, {}, {})[0] == 4
    assert evaluator("U_{ijk}^{123}^2", {"U_{ijk}^{123}": 2}, {}, {})[0] == 4
    # Regular variable names
    assert evaluator("U_cat/2 + Th3_dog__7a_", {"U_cat": 2, "Th3_dog__7a_": 4}, {}, {})[0] == 5
    # tensor subscripts need braces
    with raises(UnableToParse):
        assert evaluator("U_123^{ijk}", {}, {}, {})
    with raises(UnableToParse):
        assert evaluator("T_1_{123}^{ijk}", {}, {}, {})

def test_calc_functions_multiple_arguments():
    """Tests calc.py handling functions with multiple arguments correctly"""
    def h1(x): return x

    def h2(x, y): return x + y

    def h3(x, y, z): return x + y + z

    assert evaluator("h(2)", {}, {"h": h1}, {})[0] == 2.0
    assert evaluator("h(1, 2)", {}, {"h": h2}, {})[0] == 3.0
    assert evaluator("h(1, 2, 3)", {}, {"h": h3}, {})[0] == 6.0
    with raises(ArgumentError):
        evaluator("h(2, 1)", {}, {"h": h1}, {})
    with raises(UnableToParse):
        evaluator("h()", {}, {"h": h1}, {})
    with raises(ArgumentError):
        evaluator("h(1)", {}, {"h": h2}, {})
    with raises(ArgumentError):
        evaluator("h(1,2,3)", {}, {"h": h2}, {})
    with raises(UnableToParse):
        evaluator("h()", {}, {"h": h3}, {})
    with raises(ArgumentError):
        evaluator("h(1)", {}, {"h": h3}, {})
    with raises(ArgumentError):
        evaluator("h(1,2)", {}, {"h": h3}, {})
