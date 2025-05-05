from flask import render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import os

# lista de hospedagens
hospedagensLista = [
    {
        'Nome': 'Tauá Resort & Convention',
        'Local': 'Atibaia-SP',
        'Preço': 'R$ 450/noite',
        'Check-in': '15:00',
        'Check-out': '12:00',
        'Descrição': 'Resort com piscinas térmicas e ampla área verde',
        'Imagem': '/static/imgs/quarto.jpg'
    },
    {
        'Nome': 'Nannai Resort & Spa',
        'Local': 'Porto de Galinhas-PE',
        'Preço': 'R$ 890/noite',
        'Check-in': '14:00',
        'Check-out': '11:00', 
        'Descrição': 'Resort frente ao mar com all-inclusive',
        'Imagem': '/static/imgs/quarto2.jpg'
    }
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
# Lista de feedbacks
feedbacksLista = []

def init_app(app):
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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
            # Verificar campos obrigatórios
            campos_obrigatorios = ['Local', 'Preço', 'Duração', 'Data']
            if all(request.form.get(campo) for campo in campos_obrigatorios):
                # Processar upload da imagem
                imagem = request.files.get('imagem')
                imagem_url = 'https://via.placeholder.com/300'  # URL padrão

                if imagem and imagem.filename != '':
                    filename = secure_filename(imagem.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    imagem.save(filepath)
                    imagem_url = url_for('static', filename=f'uploads/{filename}')

                nova_viagem = {
                    'Local': request.form['Local'],
                    'Preço': request.form['Preço'],
                    'Duração': request.form['Duração'],
                    'Data': request.form['Data'],
                    'Imagem': imagem_url
                }
                viagensLista.append(nova_viagem)
                flash('Viagem cadastrada com sucesso!', 'success')
                return redirect(url_for('viagens'))
            else:
                flash('Preencha todos os campos obrigatórios!', 'danger')

    # Resto do código da rota...

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
            # Processar upload de imagem
            imagem = request.files.get('imagem')
            imagem_url = '/static/imgs/quarto.jpg'  # Imagem padrão
            
            if imagem and imagem.filename != '':
                filename = secure_filename(imagem.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(filepath)
                imagem_url = url_for('static', filename=f'uploads/{filename}')

            nova_hospedagem = {
                'Nome': request.form.get('nome'),
                'Local': request.form.get('local'),
                'Preço': request.form.get('preco'),
                'Check-in': request.form.get('checkin'),
                'Check-out': request.form.get('checkout'),
                'Descrição': request.form.get('descricao'),
                'Imagem': imagem_url
            }
            
            hospedagensLista.append(nova_hospedagem)
            flash('Hospedagem cadastrada com sucesso!', 'success')
            return redirect(url_for('hospedagens'))

        # Processar busca
        busca_term = request.args.get('busca', '').lower()
        if busca_term:
            resultadoBusca = [h for h in hospedagensLista if
                busca_term in h['Nome'].lower() or
                busca_term in h['Local'].lower() or
                busca_term in h['Descrição'].lower()]
        else:
            resultadoBusca = hospedagensLista

        return render_template('hospedagens.html',
                            hospedagensLista=resultadoBusca,
                            busca_term=busca_term)
    @app.route('/feedbacks', methods=['GET', 'POST'])
    def feedbacks():
        if request.method == 'POST':
            # coleta dados do formulário
            nome = request.form.get('nome', 'Anônimo')
            comentario = request.form.get('comentario', '')
            nota = int(request.form.get('nota', 0))

            # adiciona à lista
            feedbacksLista.append({
                'nome': nome,
                'comentario': comentario,
                'nota': nota
            })
            flash('Obrigado pelo feedback!', 'success')
            return redirect(url_for('feedbacks'))

        # GET: exibe formulário + feedbacks
        return render_template('feedbacks.html', feedbacks=feedbacksLista)