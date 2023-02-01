# api_final
### Описание
Проект позволит вам создавать посты и подписываться на любимых авторов!
Так же есть возможность оставлять свои комментарии под понравившимися (или напротив) постами!

# Как запустить проект:
```
git clone https://github.com/virtuous-hub/api_final_yatube.git
```
```
cd api_final_yatube
```
# Создать и активировать виртуальное окружение
```
python -m venv venv
```
```
source venv/Scripts/activate
```
# Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
``` 
# Выполнить миграции:
```
python3 manage.py migrate
```
# Запустить проект:
``` 
python3 manage.py runserver
``` 
