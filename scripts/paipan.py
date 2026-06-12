#!/usr/bin/env python3
"""
八字精确排盘计算器
用法: python3 paipan.py <公历年> <公历月> <公历日> [时辰/小时] [性别m/f]
示例: python3 paipan.py 2002 8 2 10 f
"""
import sys
from datetime import date

TIANGAN = '甲乙丙丁戊己庚辛壬癸'
DIZHI = '子丑寅卯辰巳午未申酉戌亥'
WUXING_STEM = ['木','木','火','火','土','土','金','金','水','水']
WUXING_BRANCH = ['水','土','木','木','土','火','火','土','金','金','土','水']

CANGGAN = {
    '子': [('癸',10)],
    '丑': [('己',10),('癸',3),('辛',3)],
    '寅': [('甲',10),('丙',3),('戊',3)],
    '卯': [('乙',10)],
    '辰': [('戊',10),('乙',3),('癸',3)],
    '巳': [('丙',10),('戊',3),('庚',3)],
    '午': [('丁',10),('己',3)],
    '未': [('己',10),('丁',3),('乙',3)],
    '申': [('庚',10),('壬',3),('戊',3)],
    '酉': [('辛',10)],
    '戌': [('戊',10),('辛',3),('丁',3)],
    '亥': [('壬',10),('甲',3)],
}

# 十二长生表 (阳干用顺行，阴干用逆行)
CHANGSHENG = ['长生','沐浴','冠带','临官','帝旺','衰','病','死','墓','绝','胎','养']
# 各阳干长生起始地支index: 甲→亥(11), 丙→寅(2), 戊→寅(2), 庚→巳(5), 壬→申(8)
YANG_CHANGSHENG_START = {0:11, 2:2, 4:2, 6:5, 8:8}
# 阴干长生起始: 乙→午(6), 丁→酉(9), 己→酉(9), 辛→子(0), 癸→卯(3)
YIN_CHANGSHENG_START = {1:6, 3:9, 5:9, 7:0, 9:3}

NAYIN = [
    '海中金','炉中火','大林木','路旁土','剑锋金','山头火',
    '涧下水','城头土','白蜡金','杨柳木','泉中水','屋上土',
    '霹雳火','松柏木','长流水','砂石金','山下火','平地木',
    '壁上土','金箔金','覆灯火','天河水','大驿土','钗钏金',
    '桑柘木','大溪水','砂中土','天上火','石榴木','大海水'
]

# 节气近似日期 (月份, 日期) - 用于判断月柱
JIE_QI = {
    '立春': (2, 4), '惊蛰': (3, 6), '清明': (4, 5), '立夏': (5, 6),
    '芒种': (6, 6), '小暑': (7, 7), '立秋': (8, 7), '白露': (9, 8),
    '寒露': (10, 8), '立冬': (11, 7), '大雪': (12, 7), '小寒': (1, 6),
}

def jiazi(index):
    return TIANGAN[index % 10] + DIZHI[index % 12]

def jiazi_index(stem_idx, branch_idx):
    for i in range(60):
        if i % 10 == stem_idx and i % 12 == branch_idx:
            return i
    return -1

def get_nayin(jiazi_idx):
    return NAYIN[jiazi_idx // 2]

def get_changsheng(day_stem_idx, branch_idx):
    if day_stem_idx % 2 == 0:  # 阳干
        start = YANG_CHANGSHENG_START[day_stem_idx]
        offset = (branch_idx - start) % 12
    else:  # 阴干逆行
        start = YIN_CHANGSHENG_START[day_stem_idx]
        offset = (start - branch_idx) % 12
    return CHANGSHENG[offset]

def get_shishen(stem_idx, day_stem_idx):
    if stem_idx == day_stem_idx:
        return '日主'
    wuxing_map = [0,0,1,1,2,2,3,3,4,4]
    dm_wx = wuxing_map[day_stem_idx]
    other_wx = wuxing_map[stem_idx]
    same_sex = (day_stem_idx % 2 == stem_idx % 2)

    rel = (other_wx - dm_wx) % 5
    names = {
        0: ('比肩','劫财'),
        1: ('食神','伤官'),
        2: ('偏财','正财'),
        3: ('七杀','正官'),
        4: ('偏印','正印'),
    }
    return names[rel][0] if same_sex else names[rel][1]

def get_month_branch(year, month, day):
    """根据节气判断月支"""
    jie_order = ['小寒','立春','惊蛰','清明','立夏','芒种',
                 '小暑','立秋','白露','寒露','立冬','大雪']
    branch_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]  # 丑寅卯辰巳午未申酉戌亥子

    current_month_idx = month - 1
    jie_name = jie_order[current_month_idx]
    jie_month, jie_day = JIE_QI[jie_name]

    if day >= jie_day:
        return branch_order[current_month_idx]
    else:
        prev_idx = (current_month_idx - 1) % 12
        return branch_order[prev_idx]

def get_month_stem(year_stem, month_branch):
    """年上起月法"""
    zi_month_stem = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]
    寅_index = 2
    offset = (month_branch - 寅_index) % 12
    return (zi_month_stem[year_stem] + offset) % 10

def get_hour_stem(day_stem, hour_branch):
    """日上起时法"""
    zi_hour_stem = [0, 2, 4, 6, 8, 0, 2, 4, 6, 8]
    return (zi_hour_stem[day_stem] + hour_branch) % 10

def hour_to_branch(hour):
    """将小时转为地支index"""
    if hour == 23 or hour == 0:
        return 0
    return ((hour + 1) // 2) % 12

def calculate_dayun(month_jiazi_idx, is_forward, birth_year, start_age):
    """计算大运序列"""
    result = []
    for i in range(1, 9):
        if is_forward:
            dy_idx = (month_jiazi_idx + i) % 60
        else:
            dy_idx = (month_jiazi_idx - i) % 60
        age_start = start_age + (i-1) * 10
        age_end = age_start + 9
        year_start = birth_year + age_start
        year_end = birth_year + age_end
        result.append({
            'gz': jiazi(dy_idx),
            'age': f'{age_start}-{age_end}',
            'years': f'{year_start}-{year_end}',
            'stem': TIANGAN[dy_idx % 10],
            'branch': DIZHI[dy_idx % 12],
        })
    return result

def paipan(year, month, day, hour=None, gender=None):
    """主排盘函数"""
    # 年柱
    year_for_calc = year
    if month < 2 or (month == 2 and day < 4):
        year_for_calc = year - 1
    year_stem = (year_for_calc - 4) % 10
    year_branch = (year_for_calc - 4) % 12
    year_jiazi = jiazi_index(year_stem, year_branch)

    # 月柱
    month_branch = get_month_branch(year, month, day)
    month_stem = get_month_stem(year_stem, month_branch)
    month_jiazi = jiazi_index(month_stem, month_branch)

    # 日柱
    ref_date = date(1900, 1, 1)
    ref_index = 10  # 1900-01-01 = 甲戌
    target = date(year, month, day)
    delta = (target - ref_date).days
    day_jiazi = (ref_index + delta) % 60
    day_stem = day_jiazi % 10
    day_branch = day_jiazi % 12

    # 时柱
    hour_info = None
    if hour is not None:
        h_branch = hour_to_branch(hour)
        h_stem = get_hour_stem(day_stem, h_branch)
        hour_jiazi = jiazi_index(h_stem, h_branch)
        hour_info = {
            'gz': TIANGAN[h_stem] + DIZHI[h_branch],
            'stem': TIANGAN[h_stem],
            'branch': DIZHI[h_branch],
            'stem_idx': h_stem,
            'branch_idx': h_branch,
            'nayin': get_nayin(hour_jiazi),
            'changsheng': get_changsheng(day_stem, h_branch),
            'shishen_stem': get_shishen(h_stem, day_stem),
        }

    result = {
        'year': {
            'gz': TIANGAN[year_stem] + DIZHI[year_branch],
            'stem': TIANGAN[year_stem], 'branch': DIZHI[year_branch],
            'stem_idx': year_stem, 'branch_idx': year_branch,
            'nayin': get_nayin(year_jiazi),
            'changsheng': get_changsheng(day_stem, year_branch),
            'shishen_stem': get_shishen(year_stem, day_stem),
        },
        'month': {
            'gz': TIANGAN[month_stem] + DIZHI[month_branch],
            'stem': TIANGAN[month_stem], 'branch': DIZHI[month_branch],
            'stem_idx': month_stem, 'branch_idx': month_branch,
            'nayin': get_nayin(month_jiazi),
            'changsheng': get_changsheng(day_stem, month_branch),
            'shishen_stem': get_shishen(month_stem, day_stem),
        },
        'day': {
            'gz': TIANGAN[day_stem] + DIZHI[day_branch],
            'stem': TIANGAN[day_stem], 'branch': DIZHI[day_branch],
            'stem_idx': day_stem, 'branch_idx': day_branch,
            'nayin': get_nayin(day_jiazi),
            'changsheng': get_changsheng(day_stem, day_branch),
        },
        'hour': hour_info,
        'day_master': TIANGAN[day_stem],
        'day_master_wuxing': WUXING_STEM[day_stem],
        'day_master_yinyang': '阳' if day_stem % 2 == 0 else '阴',
    }

    # 大运
    if gender:
        is_yang_year = (year_stem % 2 == 0)
        is_male = (gender.lower() in ['m', '男'])
        is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
        result['dayun_direction'] = '顺排' if is_forward else '逆排'
        result['dayun'] = calculate_dayun(month_jiazi, is_forward, year, 9)  # 默认9岁起运

    # 藏干与十神
    for pillar in ['year', 'month', 'day']:
        branch = result[pillar]['branch']
        cg = CANGGAN[branch]
        result[pillar]['canggan'] = [(g, get_shishen(TIANGAN.index(g), day_stem)) for g, _ in cg]
    if hour_info:
        branch = hour_info['branch']
        cg = CANGGAN[branch]
        hour_info['canggan'] = [(g, get_shishen(TIANGAN.index(g), day_stem)) for g, _ in cg]

    return result

def print_result(r):
    print(f"\n{'='*60}")
    print(f"日主：{r['day_master']}（{r['day_master_yinyang']}{r['day_master_wuxing']}）")
    print(f"{'='*60}")

    headers = ['', '年柱', '月柱', '日柱', '时柱']
    pillars = [r['year'], r['month'], r['day'], r.get('hour')]

    print(f"\n{'':>6} {'年柱':>8} {'月柱':>8} {'日柱':>8} {'时柱':>8}")
    print(f"{'天干':>6}", end='')
    for p in pillars:
        print(f" {p['stem'] if p else '?':>7}", end='')
    print()
    print(f"{'地支':>6}", end='')
    for p in pillars:
        print(f" {p['branch'] if p else '?':>7}", end='')
    print()
    print(f"{'纳音':>6}", end='')
    for p in pillars:
        print(f" {p['nayin'] if p else '?':>7}", end='')
    print()
    print(f"{'地势':>6}", end='')
    for p in pillars:
        print(f" {p['changsheng'] if p else '?':>7}", end='')
    print()

    print(f"\n十神：")
    for name, p in [('年干', r['year']), ('月干', r['month']), ('时干', r.get('hour'))]:
        if p and 'shishen_stem' in p:
            print(f"  {p['stem']}（{name}）→ {p['shishen_stem']}")

    print(f"\n藏干：")
    for name, p in [('年支', r['year']), ('月支', r['month']), ('日支', r['day']), ('时支', r.get('hour'))]:
        if p and 'canggan' in p:
            cg_str = '、'.join(f"{g}({ss})" for g, ss in p['canggan'])
            print(f"  {p['branch']}（{name}）→ {cg_str}")

    if 'dayun' in r:
        print(f"\n大运（{r['dayun_direction']}）：")
        for dy in r['dayun']:
            print(f"  {dy['age']}岁：{dy['gz']}（{dy['years']}）")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    y, m, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

    # 第4/5个参数灵活解析：数字=小时，m/f/男/女=性别，'-'=时辰未知占位
    h, g = None, None
    for arg in sys.argv[4:6]:
        if arg == '-':
            continue
        if arg.lower() in ('m', 'f', '男', '女'):
            g = arg
        else:
            h = int(arg)

    # 夜子时（23点后）按次日日柱计算
    if h == 23:
        from datetime import timedelta
        nd = date(y, m, d) + timedelta(days=1)
        y, m, d, h = nd.year, nd.month, nd.day, 0
        print("【夜子时】23点后出生，已按次日日柱排盘")

    result = paipan(y, m, d, h, g)
    print_result(result)
    if 'dayun' in result:
        print("\n⚠️ 起运年龄为近似值（默认9岁）。精确起运年龄需按节气天数÷3计算，")
        print("   干支序列正确，仅年龄区间可能整体偏移，请按 references/dayun-rules.md 修正。")
