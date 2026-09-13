import pytest

from phantom.core.condition.decoders import Decoder, PiecewiseLinear


@pytest.mark.parametrize(
    "points",
    [
        (),
        ((0.0, 0.0),),
        ((0.0, 0.0), (0.0, 1.0)),
        ((1.0, 0.0), (0.0, 1.0)),
        ((0.0, 0.0), (1.0, float("inf"))),
    ],
)
def test_invalid_interpolation_rejected(points: tuple[tuple[float, float], ...]) -> None:
    with pytest.raises(ValueError):
        PiecewiseLinear(points)


def test_generic_interpolation_handles_both_slopes_and_rejects_extrapolation() -> None:
    curve = PiecewiseLinear(((0.0, 5.0), (2.0, 1.0), (6.0, 9.0)))
    assert [curve.decode(x) for x in (0.0, 1.0, 2.0, 4.0, 6.0)] == [5.0, 3.0, 1.0, 5.0, 9.0]
    for value in (-1.0, 7.0, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            curve.decode(value)
    with pytest.raises(TypeError):
        Decoder()  # type: ignore[abstract]
