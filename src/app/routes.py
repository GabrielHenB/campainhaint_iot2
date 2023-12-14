from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from markupsafe import escape
from flask_cors import CORS
import os

from app import app, db
from app.models import Imagem, Pessoa, Evento
from app.config import Config
from facereq.facialreq import reconhecimento

# CONSTANTES GLOBAIS (Outras estao em config.py)
# Extensoes permitidas no envio de arquivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Endereco local do ESP-32
ENDERECO_ESP = "192.168.0.45"
# Endereco do Aplicativo
ENDERECO_APP = "127.0.0.1:8000"

# Cross-Origin Resource Sharing routes
#CORS(app, resources={r"/*": {"origins": [ENDERECO_ESP, ENDERECO_APP]}}) 
CORS(app)

# Esse endpoint retorna um pequeno documento HTML para testes
@app.route('/', methods=['GET'])
def index(name=None):
    return render_template('index.html', name=name)

# Esse endpoint serve apenas para debug e inicializa o banco de dados com o ORM SQLAlchemy
@app.route('/debugdb')
def debugdb():
    print("iniciando criacao de dados no bd")
    with app.app_context():
        db.create_all()
    return redirect(url_for('index'))

# Esse endpoint espera receber um request com arquivo de nome "imagem" que sera salva
# associada a uma pessoa apos o reconhecimento obter dados disso ou nao
@app.route('/upload', methods=['POST'])
def store():
    # Receber a Imagem do ESP-32 CAM ou outro Dispositivo
    try:
        print("Teste do arquivo: ")
        filess = request.files
        for file_namee, file_data in filess.items():
            print(f"File Name: {file_namee}")
            print(f"Content Type: {file_data.content_type}")
            print(f"Content Length: {file_data.content_length}")
            
        
        # Aqui ele verifica se existe o campo no request object se nao BAD REQUEST
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Request vazio!'}), 400
        
        # Assuming the photo is sent in the request body
        resposta = request.files['imagem']
        
        # Valida se tem arquivo e se a extensao eh permitida. O backend nao aceita outras extensoes. Poderia validar tamanho tambem.
        if resposta.filename == '':
            return jsonify({'erro': 'Request sem imagem!'}), 400

        if not (allowed_file(resposta.filename)):
            return jsonify({'erro': 'Tipo invalido de arquivo. Deve ser png, jpg, jpeg'}), 400
        
        # Usa o helper de sanitizar nomes de arquivos do werkzeug. Talvez depois mudar para outro esquema.
        nome_seguro = secure_filename(resposta.filename)

        # Salva a imagem usando o caminho atual (src) e o configurado para a pasta das imagens com o nome
        path_correction()
        caminho_salvar = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], nome_seguro)
        resposta.save(caminho_salvar)

        # Realizar reconhecimento facial e obter resposta ID da Pessoa ou None
        id_reconhecido = usar_facerec(caminho_salvar)
        
        # Bom se for None ele avisa mas internamente toda Imagem com pessoa_id None eh considerada Desconhecido
        if id_reconhecido is None:
            print("Nao reconhecido")

        # Isso aqui cria uma nova Row no banco de dados com a nova Imagem
        if resposta:
            new_photo = Imagem(photo_path=caminho_salvar,pessoa_id=id_reconhecido)
            db.session.add(new_photo)
            db.session.commit()
        
        # Um Evento deve ser registrado
        if resposta:
            new_evento = Evento(pessoa_id=id_reconhecido,imagem_id=new_photo.id_img)
            db.session.add(new_evento)
            db.session.commit()
        

        return jsonify({"status": "A imagem foi salva com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({'status': '500','msg': str(e)}), 500

# Esse endpoint equivale ao registro de uma nova pessoa quando escolher salvar no aplicativo
# espera receber algum identificador da imagem/evento para registrar
@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        print(request.form)
        # Algumas validacoes (request.form ou request.args)
        if 'id_evento' not in request.form:
            return jsonify({'status':'400','msg': 'Evento nao encontrado no request!'}), 400
        if 'nome' not in request.form or 'tem_acesso' not in request.form:
            return jsonify({'status':'400','msg':'A pessoa esta faltando no request!'}), 400
        
        # Sanitizar a entrada
        id_evento_ent = int(request.form.get('id_evento'))
        nome_pessoa = escape(request.form.get('nome'))
        se_tem_acesso = (request.form.get('tem_acesso') == "True" or request.form.get('tem_acesso') == "true")

        # Chegou aqui tem o nome e o evento mas verificar se existem
        o_evento = db.get_or_404(Evento, id_evento_ent)
        
        # Entao o evento de fato existe e podemos associa-lo a pessoa
        # Mas e se a Pessoa ja existir?
        # O fetchone retorna exatamente UMA linha OU None
        stmt = db.select(Pessoa).where(Pessoa.nome == nome_pessoa)
        ja_existe = db.session.execute(stmt).fetchone()

        if ja_existe is not None:
            return jsonify({'status':'400','msg': 'A pessoa informada ja existe!'}), 400
        
        
        # Cria e INSERT Pessoa se ela nao existir ainda
        a_pessoa = Pessoa(nome=nome_pessoa, tem_acesso=se_tem_acesso)
        db.session.add(a_pessoa)
        db.session.commit()
        
        # UPDATE Evento e flush no BD
        o_evento.pessoa_id = a_pessoa.id
        db.session.commit()
        
        # UPDATE Imagem e flush no BD
        imagem_evento = db.get_or_404(Imagem, o_evento.imagem_id)
        imagem_evento.pessoa_id = a_pessoa.id
        db.session.commit()

        return jsonify({'status': '200', 'msg': 'Pessoa registrada com sucesso!'}), 200

    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Rota para deletar pessoas por ID.
@app.route('/pessoas/deletar/<id>', methods=['DELETE'])
def pessoas_deletar(id):
    try:
        a_pessoa = db.get_or_404(Pessoa, id)
        db.session.delete(a_pessoa)
        db.session.commit()
        return jsonify({'status':'200','msg':'Ok'}), 200
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

@app.route('/pessoas/up/<id>', methods=['PUT'])
def pessoas_up(id):
    try:
        a_pessoa = db.get_or_404(Pessoa, id)

        # Algumas validacoes (request.form ou request.args)
        if 'nome' not in request.form or 'tem_acesso' not in request.form:
            return jsonify({'status':'400','msg':'A pessoa esta faltando no request!'}), 400
        
        nome_pessoa = escape(request.form.get('nome'))
        se_tem_acesso = (request.form.get('tem_acesso') == 'True' or request.form.get('tem_acesso') == 'true')
        
        a_pessoa.nome = nome_pessoa
        a_pessoa.tem_acesso = se_tem_acesso


        db.session.commit()
        return jsonify({'status':'200','msg':'Ok'}), 200
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Esse endpoint retorna uma lista de pessoas
@app.route('/pessoas', methods=['GET'])
def pessoas_index():
    try:
        pessoas = db.session.execute(db.select(Pessoa).order_by(Pessoa.nome)).scalars()
        pessoas_list = [{'id': pessoa.id, 'nome': pessoa.nome, 'tem_acesso': pessoa.tem_acesso} for pessoa in pessoas]
        return jsonify({'status': '200', 'data': pessoas_list}), 200
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Esse endpoint retorna uma lista de eventos que contem tambem o caminho de cada imagem respectiva
@app.route('/eventos', methods=['GET'])
def evento_index():
    try:
        # Traz os eventos do BD
        #stmt = db.select(Evento, Imagem.photo_path).join(Evento.imagem).order_by(Evento.data)
        stmt = db.select(Evento, Imagem.photo_path, Pessoa.nome, Pessoa.tem_acesso).join(Evento.imagem).join(Evento.pessoa).order_by(Evento.data)
        # OBS ISSO PODE CAUSAR N+1 QUERIES
        events = db.session.execute(stmt).scalars()

        # Queremos entregar o Evento junto com sua Imagem correspondente
        result = [{"id_evento": event.id_evento,"data": event.data, "descricao": event.descricao, "pessoa_id": event.pessoa_id, "imagem_id": event.imagem_id, "nome": event.pessoa.nome, "tem_acesso": event.pessoa.tem_acesso, "photo_path": normalizar_path(event.imagem.photo_path)} for event in events]
        
        return jsonify({'status': '200', 'data': result}), 200
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Esse endpoint retorna todas imagens usando a ORM do SQLAlchemy
@app.route('/capturas', methods=['GET'])
def imagem_index():
    try:
        # Traz as Imagens do BD, outra forma de trazer que nao eh a session.execute tb funciona
        photos = Imagem.query.all()

        # So converte pra um array com chaves string pra poder jsonificar
        photo_links = [{"id_img": photo.id_img,"photo_path": normalizar_path(photo.photo_path), "pessoa_id": photo.pessoa_id, "timestamp": photo.timestamp} for photo in photos]

        return jsonify({"status":"200","data": photo_links})
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Esse endpoint simplesmente retorna se uma Pessoa do id tem acesso
@app.route('/api/temacesso/<id>', methods=['GET'])
def pessoa_acesso(id):
    try:
        quem = db.get_or_404(Pessoa, id)
        return jsonify({'status':'200','data': quem.tem_acesso})
    except Exception as e:
        return jsonify({'status': '500', 'msg': str(e)}), 500

# Esse endpoint serve a imagem em url
@app.route('/api/i/<name>', methods=['GET'])
def download_file(name):
    criar_diretorio()
    upload_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    print("Tentando baixar de " + upload_dir)
    return send_from_directory(upload_dir, name)

# METODOS EXTERNOS
# Isso trata do reconhecimento facial e chama do modulo facialreq.py
# Retorna o id da Pessoa se encontrar correspondencia e se nao retorna None
def usar_facerec(alvo):
    try:
        # Queremos rodar por todas tuplas de Imagem ate encontrar um correspondente
        as_imagens = Imagem.query.all()
        
        for imagem in as_imagens:
            if imagem.pessoa_id is not None:
                if reconhecimento(imagem.photo_path,alvo) == True:
                    # Se isso aconteceu ele esta no banco de dados
                    resultado = db.get_or_404(Pessoa, imagem.pessoa_id)
                    print(f"Encontrado: {resultado.id}")
                    return resultado.id
        return None
    except Exception as somee:
        print("Erro na funcao usar_facerec = ")
        print(somee)
        return None


# FUNCOES AUXILIARES
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Gera o URL de imagens para serem usadas em tags img no html
def normalizar_path(caminho):
    directory, filename = os.path.split(caminho)
    print(f"Tentando normalizar de {caminho} para {directory} e nome {filename}")
    return url_for("download_file",name=filename)

# Isso aqui so verifica se o diretorio onde vou salvar ja existe ou nao
def criar_diretorio():
    try:
        expected_folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
        os.makedirs(expected_folder, exist_ok=True)
    except FileExistsError:
        print("O diretorio ja existia")
    