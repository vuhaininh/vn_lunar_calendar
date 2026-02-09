# GEMINI.md - AI Assistant Guide for vn_lunar_calendar

## Project Overview
A reusable Python package for **Vietnamese Lunar Calendar** (Lịch Âm Việt Nam) conversion and calculations.

## Tech Stack
- **Language**: Python 3.8+
- **Build System**: Hatchling (pyproject.toml)
- **Testing**: pytest + pytest-cov
- **Linting**: ruff
- **Type Checking**: mypy
- **Dependencies**: Pure Python (no external deps)

## Project Structure
```
src/vn_lunar_calendar/    # Main package (src layout)
tests/                     # Test files (test_*.py)
docs/PRD/                  # Design docs & algorithms
```

## Key Rules
1. **Always use context7 MCP** when implementing or looking up Python/library docs
2. **Pure Python only** – no C extensions, no external dependencies
3. **Type hints** on all public functions (PEP 484)
4. **Docstrings** on all public classes/functions (Google style)
5. **Immutable dates** – SolarDate and LunarDate are `frozen=True` dataclasses
6. **Default timezone = 7.0** (UTC+7 for Vietnam)
7. **Use `functools.lru_cache`** for expensive astronomical calculations

## Core Algorithms
- Based on **Ho Ngoc Duc's algorithm** (Astronomical Algorithms by Jean Meeus, 1998)
- Julian Day Number as intermediate for all date conversions
- New Moon + Sun Longitude for determining lunar months
- See `docs/PRD/02_Algorithm_Design.md` for full pseudocode

## Commands
```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=vn_lunar_calendar

# Type check
mypy src/vn_lunar_calendar/

# Lint
ruff check src/ tests/
```

## Module Dependencies (import order)
```
constants.py → exceptions.py → utils.py → converter.py → solar.py / lunar.py
                                  ↑
                            canchi.py, solar_terms.py, lucky_hours.py
```

## Important Notes
- Vietnamese lunar calendar uses **UTC+7** (different from Chinese UTC+8)
- Tháng 11 âm lịch always contains **Đông Chí** (Winter Solstice)
- Leap month (tháng nhuận) = month with **no Major Solar Term** (Trung Khí)
- Can Chi formulas use specific offsets: year→(+6,+8), day→(+9,+1), see algorithm doc
