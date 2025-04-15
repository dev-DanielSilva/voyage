from flask import render_template, request, flash, redirect, url_for
# lista de hospedagens
hospedagensLista = ["Tauá Resort & Convention, Atibaia-SP",
                    "Nannai Resort & Spa, Porto de Galinhas-PE",
                    "Iberostar Selection Praia do Forte, Açu da Torre-BA",
                    ]
# lista de viagens

viagensLista = [
    {
        'Local': 'Paris',
        'Preço': '1399,99',
        'Tempo': '10',
        'Data': '12 de janeiro',
        'Imagem': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80' 
    },
    {
        'Local': 'Rio de Janeiro',
        'Preço': '799,99',
        'Tempo': '15',
        'Data': '23 de agosto',
        'Imagem': 'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80'
    },
    {
        'Local': 'Tóquio',
        'Preço': '1111,99',
        'Tempo': '9',
        'Data': '22 de novembro',
        'Imagem': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1371&q=80'
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
        return render_template('index.html', viagensLista=viagensLista)

    @app.route('/usuarios', methods=['GET', 'POST'])
    def usuarios():
        busca_term = request.args.get('busca', '').lower()
        
        if request.method == 'POST':
            # Adicionar novo usuário
            novo_usuario = {
                'Nome': request.form.get('nome'),
                'CPF': request.form.get('cpf'),
                'E-mail': request.form.get('e-mail'),
                'Telefone': request.form.get('telefone')
            }
            usersLista.append(novo_usuario)
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('usuarios'))

        # Filtrar resultados da busca
        if busca_term:
            resultado_busca = [usuario for usuario in usersLista if
                busca_term in usuario['Nome'].lower() or
                busca_term in usuario['CPF'].lower() or
                busca_term in usuario['E-mail'].lower() or
                busca_term in usuario['Telefone'].lower()
            ]
        else:
            resultado_busca = usersLista

        return render_template('usuarios.html',
                            usersLista=resultado_busca,
                            busca_term=busca_term)

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
                # Redireciona para evitar reenvio do formulário
                return redirect(url_for('hospedagens'))

        # Processa a busca
        busca_term = request.args.get('busca', '').lower()
        if busca_term:
            resultadoBusca = [
                h for h in hospedagensLista if busca_term in h.lower()]
        else:
            resultadoBusca = hospedagensLista

        return render_template('hospedagens.html',
                               hospedagensLista=resultadoBusca,
                               busca_term=busca_term)
