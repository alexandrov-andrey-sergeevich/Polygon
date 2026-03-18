from typing import Final

# Приоритеты
PRIORITY_LOWEST: Final[int] = 0
PRIORITY_LOW: Final[int] = 20
PRIORITY_MEDIUM: Final[int] = 50
PRIORITY_HIGH: Final[int] = 80
PRIORITY_HIGHEST: Final[int] = 100

# Допуски и погрешности для смеси
PROPORTION_SUM_TOLERANCE: Final[float] = 0.01
PROPORTION_MIN: Final[float] = 0.0
PROPORTION_MAX: Final[float] = 1.0

# Значения по умолчанию
DEFAULT_PRIORITY: Final[int] = PRIORITY_MEDIUM
DEFAULT_CAPACITY: Final[int] = 1
