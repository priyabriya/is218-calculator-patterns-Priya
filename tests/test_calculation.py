import pytest

from calculator.calculation import ArithmeticCalculation, Calculation
from calculator.operations import Operations


def test_factory_stores_values_and_operation():
    calculation = ArithmeticCalculation.create(5, 3, Operations.add)
    assert isinstance(calculation, ArithmeticCalculation)
    assert isinstance(calculation, Calculation)
    assert calculation.a == 5
    assert calculation.b == 3
    assert calculation.operation is Operations.add
    assert calculation.execute() == 8


@pytest.mark.parametrize("operation,expected", [
    (Operations.add, 8), (Operations.subtract, 2),
    (Operations.multiply, 15), (Operations.divide, 5 / 3),
    (lambda a, b: a ** b, 125)])
def test_different_operations(operation, expected):
    calculation = ArithmeticCalculation.create(5, 3, operation)
    assert calculation.execute() == pytest.approx(expected)


def test_execute_propagates_errors():
    calculation = ArithmeticCalculation.create(1, 0, Operations.divide)
    with pytest.raises(ValueError):
        calculation.execute()


def test_abstract_calculation_cannot_be_created():
    with pytest.raises(TypeError):
        Calculation.create(5, 3, Operations.add)
    with pytest.raises(TypeError):
        Calculation(5, 3, Operations.add)
