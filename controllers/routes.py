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
        'Duração': '10',
        'Data': '12 de janeiro',
        'Imagem': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80'
    },
    {
        'Local': 'Rio de Janeiro',
        'Preço': '799,99',
        'Duração': '15',
        'Data': '23 de agosto',
        'Imagem': 'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80'
    },
    {
        'Local': 'Tóquio',
        'Preço': '1111,99',
        'Duração': '9',
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
        busca_term = request.args.get('busca', '').lower()
        
        if request.method == 'POST':
            # Verifica se todos os campos foram preenchidos corretamente
            if all([request.form.get('Local'), request.form.get('Preço'), 
                   request.form.get('Duração'), request.form.get('Data')]):
                nova_viagem = {
                    'Local': request.form.get('Local'),
                    'Preço': request.form.get('Preço'),
                    'Duração': request.form.get('Duração'),
                    'Data': request.form.get('Data'),
                    'Imagem': request.form.get('imagem') or 'https://via.placeholder.com/300'
                }
                viagensLista.append(nova_viagem)
                flash('Viagem cadastrada com sucesso!', 'success')
                return redirect(url_for('viagens'))

        # Filtrar resultados da busca
        if busca_term:
            viagens_filtradas = [
                v for v in viagensLista 
                if (busca_term in v['Local'].lower() or 
                    busca_term in v['Preço'].lower() or 
                    busca_term in v['Data'].lower() or
                    busca_term in v['Duração'].lower())
            ]
        else:
            viagens_filtradas = viagensLista

        return render_template('viagens.html',
                            viagensLista=viagens_filtradas,
                            busca_term=busca_term)

    @app.route('/hospedagens', methods=['GET', 'POST'])
    def hospedagens():
        if request.method == 'POST':
            if request.form.get('hospedagem'):
                hospedagensLista.append(request.form.get('hospedagem'))
                flash('Hospedagem cadastrada com sucesso!', 'success')
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