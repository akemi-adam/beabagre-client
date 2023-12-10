import json

from http.client import HTTPConnection, HTTPResponse


class Response:
    def __init__(self, response: HTTPResponse):
        try:
            self.response = json.loads(response.read())
        except json.JSONDecodeError:
            self.response = json.loads('[]')

    def format_response(self) -> str:
        formated_response: str = ''
        if type(self.response) is dict:
            formated_response = self.run_dict(self.response)
        else:
            for json in self.response:
                formated_response += self.run_dict(json)
        return formated_response


    def run_dict(self, json: dict|list) -> str:
        formated_response = '{\n'
        for key in json.keys():
            formated_response += '  "{}": "{}",\n'.format(key, json.get(key))
        formated_response += '},\n\n'
        return formated_response

    def __str__(self) -> str:
        return self.format_response()


class Request:
    def __init__(self, base_uri: str = 'localhost', method: str = 'GET', endpoint: str = '/'):
        self.connection: HTTPConnection = HTTPConnection(base_uri, 8000)
        self.method = method
        self.endpoint = endpoint

    def make_request(self, body: dict = {}, headers: dict[str, str] = {'Content-Type': 'application/json'}) -> Response:
        self.connection.request(self.method, self.endpoint, json.dumps(body), headers)
        return Response(self.connection.getresponse())


class Account:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Bagre:
    def __init__(self, specie: str, weight: float, size: int, color: str) -> None:
        self.specie = specie
        self.weight = weight
        self.size = size
        self.color = color


class BagreCreate(Bagre):
    def __init__(self, specie: str, weight: float, size: int, color: str) -> None:
        while True:
            if specie != '' and weight != 0 and size != 0 and color != '':
                break
            elif specie == '':
                specie = input('Espécie não pode ser nula: ')
            elif weight <= 0:
                weight = float(input('Peso não pode ser 0: '))
            elif size <= 0:
                size = int(input('Tamanho não pode ser 0: '))
            elif color == '':
                color = input('Cor não pode ser nula: ')
        super().__init__(specie, weight, size, color)


class BagreEdit(Bagre):
    def __init__(self, specie: str, weight: float, size: int, color: str, uuid: str, headers: dict[str, str]) -> None:
        self.model = {}
        if specie != '':
            self.model['specie'] = specie
        if weight > 0:
            self.model['weight'] = weight
        if size > 0:
            self.model['size'] = size
        if color != '':
            self.model['color'] = color

    def model_dump(self) -> dict:
        return self.model
