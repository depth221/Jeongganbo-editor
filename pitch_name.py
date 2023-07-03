from enum import Enum, unique


@unique
class PitchName(Enum):
    HWANG = "黃"
    TAE = "太"
    JUNG = "仲"
    IM = "林"
    MU = "無"

    DAE = "大"
    HYEOP = "夾"
    GO = "姑"
    YU = "蕤"
    YI = "夷"
    NAM = "南"
    EUNG = "應"


@unique
class PitchNamePlus1(Enum):
    HWANG = "潢"
    TAE = "汰"
    JUNG = "㳞"
    IM = "淋"
    MU = "潕"

    DAE = "汏"
    HYEOP = "浹"
    GO = "㴌"
    YU = "㶋"
    YI = "洟"
    NAM = "湳"
    EUNG = "㶐"


@unique
class PitchNamePlus2(Enum):
    HWANG = "㶂"
    TAE = "㳲"
    JUNG = "㴢"
    IM = "㵉"
    MU = "㶃"

    DAE = "𣴘"
    HYEOP = "㴺"
    GO = "㵈"
    YU = "㶙"
    YI = "㴣"
    NAM = "㵜"
    EUNG = "㶝"


@unique
class PitchNameMinus1(Enum):
    HWANG = "僙"
    TAE = "㑀"
    JUNG = "㑖"
    IM = "㑣"
    MU = "㒇"

    DAE = "㐲"
    HYEOP = "俠"
    GO = "㑬"
    YU = "𠐭"
    YI = "侇"
    NAM = "㑲"
    EUNG = "㒣"


@unique
class PitchNameMinus2(Enum):
    HWANG = "㣴"
    TAE = "㣖"
    JUNG = "㣡"
    IM = "㣩"
    MU = "㣳"

    DAE = "㣕"
    HYEOP = "㣣"
    GO = "㣨"
    YU = "㣸"
    YI = "𢓡"
    NAM = "㣮"
    EUNG = "㣹"