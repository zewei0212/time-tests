import times  
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
