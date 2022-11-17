from api import PetFriends
from settings import *
import os
import pytest

pf = PetFriends()


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    ''' Проверяем, что при вводе неправильного пароля нельзя получить API ключ '''

    # Отправляем запрос, ожидаем ошибку
    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    ''' Проверяем, что при вводе неправильного e-mail нельзя получить API ключ '''

    # Отправляем запрос, ожидаем ошибку
    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200, result
    содержит слово key, а также result идентичен api_key из файла settings """
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
    assert result == api_key
    # print('\n', result)


def test_get_pets_with_invalid_filter(filter='something'):
    ''' Проверяем, что нельзя получить список питомцев с неправильным фильтром '''

    # Отправляем запрос, ожидаем ошибку
    status, _ = pf.get_list_of_pets(api_key, filter)
    assert status == 500


def test_get_my_pet_info_with_wrong_key(filter='my_pets'):
    ''' Проверяем невозможность получения информации о питомцах, если указан неверный ключ '''
    # Отправляем запрос, ожидаем ошибку
    auth_key = {'key': '123'}
    status, my_pets = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос ВСЕХ питомцев возвращает не пустой список.
    Используя api_key из setting, подставляем его в запрос списка всех
    питомцев и проверяем что список не пустой.
    Доступное значение параметра filter: 'my_pets' для своих питомцев,
    либо '' для ВСЕХ питомцев """

    status, result = pf.get_list_of_pets(api_key, filter)

    assert status == 200
    assert len(result['pets']) > 0, 'Should be 100'
    # print('\n', len(result['pets']))



def test_add_new_pet_with_valid_data(name='Рыжик', animal_type='котик',
                                     age='0.7', pet_photo='images/cat1.jpg'):
    """ Проверяем, что можно добавить питомца с корректными данными
    БАГ! age принимает только string, но по документации должен number (int or float) """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    # print('\n', result['name'])


def test_add_info_about_new_pet_without_photos(name='Luntik', animal_type='unknown', age='4'):
    """ Проверяем, что можно добавить корректную информацию без фото о новом питомце
    БАГ! age принимает только string, но по документации должен number (int or float) """

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(api_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''
    # print('\n', result['name'])


def test_update_pet_photo(pet_photo='images/P1040103.jpg', filter='my_pets'):
    ''' Проверяем возможность обновления фотографии питомца '''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, filter)

    # Проверяем список питомцев, если он не пустой, меняем фото первого питомца на новое
    if len(my_pets['pets']) > 0:
        status, result = pf.add_only_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем, что статус ответа = 200 и что фото обновилось
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_update_self_pet_name(name='Полоскин', animal_type='', age=''):
    ''' Проверяем, что можно корректно изменить только имя питомца,
    остальные данные остались прежними '''

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Если список не пустой, то пробуем обновить имя первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        # pet_name = my_pets['pets'][0]['name']
        pet_type = my_pets['pets'][0]['animal_type']
        pet_age = my_pets['pets'][0]['age']
        status, result = pf.update_pet_info(api_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменилось только имя, остальные данные остались прежними
        assert status == 200
        assert result['name'] == name
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['age'] == pet_age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_update_self_pet_nimal_type(name='', animal_type='барсук', age=''):
    ''' Проверяем, что можно корректно изменить только тип питомца,
    остальные данные остались прежними '''

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Если список не пустой, то пробуем обновить тип первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pet_name = my_pets['pets'][0]['name']
        # pet_type = my_pets['pets'][0]['animal_type']
        pet_age = my_pets['pets'][0]['age']
        status, result = pf.update_pet_info(api_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменился только тип, остальные данные остались прежними
        assert status == 200
        assert result['animal_type'] == animal_type
        assert result['id'] == pet_id
        assert result['name'] == pet_name
        assert result['age'] == pet_age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_update_self_pet_age(name='', animal_type='', age=1.3):
    ''' Проверяем, что можно корректно изменить только возраст питомца,
    остальные данные остались прежними '''

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Если список не пустой, то пробуем обновить имя первого питомца
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pet_name = my_pets['pets'][0]['name']
        pet_type = my_pets['pets'][0]['animal_type']
        # pet_age = my_pets['pets'][0]['age']
        status, result = pf.update_pet_info(api_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменился только возраст, остальные данные остались прежними
        assert status == 200
        assert result['age'] == str(age)
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['name'] == pet_name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


@pytest.mark.xfail
def test_unsuccessful_update_self_pet_age(name='', animal_type='', age='one'):
    ''' Проверяем, что нельзя возраст питомца прописывать не цифрами.
    Тест проваливается!!!
    Этот тест обнаружил баг, так как найдено отклонение от документации '''

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Если список не пустой, то пробуем обновить возраст первого питомца
    if len(my_pets['pets']) > 0:
        status, _ = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Отправляем запрос, ожидаем ошибку 400
        assert status == 400
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


@pytest.mark.xfail
def test_add_wrong_age_about_new_pet_without_photos(name='Luntik2', animal_type='unknown', age='four'):
    ''' Проверяем, что нельзя возраст питомца прописывать не цифрами.
    Тест проваливается!!!
    Этот тест обнаружил баг, так как найдено отклонение от документации '''

    # Добавляем питомца
    status, _ = pf.add_new_pet_simple(api_key, name, animal_type, age)

    # Отправляем запрос, ожидаем ошибку 400
    assert status == 400


def test_successful_update_self_pet_info(name='Пупкин', animal_type='двортерьер', age=6):
    """ Проверяем возможность обновления корректной информации о питомце """

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Если список не пустой, то пробуем обновить имя, тип и возраст первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200, имя, тип и возраст питомца соответствуют заданным
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == str(age)
        # print(result['name'])
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_another_file_instead_of_a_photo(pet_photo='images/wrong_photo.txt', filter='my_pets'):
    ''' Проверяем невозможность добавления иного файла вместо фото '''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, filter)

    # Проверяем список питомцев, если он не пустой, меняем фото первого питомца на новое
    if len(my_pets['pets']) > 0:
        status, _ = pf.add_only_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 500
        assert status == 500
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """ Проверяем возможность удаления питомца """

    # Запрашиваем список СВОИХ питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print('\n', len(my_pets['pets']))

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(api_key, "Суперкот", "кот", '3.6', "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(api_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(api_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(api_key, "my_pets")
    # print(len(my_pets['pets']))

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()




















