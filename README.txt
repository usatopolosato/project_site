Приветствуем вас в нашем репозитории.
 Для того чтобы насладиться всем функционалом сайта,
 Запустите сервер локально и авторизуйтесь
 Под логином: test
 Пароль: 1234567890aA
На нашем сайте существует API
Вот пример получения api-key для новой роли(в glitch данная функция отключена):
print(requests.get('http://127.0.0.1:5000/api/key_roles/2',
                   json={'api_key': 'extymtbnhelltytuvytlflen'}).json())
Данный api-key является ключом разработчика, будьте осторожны.


Welcome to our repository.
 In order to enjoy all the functionality of the site,
 Start the server locally and log in
 Under the username: test
 Password: 1234567890aA
There is an API on our website
Here is an example of getting an api key for a new role(this feature is disabled in glitch):
print(requests.get('http://127.0.0.1:5000/api/key_roles/2',
json={'api_key': 'extymtbnhelltytuvytlflen'}).json())
This api key is the developer's key, be careful.
