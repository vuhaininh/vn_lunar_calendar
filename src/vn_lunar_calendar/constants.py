"""Constants for Vietnamese Lunar Calendar.

Contains Can (Heavenly Stems), Chi (Earthly Branches), Solar Term names,
Lucky Hour patterns, and other static data.
"""

# Thiên Can (10 Heavenly Stems)
CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']

# Địa Chi (12 Earthly Branches)
CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

# 24 Tiết Khí (Solar Terms) - starting from Xuân phân (Spring Equinox, 0°)
TIET_KHI = [
    'Xuân phân',     # 0°   - Spring Equinox
    'Thanh minh',    # 15°  - Clear and Bright
    'Cốc vũ',       # 30°  - Grain Rain
    'Lập hạ',       # 45°  - Start of Summer
    'Tiểu mãn',     # 60°  - Grain Full
    'Mang chủng',   # 75°  - Grain in Ear
    'Hạ chí',       # 90°  - Summer Solstice
    'Tiểu thử',     # 105° - Minor Heat
    'Đại thử',      # 120° - Major Heat
    'Lập thu',      # 135° - Start of Autumn
    'Xử thử',       # 150° - End of Heat
    'Bạch lộ',      # 165° - White Dew
    'Thu phân',      # 180° - Autumnal Equinox
    'Hàn lộ',       # 195° - Cold Dew
    'Sương giáng',  # 210° - Frost's Descent
    'Lập đông',     # 225° - Start of Winter
    'Tiểu tuyết',   # 240° - Minor Snow
    'Đại tuyết',    # 255° - Major Snow
    'Đông chí',     # 270° - Winter Solstice
    'Tiểu hàn',     # 285° - Minor Cold
    'Đại hàn',      # 300° - Major Cold
    'Lập xuân',     # 315° - Start of Spring
    'Vũ thủy',      # 330° - Rain Water
    'Kinh trập',    # 345° - Awakening of Insects
]

# Solar Terms in English
SOLAR_TERMS_EN = [
    'Spring Equinox', 'Clear and Bright', 'Grain Rain',
    'Start of Summer', 'Grain Full', 'Grain in Ear',
    'Summer Solstice', 'Minor Heat', 'Major Heat',
    'Start of Autumn', 'End of Heat', 'White Dew',
    'Autumnal Equinox', 'Cold Dew', "Frost's Descent",
    'Start of Winter', 'Minor Snow', 'Major Snow',
    'Winter Solstice', 'Minor Cold', 'Major Cold',
    'Start of Spring', 'Rain Water', 'Awakening of Insects',
]

# Giờ Hoàng Đạo patterns (1 = Lucky, 0 = Unlucky)
# Index by (chi_of_day % 6): Tý/Ngọ, Sửu/Mùi, Dần/Thân, Mão/Dậu, Thìn/Tuất, Tỵ/Hợi
GIO_HOANG_DAO = [
    '110100101100',  # Ngày Tý, Ngọ
    '001101001011',  # Ngày Sửu, Mùi
    '110011010010',  # Ngày Dần, Thân
    '101100110100',  # Ngày Mão, Dậu
    '001011001101',  # Ngày Thìn, Tuất
    '010010110011',  # Ngày Tỵ, Hợi
]

# Default timezone for Vietnam
DEFAULT_TIMEZONE = 7.0
