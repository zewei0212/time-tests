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


def test_given_input():
    """The content in expected cell is directly copied from the result 
    of times.py. The purpose of this function is test whether the results
    match, if match the result will be pass when input pytest -v
    in the terminal."""

    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00",
                             "2010-01-12 10:45:00", 2, 60)

    result = times.compute_overlap_time(large, short)

    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
                ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]

    assert result == expected
    # pass


def test_no_overlap():
    """Two time ranges that do not overlap at all.
    After fixing compute_overlap_time to only append if low < high,
    expect an empty list."""

    a = [("2010-01-12 07:00:00", "2010-01-12 08:00:00")]

    b = [("2010-01-12 10:00:00", "2010-01-12 11:00:00")]

    result = times.compute_overlap_time(a, b)

    assert result == []


def test_multiple_intervals_each_side():
    """Two time ranges that both contain several intervals.
    first handcraft them, so we know exactly what overlaps should be. """

    a = [
        ("2010-01-12 09:00:00", "2010-01-12 10:00:00"),
        ("2010-01-12 11:00:00", "2010-01-12 12:00:00"),
    ]

    b = [
        ("2010-01-12 09:40:00", "2010-01-12 09:50:00"),
        ("2010-01-12 11:35:00", "2010-01-12 11:55:00"),
    ]

    result = times.compute_overlap_time(a, b)

    expected = [
        ("2010-01-12 09:40:00", "2010-01-12 09:50:00"),
        ("2010-01-12 11:35:00", "2010-01-12 11:55:00"),
    ]

    assert result == expected


def test_touching_intervals_no_overlap():
    """Two time ranges where one ends just when the other starts. This is considered 
    no overlap."""

    a = [("2010-01-12 10:00:00", "2010-01-12 11:00:00")]
    b = [("2010-01-12 11:00:00", "2010-01-12 12:00:00")]

    result = times.compute_overlap_time(a, b)

    # there is no positive-length overlap. We expect [].
    assert result == []

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