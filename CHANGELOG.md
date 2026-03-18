# Changelog

Все значимые изменения в проекте будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Базовая структура проекта с модулями `models/` и `core/`
- Модели данных для буферов:
  - `BulkBufferConfig` — конфигурация буфера непрерывных материалов.
  - `DiscreteBufferConfig` — конфигурация буфера дискретных объектов.
- Модели данных для деталей:
  - `BulkPartConfig` — непрерывные материалы.
  - `DiscretePartConfig` — дискретные объекты.
  - `MixturePartConfig` — смеси с валидацией пропорций.
  - `AssemblyPartConfig` — сборочные единицы.
- Модели данных для процессов:
  - `SimpleProcessConfig` — базовый процесс обработки.
  - `AssemblingProcessConfig` — процесс сборки.
  - `DisassemblingProcessConfig` — процесс разборки.
  - `MixingProcessConfig` — процесс смешивания.
- Политики активации процессов (временно отложены для после MVP)
- Файл констант `constants.py` с приоритетами и допусками
- Единый стиль `docstring` для всех моделей данных

### Changed
- Переименованы классы политик активации для краткости:
  - `DiscreteBatchActivationConfig` → `DiscreteBatchConfig`
  - `BulkBatchActivationConfig` → `BulkBatchConfig`
  - `BaseActivationPolicyConfig` → `BaseActivationConfig`
- Удалён параметр `threshold` из `ImmediateConfig` (политики активации отложены)

### Fixed
- Исправлена некорректная валидация `gt=0` для полей с `None` по умолчанию
- Исправлена валидация в `BaseBufferConfig.capacity` (убрано `gt=0` для `None`)

### Removed
- Политики активации временно удалены из рабочего кода (перенесены на после MVP)

---

## [0.0.6] - 2026-03-19

### Added
- Модели данных проекта
- Новая структура проекта

[Unreleased]: https://github.com/alexandrov-andrey-sergeevich/polygon/compare/v0.0.1...HEAD
[0.0.6]: https://github.com/alexandrov-andrey-sergeevich/polygon/releases/tag/v0.0.1