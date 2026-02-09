# Thiết Kế Thuật Toán: Vietnamese Lunar Calendar
## Algorithm Design Document

---

## 1. Tổng Quan Các Phương Pháp (Approach Comparison)

Qua nghiên cứu 3 repository tham khảo, có **3 phương pháp chính** để tính lịch âm:

### 1.1 Phương Pháp 1: Lookup Table (Bảng tra cứu)
> Sử dụng bởi: **wolfhong/LunarCalendar**

- **Nguyên lý**: Mã hóa thông tin mỗi năm âm lịch thành một số nguyên (packed binary), lưu trong mảng
- **Ưu điểm**: Nhanh, đơn giản, không cần tính toán thiên văn
- **Nhược điểm**: Giới hạn phạm vi thời gian, cần dữ liệu pre-computed

### 1.2 Phương Pháp 2: Year Code Encoding
> Sử dụng bởi: **nacana22/lunar-date**

- **Nguyên lý**: Mã hóa thông tin năm vào "year code" chứa: offset Tết, độ dài 12 tháng, tháng nhuận
- **Ưu điểm**: Phạm vi rộng (1200-2199), cấu trúc rõ ràng
- **Nhược điểm**: Vẫn cần dữ liệu pre-computed cho mỗi thế kỷ

### 1.3 Phương Pháp 3: Astronomical Calculation (Tính toán thiên văn)
> Sử dụng bởi: **ThienMD/lich-van-nien-flutter** (gốc từ [Ho Ngoc Duc](https://www.informatik.uni-leipzig.de/~duc/amlich/))

- **Nguyên lý**: Tính trực tiếp vị trí Mặt Trời (Sun Longitude) và thời điểm Trăng Mới (New Moon) bằng công thức thiên văn
- **Ưu điểm**: Không giới hạn phạm vi, chính xác cao, là phương pháp "gốc"
- **Nhược điểm**: Phức tạp hơn, tính toán nhiều hơn

### 1.4 Phương Pháp Được Chọn: **Hybrid (Kết hợp)**

Chúng ta sẽ sử dụng **phương pháp Astronomical Calculation** làm nền tảng (giống Ho Ngoc Duc / ThienMD) vì:
1. **Chính xác**: Dựa trên thuật toán thiên văn chuẩn (Jean Meeus, 1998)
2. **Phạm vi rộng**: Không bị giới hạn bởi bảng dữ liệu
3. **Đã được kiểm chứng**: Thuật toán Ho Ngoc Duc được sử dụng rộng rãi nhất cho lịch âm Việt Nam
4. **Timezone chính xác**: Sử dụng UTC+7 cho Việt Nam (khác với Trung Quốc UTC+8)

Kết hợp thêm **lookup table** để cache kết quả và tăng tốc cho phạm vi phổ biến (1900-2100).

---

## 2. Thuật Toán Chi Tiết

### 2.1 Julian Day Number (JDN)

JDN là số nguyên ngày liên tục kể từ 1/1/4713 BC (Julian Calendar). Đây là nền tảng cho mọi phép tính chuyển đổi.

#### 2.1.1 Ngày Dương → JDN

```
Thuật toán: Công thức Tondering
Input:  dd (ngày), mm (tháng), yy (năm) theo dương lịch
Output: jd (Julian Day Number)

1. a = INT((14 - mm) / 12)
2. y = yy + 4800 - a
3. m = mm + 12 * a - 3
4. jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) 
       - INT(y / 100) + INT(y / 400) - 32045

// Nếu trước 15/10/1582 (lịch Julian, chưa Gregorian):
Nếu jd < 2299161:
    jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) - 32083
```

#### 2.1.2 JDN → Ngày Dương

```
Input:  jd (Julian Day Number)
Output: dd, mm, yy (ngày, tháng, năm dương lịch)

Nếu jd > 2299160 (Gregorian Calendar):
    1. a = jd + 32044
    2. b = INT((4 * a + 3) / 146097)
    3. c = a - INT((b * 146097) / 4)
Ngược lại (Julian Calendar):
    1. b = 0
    2. c = jd + 32082

4. d = INT((4 * c + 3) / 1461)
5. e = c - INT((1461 * d) / 4)
6. m = INT((5 * e + 2) / 153)
7. day   = e - INT((153 * m + 2) / 5) + 1
8. month = m + 3 - 12 * INT(m / 10)
9. year  = b * 100 + d - 4800 + INT(m / 10)
```

---

### 2.2 Tính Thời Điểm Trăng Mới (New Moon)

> Algorithm source: "Astronomical Algorithms" by Jean Meeus, 1998

Trăng mới (Sóc - 朔) là thời điểm Mặt Trăng và Mặt Trời có cùng kinh độ ecliptic (hoàng kinh). Đây là mốc bắt đầu mỗi tháng âm lịch.

```
Input:  k (số thứ tự trăng mới kể từ 1/1/1900 13:52 UTC)
Output: JD (thời điểm trăng mới, dạng số thực)

1. T = k / 1236.85                              // Julian centuries từ 1900
2. T2 = T * T
3. T3 = T2 * T
4. dr = π / 180                                  // degree → radian

5. Jd1 = 2415020.75933 + 29.53058868 * k 
       + 0.0001178 * T2 - 0.000000155 * T3
6. Jd1 += 0.00033 * sin((166.56 + 132.87 * T 
       - 0.009173 * T2) * dr)                    // Mean new moon

7. M   = 359.2242 + 29.10535608 * k 
       - 0.0000333 * T2 - 0.00000347 * T3        // Sun's mean anomaly
8. Mpr = 306.0253 + 385.81691806 * k 
       + 0.0107306 * T2 + 0.00001236 * T3         // Moon's mean anomaly
9. F   = 21.2964 + 390.67050646 * k 
       - 0.0016528 * T2 - 0.00000239 * T3         // Moon's argument of latitude

// Correction terms
10. C1  = (0.1734 - 0.000393 * T) * sin(M * dr) + 0.0021 * sin(2 * dr * M)
11. C1 -= 0.4068 * sin(Mpr * dr) + 0.0161 * sin(dr * 2 * Mpr)
12. C1 -= 0.0004 * sin(dr * 3 * Mpr)
13. C1 += 0.0104 * sin(dr * 2 * F) - 0.0051 * sin(dr * (M + Mpr))
14. C1 -= 0.0074 * sin(dr * (M - Mpr)) + 0.0004 * sin(dr * (2 * F + M))
15. C1 -= 0.0004 * sin(dr * (2 * F - M)) - 0.0006 * sin(dr * (2 * F + Mpr))
16. C1 += 0.0010 * sin(dr * (2 * F - Mpr)) + 0.0005 * sin(dr * (2 * Mpr + M))

// Delta T correction
17. Nếu T < -11:
        deltat = 0.001 + 0.000839*T + 0.0002261*T2 
               - 0.00000845*T3 - 0.000000081*T*T3
    Ngược lại:
        deltat = -0.000278 + 0.000265*T + 0.000262*T2

18. JdNew = Jd1 + C1 - deltat
19. Return JdNew
```

#### Hàm Phụ Trợ: Ngày Trăng Mới Trong Timezone

```
getNewMoonDay(k, timeZone):
    return INT(NewMoon(k) + 0.5 + timeZone / 24)
```

---

### 2.3 Tính Sun Longitude (Kinh Độ Mặt Trời)

Sun Longitude xác định vị trí Mặt Trời trên hoàng đạo, cần thiết cho việc xác định tháng âm lịch và 24 tiết khí.

```
Input:  jdn (Julian Day Number, số thực)
Output: L (Sun Longitude, radian, trong khoảng [0, 2π))

1. T  = (jdn - 2451545.0) / 36525    // Julian centuries từ J2000.0
2. T2 = T * T
3. dr = π / 180

// Mean anomaly (độ)
4. M  = 357.52910 + 35999.05030 * T - 0.0001559 * T2 
       - 0.00000048 * T * T2

// Mean longitude (độ)
5. L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2

// Equation of center
6. DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * sin(dr * M)
       + (0.019993 - 0.000101 * T) * sin(dr * 2 * M)
       + 0.000290 * sin(dr * 3 * M)

// True longitude
7. L = L0 + DL
8. L = L * dr                         // Convert to radians
9. L = L - 2π * INT(L / (2π))         // Normalize to [0, 2π)

Return L
```

#### Sun Longitude Segment (cho xác định tháng)

```
getSunLongitude(dayNumber, timeZone):
    // Tính Sun Longitude tại lúc 0h (nửa đêm) theo timezone
    return INT(SunLongitude(dayNumber - 0.5 - timeZone / 24) / π * 6)
    
// Kết quả: số từ 0-11, biểu thị segment trên hoàng đạo
// 0: Xuân phân → Thanh minh
// 1: Thanh minh → ...
// ...
// 11: Kinh trập → Xuân phân
```

---

### 2.4 Chuyển Đổi Dương → Âm Lịch

Đây là thuật toán chính, kết hợp New Moon và Sun Longitude.

```
Input:  dd, mm, yy (ngày dương lịch), timeZone (mặc định 7.0 cho VN) 
Output: lunarDay, lunarMonth, lunarYear, lunarLeap

 1. dayNumber = jdFromDate(dd, mm, yy)

 2. // Tìm ngày Sóc (đầu tháng âm) chứa ngày dayNumber
    k = INT((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = getNewMoonDay(k + 1, timeZone)
    if monthStart > dayNumber:
        monthStart = getNewMoonDay(k, timeZone)

 3. // Tìm ngày Sóc tháng 11 âm lịch (Đông Chí)
    a11 = getLunarMonth11(yy, timeZone)
    b11 = a11
    
    if a11 >= monthStart:
        lunarYear = yy
        a11 = getLunarMonth11(yy - 1, timeZone)
    else:
        lunarYear = yy + 1
        b11 = getLunarMonth11(yy + 1, timeZone)

 4. // Tính ngày âm
    lunarDay = dayNumber - monthStart + 1

 5. // Tính tháng âm
    diff = INT((monthStart - a11) / 29)
    lunarLeap = 0
    lunarMonth = diff + 11

 6. // Xử lý tháng nhuận
    if b11 - a11 > 365:                    // Năm có tháng nhuận
        leapMonthDiff = getLeapMonthOffset(a11, timeZone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                lunarLeap = 1              // Đây là tháng nhuận

 7. if lunarMonth > 12:
        lunarMonth -= 12

 8. if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1

 9. Return [lunarDay, lunarMonth, lunarYear, lunarLeap]
```

#### Hàm getLunarMonth11: Tìm Tháng 11 Âm Lịch

Tháng 11 âm lịch là tháng chứa **Đông Chí** (Winter Solstice, Sun Longitude segment = 9).

```
getLunarMonth11(yy, timeZone):
    1. off = jdFromDate(31, 12, yy) - 2415021
    2. k = INT(off / 29.530588853)
    3. nm = getNewMoonDay(k, timeZone)
    4. sunLong = getSunLongitude(nm, timeZone)
    5. if sunLong >= 9:
           nm = getNewMoonDay(k - 1, timeZone)
    6. return nm
```

#### Hàm getLeapMonthOffset: Tìm Tháng Nhuận

Tháng nhuận là tháng **không chứa Trung Khí** (Major Solar Term). Thuật toán tìm tháng nhuận đầu tiên sau tháng 11.

```
getLeapMonthOffset(a11, timeZone):
    1. k = INT((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    2. last = 0
    3. i = 1
    4. arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
    5. repeat:
           last = arc
           i++
           arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
       until arc != last or i >= 14
    6. return i - 1
```

---

### 2.5 Chuyển Đổi Âm → Dương Lịch

```
Input:  lunarDay, lunarMonth, lunarYear, lunarLeap, timeZone
Output: [dd, mm, yy] (ngày dương lịch)

 1. if lunarMonth < 11:
        a11 = getLunarMonth11(lunarYear - 1, timeZone)
        b11 = getLunarMonth11(lunarYear, timeZone)
    else:
        a11 = getLunarMonth11(lunarYear, timeZone)
        b11 = getLunarMonth11(lunarYear + 1, timeZone)

 2. k = INT(0.5 + (a11 - 2415021.076998695) / 29.530588853)

 3. off = lunarMonth - 11
    if off < 0:
        off += 12

 4. // Xử lý tháng nhuận
    if b11 - a11 > 365:
        leapOff = getLeapMonthOffset(a11, timeZone)
        leapMonth = leapOff - 2
        if leapMonth < 0:
            leapMonth += 12
        if lunarLeap != 0 and lunarMonth != leapMonth:
            return [0, 0, 0]  // Invalid
        elif lunarLeap != 0 or off >= leapOff:
            off += 1

 5. monthStart = getNewMoonDay(k + off, timeZone)
 6. return jdToDate(monthStart + lunarDay - 1)
```

---

### 2.6 Can Chi (Sexagenary Cycle / Thiên Can Địa Chi)

Hệ thống 60 tổ hợp giữa 10 Thiên Can và 12 Địa Chi.

#### Constants

```python
CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
```

#### Can Chi Năm

```
Input:  year (năm âm lịch)
Output: string (vd: "Giáp Thìn")

can = CAN[(year + 6) % 10]
chi = CHI[(year + 8) % 12]
return can + " " + chi
```

> Giải thích: năm 4 (Giáp Tý đầu tiên) → (4+6)%10=0 (Giáp), (4+8)%12=0 (Tý) ✓

#### Can Chi Tháng

```
Input:  month (tháng âm lịch), year (năm âm lịch)
Output: string

can = CAN[(year * 12 + month + 3) % 10]
chi = CHI[(month + 1) % 12]
return can + " " + chi
```

> Giải thích: Tháng 1 → chi = CHI[2] = "Dần" (tháng Giêng luôn là Dần)

#### Can Chi Ngày

```
Input:  jd (Julian Day Number)
Output: string

can = CAN[(jd + 9) % 10]
chi = CHI[(jd + 1) % 12]
return can + " " + chi
```

#### Can Chi Giờ (Giờ đầu ngày - Giờ Tý)

```
Input:  jd (Julian Day Number)
Output: string

can = CAN[(jd - 1) * 2 % 10]
chi = CHI[0]  // Tý
return can + " " + chi
```

---

### 2.7 Tiết Khí (24 Solar Terms)

24 tiết khí chia hoàng đạo thành 24 phần bằng nhau (mỗi phần 15°).

```python
TIET_KHI = [
    'Xuân phân',    # 0°     - Spring Equinox
    'Thanh minh',   # 15°    - Clear and Bright
    'Cốc vũ',       # 30°    - Grain Rain
    'Lập hạ',       # 45°    - Start of Summer
    'Tiểu mãn',     # 60°    - Grain Full
    'Mang chủng',   # 75°    - Grain in Ear
    'Hạ chí',       # 90°    - Summer Solstice
    'Tiểu thử',     # 105°   - Minor Heat
    'Đại thử',      # 120°   - Major Heat
    'Lập thu',      # 135°   - Start of Autumn
    'Xử thử',       # 150°   - End of Heat
    'Bạch lộ',      # 165°   - White Dew
    'Thu phân',      # 180°   - Autumnal Equinox
    'Hàn lộ',       # 195°   - Cold Dew
    'Sương giáng',  # 210°   - Frost's Descent
    'Lập đông',     # 225°   - Start of Winter
    'Tiểu tuyết',   # 240°   - Minor Snow
    'Đại tuyết',    # 255°   - Major Snow
    'Đông chí',     # 270°   - Winter Solstice
    'Tiểu hàn',     # 285°   - Minor Cold
    'Đại hàn',      # 300°   - Major Cold
    'Lập xuân',     # 315°   - Start of Spring
    'Vũ thủy',      # 330°   - Rain Water
    'Kinh trập',    # 345°   - Awakening of Insects
]
```

```
Tính tiết khí cho một ngày:
    getTietKhi(jd):
        return TIET_KHI[getSunLongitude(jd + 1, 7.0)]
```

---

### 2.8 Giờ Hoàng Đạo (Lucky Hours)

Mỗi ngày có 6 giờ Hoàng Đạo (tốt) và 6 giờ Hắc Đạo (xấu), dựa vào Địa Chi của ngày.

```python
# Pattern Giờ Hoàng Đạo: 1 = Hoàng Đạo, 0 = Hắc Đạo
# Áp dụng cho 12 chi giờ: Tý(23-1), Sửu(1-3), Dần(3-5),..., Hợi(21-23)
GIO_HOANG_DAO = [
    '110100101100',  # Ngày Tý, Ngọ
    '001101001011',  # Ngày Sửu, Mùi
    '110011010010',  # Ngày Dần, Thân
    '101100110100',  # Ngày Mão, Dậu
    '001011001101',  # Ngày Thìn, Tuất
    '010010110011',  # Ngày Tỵ, Hợi
]
```

```
getLuckyHours(jd):
    1. chiOfDay = (jd + 1) % 12
    2. pattern = GIO_HOANG_DAO[chiOfDay % 6]
    3. lucky_hours = []
    4. for i in 0..11:
           if pattern[i] == '1':
               hour = {
                   name: CHI[i],
                   start: (i * 2 + 23) % 24,
                   end:   (i * 2 + 1) % 24
               }
               lucky_hours.append(hour)
    5. return lucky_hours
```

---

## 3. Quy Tắc Cốt Lõi Của Lịch Âm Việt Nam

### 3.1 Tháng Âm Lịch
- Mỗi tháng bắt đầu từ ngày **Sóc** (New Moon / Trăng mới)
- Tháng có 29 hoặc 30 ngày

### 3.2 Năm Âm Lịch
- Năm bình thường: **12 tháng** (~354 ngày)
- Năm nhuận: **13 tháng** (~384 ngày, thêm 1 tháng nhuận)

### 3.3 Tháng Nhuận
- Tháng nhuận là tháng **không chứa Trung Khí** (Major Solar Term)
- Trung Khí: Xuân phân, Cốc vũ, Tiểu mãn, Hạ chí, Đại thử, Xử thử, Thu phân, Sương giáng, Tiểu tuyết, Đông chí, Đại hàn, Vũ thủy
- Tháng nhuận mang tên của tháng đứng trước nó

### 3.4 Tháng 11
- Tháng 11 âm lịch là tháng **chứa Đông Chí** (Winter Solstice)
- Đây là mốc neo quan trọng nhất để tính lịch âm

### 3.5 Timezone
- Lịch âm Việt Nam sử dụng **UTC+7** (khác Trung Quốc UTC+8)
- Điều này có thể dẫn đến sự khác biệt 1 ngày so với lịch âm Trung Quốc trong một số trường hợp

---

## 4. Data Flow

```
                    ┌─────────────┐
                    │  User Input  │
                    │ (Solar Date) │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Validate    │
                    │  Solar Date  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Solar → JDN │
                    │  (jdFromDate)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐  ┌─▼──────┐  ┌─▼───────────┐
       │  Find New    │  │ Find   │  │ Determine   │
       │  Moon (Sóc)  │  │ Month  │  │ Leap Month  │
       │  containing  │  │ 11     │  │ (if any)    │
       │  this day    │  │ (a11)  │  │             │
       └──────┬──────┘  └─┬──────┘  └─┬───────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │  Calculate   │
                    │  Lunar Date  │
                    │  (day,month, │
                    │   year,leap) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐  ┌─▼──────┐  ┌─▼───────────┐
       │  Can Chi     │  │ Tiết   │  │ Giờ Hoàng   │
       │  (Năm,Tháng │  │ Khí    │  │ Đạo         │
       │   Ngày,Giờ) │  │        │  │             │
       └─────────────┘  └────────┘  └─────────────┘
```

---

## 5. Caching Strategy

Để tối ưu performance, sử dụng cache cho:

1. **New Moon calculations**: Cache kết quả `getNewMoonDay(k, tz)` vì cùng k+tz luôn cho cùng kết quả
2. **getLunarMonth11**: Cache theo (year, timezone)
3. **Year decode**: Cache danh sách tháng âm lịch của mỗi năm

Sử dụng `functools.lru_cache` của Python stdlib.

---

## 6. Độ Chính Xác & Giới Hạn

### 6.1 Nguồn Gốc Thuật Toán
- **Sun Longitude**: "Astronomical Algorithms" by Jean Meeus, 1998
- **New Moon**: Cùng nguồn Jean Meeus
- **Adapted by**: Ho Ngoc Duc (Đại học Leipzig, Đức) cho lịch Việt Nam

### 6.2 Sai Số
- Sun Longitude: ±0.01° (đủ chính xác cho mục đích lịch)
- New Moon: ±0.5 ngày (đủ để xác định ngày Sóc)
- So với lịch chính thức: cực kỳ hiếm khi sai (< 0.1% trong 1000 năm)

### 6.3 Trường Hợp Đặc Biệt
- **1582**: Chuyển đổi lịch Julian → Gregorian (ngày 05-14/10/1582 không tồn tại)
- **Ranh giới năm**: Tết Nguyên Đán rơi vào tháng 1 hoặc 2 dương lịch
- **Tháng nhuận kép**: Rất hiếm nhưng có thể xảy ra
