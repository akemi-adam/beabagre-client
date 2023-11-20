from http.client import HTTPConnection, HTTPResponse
from signal import signal, SIGPIPE, SIG_DFL   

import sys
import json

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
    def __init__(self, method: str, endpoint: str = ''):
        self.connection: HTTPConnection = HTTPConnection(sys.argv[1])
        self.method = method
        self.endpoint = endpoint

    def make_request(self, body: dict = {}, headers: dict[str, str] = {'Content-Type': 'application/json'}) -> Response:
        self.connection.request(self.method, self.endpoint, json.dumps(body), headers)
        return Response(self.connection.getresponse())


class SuapClient:
    pass


class Account:
    pass


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
    def __init__(self, specie: str, weight: float, size: int, color: str, uuid: str) -> None:
        request: Request = Request('GET', f'/bagres/{uuid}')
        response = request.make_request().response
        self.specie = response.get('specie')
        self.size = response.get('size')
        self.weight = response.get('weight')
        self.color = response.get('color')
        if specie != '':
            self.specie = specie
        if weight > 0:
            self.weight = weight
        if size > 0:
            self.size = size
        if color != '':
            self.color = color


class Menu:
    def __init__(self) -> None:
        self.operations = [Request('GET', '/bagres/'), Request('GET'), Request('POST', '/bagres/'), Request('PUT'), Request('DELETE')]

    def show(self) -> None:
        print('\n-----------------------\nOperações\n-----------------------\n1 - Listar todos os bagres\n2 - Recuperar um bagre\n3 - Cadastrar um bagre\n4 - Editar um bagre\n5 - Deletar um bagre\n6 - Sair')

    def select_option(self, option: int, body: dict = {}, headers: dict[str, str] = {'Content-Type': 'application/json'}, uuid: str|bool = False) -> Response:
        request = self.operations[option]
        if uuid:
            request.endpoint = f'/bagres/{uuid}'
        response = request.make_request(body, headers)
        return response
    
    def show_response(self, response: Response) -> None:
        print(f'Resposta:\n\n{response}\n')


menu: Menu = Menu()

loop: bool = True

signal(SIGPIPE, SIG_DFL) 

while loop:
    menu.show()
    print('')
    option = input('Escolha uma opção: ')
    print('')
    match option:
        case '1':
            try:
                response = menu.select_option(int(option) - 1)
            except BrokenPipeError:
                response = menu.select_option(0)
            menu.show_response(response)
        case '2':
            response = menu.select_option(int(option) - 1, uuid=input('Insira o UUID: '))
            menu.show_response(response)
        case '3':
            print('Digite as informações do bagre')
            body: BagreCreate = BagreCreate(input('Espécie: '), float(input('Peso: ')), int(input('Tamanho: ')), input('Cor: '))
            response = menu.select_option(int(option) - 1, body.__dict__)
            menu.show_response(response)
        case '4':
            uuid: str = input('Insira o UUID: ')
            body: BagreEdit = BagreEdit(input('Espécie: '), float(input('Peso: ')), int(input('Tamanho: ')), input('Cor: '), uuid)
            response = menu.select_option(int(option) - 1, body.__dict__, uuid=uuid)
            menu.show_response(response)
        case '5':
            response = menu.select_option(int(option) - 1, uuid=input('Insira o UUID: '))
            menu.show_response(response)
        case _:
            print('\nPrograma encerrado')
            loop = False

