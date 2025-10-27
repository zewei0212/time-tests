import times  
import pytest
def test_given_input():
    """The content in expected cell is directly copied from the result 
    of times.py. The purpose of this function is test whether the results
    match, if match the result will be pass when input pytest -v
    in the terminal."""
    
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

    result = times.compute_overlap_time(large, short)

   
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), 
                ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
        

    assert result == expected 
    ## pass


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

def test_time_range_raises_on_backwards_dates():
    with pytest.raises(ValueError, match=r"end_time .* must be after start_time"):
        times.time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")