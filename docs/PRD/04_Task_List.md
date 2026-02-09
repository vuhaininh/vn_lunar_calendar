# Implementation Task List – vn_lunar_calendar

## Phase 1: Core Engine (utils.py, converter.py, solar.py, lunar.py)

### 1.1 `utils.py` – Core Math Functions
- [x] `INT(d)` – Discard fractional part
- [x] `jd_from_date(dd, mm, yy)` – Solar date → Julian Day Number
- [x] `jd_to_date(jd)` – Julian Day Number → Solar date (dd, mm, yy)
- [x] `new_moon(k)` – Compute k-th New Moon (Jean Meeus algorithm)
- [x] `get_new_moon_day(k, timezone)` – New Moon day in timezone
- [x] `sun_longitude(jdn)` – Sun longitude at JDN (radians)
- [x] `get_sun_longitude(day_number, timezone)` – Sun longitude segment (0-11)
- [x] Unit tests for all above

### 1.2 `converter.py` – Conversion Engine
- [x] `get_lunar_month_11(yy, timezone)` – Find month 11 (contains Đông Chí)
- [x] `get_leap_month_offset(a11, timezone)` – Find leap month index
- [x] `solar_to_lunar(dd, mm, yy, timezone)` – Main conversion function
- [x] `lunar_to_solar(day, month, year, leap, timezone)` – Main conversion function
- [x] Add `@lru_cache` for expensive calculations
- [x] Unit tests + roundtrip tests

### 1.3 `solar.py` – SolarDate Class
- [x] `SolarDate` dataclass (frozen=True, year/month/day)
- [x] `__post_init__` validation
- [x] `to_lunar(timezone)` → LunarDate
- [x] `to_date()` → datetime.date
- [x] `to_jdn()` → int
- [x] `from_date(d)` classmethod
- [x] `from_jdn(jd)` classmethod
- [x] `today()` classmethod
- [x] `solar_term(timezone)` → str
- [x] Comparison operators (`__eq__`, `__lt__`, etc.)
- [x] Unit tests

### 1.4 `lunar.py` – LunarDate Class
- [x] `LunarDate` dataclass (frozen=True, year/month/day/is_leap)
- [x] `__post_init__` validation
- [x] `to_solar(timezone)` → SolarDate
- [x] `to_date()` → datetime.date
- [x] `from_date(d, timezone)` classmethod
- [x] `from_solar(solar, timezone)` classmethod
- [x] `today(timezone)` classmethod
- [x] Unit tests

---

## Phase 2: Can Chi (canchi.py)
- [x] `year_name(year)` – "Giáp Thìn"
- [x] `month_name(month, year)` – "Bính Dần"
- [x] `day_name(jd)` – "Canh Tuất"
- [x] `hour_name(jd)` – "Bính Tý"
- [x] Wire into `LunarDate.year_name()`, `.month_name()`, `.day_name()`, `.hour_name()`
- [x] Unit tests (verify known dates)

---

## Phase 3: Solar Terms & Lucky Hours

### 3.1 `solar_terms.py`
- [x] `get_solar_term(jd, timezone)` → str (Tiết Khí name)
- [x] `get_all_solar_terms(year, timezone)` → list of {name, date}
- [x] Wire into `SolarDate.solar_term()` and `LunarDate.solar_term()`
- [x] Unit tests

### 3.2 `lucky_hours.py`
- [x] `get_lucky_hours(jd)` → list of {name, start, end}
- [x] Wire into `LunarDate.lucky_hours()`
- [x] Unit tests

---

## Phase 4: Testing & Quality
- [x] Integration tests: roundtrip Solar↔Lunar (180+ random dates)
- [x] Edge cases: tháng nhuận, ranh giới năm, 29/02
- [x] Verify against known Tết dates (2020-2030)
- [x] Verify against known Trung Thu dates (2020-2024)
- [ ] `mypy` passes with no errors
- [x] `ruff` auto-fixes applied
- [x] 133 tests passing, coverage 80%+ (95%+ on new modules)

---

## Phase 5: Extended Features (Optional)
- [ ] `festivals.py` – Lunar festivals (Tết, Trung Thu, Vu Lan...)
- [ ] `festivals.py` – Solar festivals (1/1, 30/4, Mother's Day...)
- [ ] CLI command (`lunar-find`)
- [ ] Publish to PyPI
- [ ] Documentation site
