from flask import render_template, request, flash
# lista de hospedagens
hospedagensLista = ["Tauá Resort & Convention, Atibaia-SP",
                    "Nannai Resort & Spa, - Porto de Galinhas-PE",
                    "Iberostar Selection Praia do Forte, Açu da Torre-BA",
                    ]
# lista de viagens

viagensLista = [
    {
        'Local': 'Paris',
        'Preço': '1399,99',
        'Tempo': '10',
        'Data': '12 de janeiro',
    },
    {
        'Local': 'Rio de Janeiro',
        'Preço': '799,99',
        'Tempo': '15',
        'Data': '23 de agosto',
    },
    {
        'Local': 'Tóquio',
        'Preço': '1111,99',
        'Tempo': '9',
        'Data': '22 de novembro',
    }
]

# lista de usuários
usersLista = [
    {
        'Nome': 'João Silva',
        'CPF': '123.456.789-00',
        'E-mail': 'joao.silva@exemplo.com',
        'Telefone': '(11) 98765-4321'
    },
    {
        'Nome': 'Maria Oliveira',
        'CPF': '987.654.321-00',
        'E-mail': 'maria.oliveira@exemplo.com',
        'Telefone': '(21) 91234-5678'
    },
    {
        'Nome': 'Carlos Souza',
        'CPF': '456.123.789-00',
        'E-mail': 'carlos.souza@exemplo.com',
        'Telefone': '(31) 99876-5432'
    }
]


def init_app(app):
    # criando a rota principal do site
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/usuarios', methods=['GET', 'POST'])
    def usuarios():
        if request.method == 'POST':
            if request.form.get('nome') and request.form.get('cpf') and request.form.get('e-mail') and request.form.get('telefone'):
                usersLista.append({
                    'Nome': request.form.get('nome'),
                    'CPF': request.form.get('cpf'),
                    'E-mail': request.form.get('e-mail'),
                    'Telefone': request.form.get('telefone')
                })
        return render_template('usuarios.html',
                               usersLista=usersLista
                               )

    @app.route('/viagens', methods=['GET', 'POST'])
    def viagens():
        if request.method == 'POST':
            if request.form.get('local') and request.form.get('preco') and request.form.get('tempo') and request.form.get('data'):
                viagensLista.append({
                    'Local': request.form.get('local'),
                    'Preço': request.form.get('preco'),
                    'Tempo': request.form.get('tempo'),
                    'Data': request.form.get('data')
                })
        return render_template('viagens.html',
                               viagensLista=viagensLista
                               )

    @app.route('/hospedagens', methods=['GET', 'POST'])
    def hospedagens():
        if request.method == 'POST':
            if request.form.get('hospedagem'):
                hospedagensLista.append(request.form.get('hospedagem'))
                flash('Hospedagem cadastrada com sucesso!', 'success')

        return render_template('hospedagens.html', hospedagensLista=hospedagensLista)
