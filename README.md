Классификатор мусора.

https://разделяйкин.рф

Основное приложение - https://github.com/morozec/GarbageCollector

Команда: **Next City** (стол 7)

## Requirements

- Python 3.6.5+


## Установка

`pip install -r requirements.txt`

## Использование

Запусти

`python app.py`

Затем на http://localhost:5000/ можешь отправлять GET запросы вида `?path=/path/to/image.jpg`

Возвращаю json формата

`{'category': 'glass', 'probability': 0.95}`
