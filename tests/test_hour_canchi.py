"""Tests for hour Can Chi feature — get_hour_info and hour_chi_index."""

import pytest

from vn_lunar_calendar.canchi import HOUR_RANGES, get_hour_info, hour_chi_index
from vn_lunar_calendar.constants import CAN, CHI
from vn_lunar_calendar.solar import SolarDate


class TestHourChiIndex:
    """Test hour_chi_index maps clock hours to correct Chi."""

    @pytest.mark.parametrize("hour,expected_chi", [
        (23, "Tý"), (0, "Tý"),         # 23:00 - 01:00
        (1, "Sửu"), (2, "Sửu"),        # 01:00 - 03:00
        (3, "Dần"), (4, "Dần"),         # 03:00 - 05:00
        (5, "Mão"), (6, "Mão"),         # 05:00 - 07:00
        (7, "Thìn"), (8, "Thìn"),       # 07:00 - 09:00
        (9, "Tỵ"), (10, "Tỵ"),         # 09:00 - 11:00
        (11, "Ngọ"), (12, "Ngọ"),       # 11:00 - 13:00
        (13, "Mùi"), (14, "Mùi"),       # 13:00 - 15:00
        (15, "Thân"), (16, "Thân"),     # 15:00 - 17:00
        (17, "Dậu"), (18, "Dậu"),       # 17:00 - 19:00
        (19, "Tuất"), (20, "Tuất"),     # 19:00 - 21:00
        (21, "Hợi"), (22, "Hợi"),       # 21:00 - 23:00
    ])
    def test_mapping(self, hour, expected_chi):
        idx = hour_chi_index(hour)
        assert CHI[idx] == expected_chi

    def test_invalid_hour_negative(self):
        with pytest.raises(ValueError):
            hour_chi_index(-1)

    def test_invalid_hour_over_23(self):
        with pytest.raises(ValueError):
            hour_chi_index(24)


class TestGetHourInfo:
    """Test get_hour_info returns correct Can Chi for specific times."""

    def test_3am_11_07_1989(self):
        """3:15 AM on 11/07/1989 = Giờ Dần, Nhâm Dần."""
        info = get_hour_info(3, 11, 7, 1989)
        assert info["chi"] == "Dần"
        assert info["name"] == "Nhâm Dần"
        assert info["start"] == "03:00"
        assert info["end"] == "05:00"

    def test_noon_11_07_1989(self):
        """12:00 on 11/07/1989 = Giờ Ngọ."""
        info = get_hour_info(12, 11, 7, 1989)
        assert info["chi"] == "Ngọ"

    def test_midnight_0(self):
        """00:00 = Giờ Tý."""
        info = get_hour_info(0, 1, 1, 2024)
        assert info["chi"] == "Tý"

    def test_23h_is_next_day_ty(self):
        """23:00 = Giờ Tý of the NEXT day's cycle.

        The Can of Tý at 23:00 on day D should equal the Can of Tý
        at 00:00 on day D+1.
        """
        info_23 = get_hour_info(23, 1, 1, 2024)
        info_next = get_hour_info(0, 2, 1, 2024)
        assert info_23["chi"] == "Tý"
        assert info_next["chi"] == "Tý"
        assert info_23["can"] == info_next["can"]
        assert info_23["name"] == info_next["name"]

    def test_all_12_hours_have_unique_chi(self):
        """All 12 double-hours on one day should have distinct Chi."""
        hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        chis = [get_hour_info(h, 1, 1, 2024)["chi"] for h in hours]
        assert len(set(chis)) == 12

    def test_can_cycles_every_5_days(self):
        """The Can of Giờ Tý cycles through 10 stems every 5 days."""
        infos = [get_hour_info(0, d, 1, 2024) for d in range(1, 6)]
        cans = [i["can"] for i in infos]
        assert len(set(cans)) == 5  # 5 unique Cans in 5 days

    def test_result_dict_has_all_keys(self):
        info = get_hour_info(8, 15, 3, 2024)
        assert "can" in info
        assert "chi" in info
        assert "name" in info
        assert "start" in info
        assert "end" in info
        assert "is_lucky" in info

    def test_name_matches_can_chi(self):
        info = get_hour_info(14, 20, 6, 2000)
        assert info["name"] == f"{info['can']} {info['chi']}"

    def test_can_is_valid(self):
        info = get_hour_info(9, 5, 5, 2025)
        assert info["can"] in CAN

    def test_chi_is_valid(self):
        info = get_hour_info(17, 5, 5, 2025)
        assert info["chi"] in CHI

    def test_is_lucky_is_bool(self):
        info = get_hour_info(6, 1, 1, 2024)
        assert isinstance(info["is_lucky"], bool)

    def test_invalid_hour(self):
        with pytest.raises(ValueError):
            get_hour_info(25, 1, 1, 2024)


class TestSolarDateGetHourInfo:
    """Test SolarDate.get_hour_info method."""

    def test_delegates_correctly(self):
        sd = SolarDate(11, 7, 1989)
        info = sd.get_hour_info(3)
        assert info["name"] == "Nhâm Dần"

    def test_all_hours_valid(self):
        sd = SolarDate(1, 1, 2024)
        for h in range(24):
            info = sd.get_hour_info(h)
            assert info["can"] in CAN
            assert info["chi"] in CHI


class TestHourRanges:
    """Test HOUR_RANGES constant."""

    def test_has_12_entries(self):
        assert len(HOUR_RANGES) == 12

    def test_all_chi_names(self):
        chis = [hr["chi"] for hr in HOUR_RANGES]
        assert chis == list(CHI)
