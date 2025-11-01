# test_times.py
import pathlib
import yaml
import pytest
import times

def _build_time_range(d: dict):
    
    return times.time_range(
        d["start"],
        d["end"],
        d.get("number_of_intervals", 1),
        d.get("gap_between_intervals_s", 0),
    )

YAML_PATH = pathlib.Path(__file__).with_name("fixture.yaml")
with YAML_PATH.open("r", encoding="utf-8") as f:
    cases = yaml.safe_load(f)  


params = []
for entry in cases:                      
    case_id, payload = next(iter(entry.items()))
    tr1 = _build_time_range(payload["time_range_1"])
    tr2 = _build_time_range(payload["time_range_2"])
    expected = [tuple(x) for x in payload["expected"]]
    params.append(pytest.param(tr1, tr2, expected, id=case_id))

@pytest.mark.parametrize(["time_range1", "time_range2", "expected"], params)
def test_overlap_parametrized(time_range1, time_range2, expected):
    assert times.compute_overlap_time(time_range1, time_range2) == expected

def test_time_range_backwards_raises():
    with pytest.raises(ValueError):
        times.time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
