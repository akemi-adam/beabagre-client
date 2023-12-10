from signal import signal, SIGPIPE, SIG_DFL
from getpass import getpass

from client import Request, Response, BagreEdit, BagreCreate, Account


class Menu:
    def __init__(self) -> None:
        self.operations = [
            Request(method='POST', endpoint='/login'),
            Request(endpoint='/bagres'),
            Request(),
            Request(method='POST', endpoint='/bagres'),
            Request(method='PUT'),
            Request(method='DELETE')
        ]

    def show(self) -> None:
        print('\n-----------------------\nOperações\n-----------------------\n1 - Fazer login\n2 - Listar todos os bagres\n3 - Recuperar um bagre\n4 - Cadastrar um bagre\n5 - Editar um bagre\n6 - Deletar um bagre\n7 - Sair')

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

account: Account|None = None

token: str|None = None


while loop:
    menu.show()
    print('')
    option = int(input('Escolha uma opção: '))
    print('')
    if option >= 2 and option <= 6 and not token:
        print('Faça login antes de usar essas funcionalidades!')
        continue
    match option:
        case 1:
            print('Digete suas credenciais')
            account = Account(input('Matrícula: '), getpass('Senha: '))
            response = menu.select_option(0, account.__dict__)
            token = response.response.get('token')
            headers = headers={'Content-Type': 'application/json', 'token': token}
            print('Login feito com sucesso!')
        case 2:
            try:
                response = menu.select_option(option=1, headers=headers)
            except BrokenPipeError:
                response = menu.select_option(1)
            menu.show_response(response)
        case 3:
            response = menu.select_option(option=2, uuid=input('Insira o UUID: '), headers=headers)
            menu.show_response(response)
        case 4:
            print('Digite as informações do bagre')
            body: BagreCreate = BagreCreate(input('Espécie: '), float(input('Peso: ')), int(input('Tamanho: ')), input('Cor: '))
            response = menu.select_option(option=3, body=body.__dict__, headers=headers)
            menu.show_response(response)
        case 5:
            uuid: str = input('Insira o UUID: ')
            specie = input('Espécie: ')
            weight = input('Peso: ')
            if weight:
                weight = float(weight)
            else:
                weight = 0
            size = input('Tamanho: ')
            if size:
                size = int(size)
            else:
                size = 0
            color = input('Cor: ')
            body: BagreEdit = BagreEdit(specie, weight, size, color, uuid, headers)
            response = menu.select_option(4, body.model_dump(), headers, uuid)
            menu.show_response(response)
        case 6:
            response = menu.select_option(option=5, headers=headers, uuid=input('Insira o UUID: '))
            menu.show_response(response)
        case _:
            print('\nPrograma encerrado')
            loop = False