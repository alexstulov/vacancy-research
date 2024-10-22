# Анализ вакансий hh.ru

## Цели
1. Получить представление о современных требованиях в анализе данных,
2. Добавить  в портфолио проект получения, подготовки, анализа и визуализации данных.

## Использование проекта
Полный список специальностей можно получить [запросом](https://api.hh.ru/professional_roles). id выбранной специальности передайте агрументом при создании экземпляра VacancyAggregator.

### Получение данных
Инициализация, сбор данных и сохранение в Excel:

```python
va = VacancyAggregator(123)
va.aggregateInfo()
va.saveToXlsx()
```

Запуск:

```bash
python3 index.py
```

### Анализ данных
Изучить процесс можно в Jupyter Notebook по [ссылке](https://nbviewer.org/github/alexstulov/vacancy-research/blob/main/vacancy_research.ipynb).

Гипотеза 1: Существует особый "аналитический" язык для описания вакансий,

Гипотеза 2: Технический стек отличается по разделам (аналитик, финансовый/инвестиционный аналитик, BI-аналитик/аналитик данных, продуктовый аналитик, маркетинговый аналитик).

Облако латинских слов из описания вакансий в разделе "BI-аналитик/аналитик данных":

![Облако латинских слов из описания вакансий в разделе "BI-аналитик/аналитик данных"](/images/analyst_latin_word_cloud.png)

## Выводы
* Гипотеза 1 опровергнута - наиболее частые слова универсальны для описания вакансий,
* Гипотеза 2 подтверждена - Python и SQL преобладают в разделах BI-аналитик/Аналитик данных, Продуктовый аналитик. Следующий по популярности инструмент Excel наиболее часто встречается в разделе Финансовый/Инвестиционный аналитик,
* Для программиста, переезжающего в анализ данных, больше шансов найти работу по специальностям BI-аналитик/аналитик данных и Продуктовый аналитик на стеке Python/SQL,
* Анализ описания вакансии позволяет выявить специальные термины и инструменты с большим успехом, нежели анализ ключевых навыков,
* Повысить точность модели можно при фильтрации вакансий по грейду (junior, middle, senior), если реализовать соответствующий фильтр в VacancyAggregator,