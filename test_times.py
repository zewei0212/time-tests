# test_times.py
import pathlib
import yaml
import pytest
import times
import datetime as dt
from unittest.mock import patch, Mock
from times import iss_passes

def test_iss_passes_happy_path():
    fake_json = {
        "info": {"passescount": 2},
        "passes": [
            {"startUTC": 1609459200, "endUTC": 1609462800},
            {"startUTC": 1609466400, "endUTC": 1609470000},
        ],
    }
    with patch("times.requests.get") as mock_get:  
        mock_get.return_value.json.return_value = fake_json
        mock_get.return_value.raise_for_status.return_value = None

        
        got = iss_passes(lat=51.5074, lng=-0.1278, days=2, min_visibility_s=50, api_key="33Q884-HFUV8K-SCS3LG-55CU")

        assert got == [
            ("2021-01-01 00:00:00", "2021-01-01 01:00:00"),
            ("2021-01-01 02:00:00", "2021-01-01 03:00:00"),
        ]



def test_iss_passes_no_results():
    with patch("times.requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.json.return_value = {"info": {"passescount": 0}, "passes": []}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        out = times.iss_passes(0.0, 0.0, api_key="33Q884-HFUV8K-SCS3LG-55CU")
        assert out == []


def _build_time_range(d: dict):
   
    return times.time_range(
        d["start"], d["end"],
        d.get("number_of_intervals", 1),
        d.get("gap_between_intervals_s", 0),
    )

YAML_PATH = pathlib.Path(__file__).with_name("fixture.yaml")
cases = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))  

params = []
for item in cases:                          
    case_id, payload = next(iter(item.items()))
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

