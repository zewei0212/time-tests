import times
import pytest

@pytest.mark.parametrize(
    ["time_range1", "time_range2", "expected"],
    [
        pytest.param(
            times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
            [
                ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
                ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
            ],
            id="generic_overlap",
        ),
        pytest.param(
            times.time_range("2010-01-12 06:00:00", "2010-01-12 07:00:00"),
            times.time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            [],
            id="no_overlap",
        ),
        pytest.param(
            times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            times.time_range("2010-01-12 12:00:00", "2010-01-12 13:00:00"),
            [],
            id="touching_but_not_overlapping",
        ),
    ],
)
def test_overlap_parametrized(time_range1, time_range2, expected):
    result = times.compute_overlap_time(time_range1, time_range2)
    assert result == expected


def test_time_range_backwards_raises():
    """
    time_range should reject a start > end.
    We expect a ValueError with a meaningful message.
    This is negative testing: we assert that bad input is *not allowed*.
    (pytest.raises is the canonical way to do this.)  # :contentReference[oaicite:8]{index=8}
    """
    with pytest.raises(ValueError) as excinfo:
        times.time_range(
            "2010-01-12 12:00:00",  # start_time
            "2010-01-12 10:00:00",  # end_time is EARLIER than start_time → invalid
            number_of_intervals=1,
            gap_between_intervals_s=0,
        )