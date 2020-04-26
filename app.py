from flask import Flask, jsonify, request, Response
from settings import app
import json

books: list = [
    {
        'author': 'daniil',
        'book_name': 'flask_edu',
        'id': 1
    },
    {
        'author': 'dan',
        'book_name': 'edu_flask',
        'id': 2
    }
]


class BookInfoValidator:
    """
    -- проверяет, что книга информация о книге имеет всю необходимую информацию
    -- делает проверку на наличие всех ключей и что все значения по ключам не равны None
    -- если равны  None, то заменяет на дефолтное значение
    """
    KEYS: set = {'author', 'book_name', 'id'}
    ERROR_TEMPLATE: dict = {
        'error': 'error msg'}

    def __init__(self, book_info: dict):
        self.book_info = book_info

    def check_book_info(self):
        if not self._check_keys():
            self.ERROR_TEMPLATE['error'] = 'Проверьте ключи, с ними что-то не так'
            return json.dumps(self.ERROR_TEMPLATE)
        if not self._check_values():
            self.ERROR_TEMPLATE['error'] = 'Проверьте значения, с ними что-то не так'
            return json.dumps(self.ERROR_TEMPLATE)

    def _check_keys(self) -> bool:
        return set(self.book_info.keys()) == self.KEYS

    def _check_values(self) -> bool:
        books_values: set = set(self.book_info.values())
        for value in books_values:
            if not bool(value):
                return False
        else:
            return True


class BookInfoValidatorForPatch(BookInfoValidator):

    def __init__(self, book_info: dict):
        super().__init__(book_info)

    def _check_keys(self) -> bool:
        for key in self.book_info:
            if key not in self.KEYS:
                return False
        else:
            return True


def find_and_update(code: int, book_info: dict, book_id: int = None) -> Response:
    if code == 204:
        book_to_replace: dict = list(filter(lambda x: x.get('id') == book_id, books))[0]
        index: int = books.index(book_to_replace)
        books[index].update(book_info)
    else:
        books.append(book_info)
    response = Response('OK', code, mimetype='application/json')
    response.headers['Location'] = f'/books/{book_info.get("id")}'
    return response


@app.route('/books')
def get_books() -> str:
    response: str = jsonify({'books': books})
    return response


@app.route('/books', methods=['POST'])
def add_book() -> str:
    book_info: dict = request.get_json()
    validator = BookInfoValidator(book_info)
    error_msg = validator.check_book_info()
    if error_msg:
        return Response(error_msg, 400, mimetype='application/json')
    else:
        response = find_and_update(201, book_info)
    return response


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_whole_book_by_id(book_id: int):
    book_info: dict = request.get_json()
    validator = BookInfoValidator(book_info)
    error_msg = validator.check_book_info()
    if error_msg:
        return Response(error_msg, 400, mimetype='application/json')
    else:
        response = find_and_update(204, book_info, book_id)
    return response


@app.route('/books/<int:book_id>')
def get_books_by_id(book_id) -> str:
    return jsonify(list(filter(lambda x: x.get('id') == book_id, books))[0])


@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_field_of_book_by_id(book_id) -> str:
    book_info: dict = request.get_json()
    validator = BookInfoValidatorForPatch(book_info)
    error_msg = validator.check_book_info()
    if error_msg:
        return Response(error_msg, 400, mimetype='application/json')
    else:
        response = find_and_update(204, book_info, book_id)
    return response


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id) -> str:
    filtered_data: list = list(filter(lambda x: x.get('id') == book_id, books))
    if not filtered_data:
        error_msg: dict = {'error': "Нет книги с таким номером"}
        return Response(json.dumps(error_msg), 404, mimetype='application/json')
    books.remove(filtered_data[0])
    return Response("OK", 204, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
