# Задание 19.7.2 "Testing API PetFriends"
  
1. У нас есть готовая библиотека с реализацией основных методов, но остались ещё два нереализованных метода. Это и будет первым практическим заданием: посмотреть [документацию](https://petfriends.skillfactory.ru/apidocs/) к имеющимся API-методам. Найти методы, которые ещё не реализованы в библиотеке, и написать их реализацию в файле api.py.  
2. Подумайте над вариантами тест-кейсов и напишите 10 различных тестов для данного REST API-интерфейса.

---

Объект тестирования: *[сайт "PetFriends"](https://petfriends.skillfactory.ru/)*  
API сайта: *[Flasgger](https://petfriends.skillfactory.ru/apidocs/)*  

### [Чек-листы проверок запросов API](https://docs.google.com/document/d/19Zi-HGKGmOGSEF2Vj2uyXNN5MaooKe_Y7DQB0I1Pe7c/edit?usp=drivesdk)  


#### Окружение: 
- OC Windows 10 Version 21H2   
- Google Chrome  Версия 109.0.5414.75, (64 бита)

В целях сокрытия конфиденциальной информации проекте используется файл `.env` (*не представлен*), для которого нужна библиотека "python-dotenv"
#### Пример содержания файла `.env`:
>valid_email = '`example@email.com`'  
>valid_password = '`QwErTy`'  
> api_key = '`000a111af68474a80f55555bfcca2d9643ebef831d6c46c72dcc0b99`'

Перед запуском тестов требуется установить необходимые библиотеки командой:
   ```bash
   pip install -r requirements.txt
   ```
Для запуска тестов через терминал следует набрать команду:  
   ```bash
   pytest -v -s tests\test_pet_friends.py
   ```