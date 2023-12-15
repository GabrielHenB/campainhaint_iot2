from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from markupsafe import escape
from flask_cors import CORS
import os
import datetime
import pytz
import random

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
        db.session.add(Pessoa(id=0,nome='desconhecido',tem_acesso=False))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/uploadesp', methods=['POST'])
def special_store():
    try:
        image_raw_bytes = request.get_data()  #get the whole body

        if image_raw_bytes is None:
            return jsonify({'status': '400','msg': 'Request vazio!'}), 400

        # renomeia
        resposta = image_raw_bytes

        # Salva a imagem usando o caminho atual (src) e o configurado para a pasta das imagens com o nome
        criar_diretorio()
        random_filename = ''.join(random.choice('0123456789') for _ in range(6))+'.jpg'
        caminho_salvar = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], random_filename)
        print(f"debug: O nome do arquivo eh {random_filename} com o caminho {caminho_salvar}")
        #resposta.save(caminho_salvar)
        f = open(caminho_salvar, 'wb') # wb for write byte data in the file instead of string
        f.write(image_raw_bytes) #write the bytes from the request body to the file
        f.close()

        # Realizar reconhecimento facial e obter resposta ID da Pessoa ou None
        id_reconhecido = usar_facerec(caminho_salvar)
        
        # Bom se for None ele avisa mas internamente toda Imagem com pessoa_id None eh considerada Desconhecido
        if id_reconhecido is None:
            id_reconhecido = 0
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
        

        return jsonify({"status":"200","msg": "A imagem foi salva com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({'status': '500','msg': str(e)}), 500

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
            return jsonify({'status': '400','msg': 'Request vazio!'}), 400
        
        # Assuming the photo is sent in the request body
        resposta = request.files['imagem']
        
        # Valida se tem arquivo e se a extensao eh permitida. O backend nao aceita outras extensoes. Poderia validar tamanho tambem.
        if resposta.filename == '':
            return jsonify({'status':'400','msg': 'Request sem imagem!'}), 400

        if not (allowed_file(resposta.filename)):
            return jsonify({'status':'400','msg': 'Tipo invalido de arquivo. Deve ser png, jpg, jpeg'}), 400
        
        # Usa o helper de sanitizar nomes de arquivos do werkzeug. Talvez depois mudar para outro esquema.
        nome_seguro = secure_filename(resposta.filename)

        # Salva a imagem usando o caminho atual (src) e o configurado para a pasta das imagens com o nome
        criar_diretorio()
        caminho_salvar = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], nome_seguro)
        resposta.save(caminho_salvar)

        # Realizar reconhecimento facial e obter resposta ID da Pessoa ou None
        id_reconhecido = usar_facerec(caminho_salvar)
        
        # Bom se for None ele avisa mas internamente toda Imagem com pessoa_id None eh considerada Desconhecido
        if id_reconhecido is None:
            id_reconhecido = 0
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

        if ja_existe is not None and nome_pessoa != "desconhecido":
            # Portanto a pessoa ja esta no bd e estamos tentando identificar
            # Devemos atribuir entao o novo nome e identificacao a pessoa!
            a_pessoa = db.session.execute(stmt).scalar_one()
            a_pessoa.tem_acesso = se_tem_acesso
            print("A pessoa ja existia e vamos associar seu id ao evento apenas!")
            #return jsonify({'status':'400','msg': 'A pessoa informada ja existe!'}), 400
        elif ja_existe is None and nome_pessoa != "desconhecido":
            # A pessoa nao existe e o nome nao eh desconhecido

            # Cria e INSERT Pessoa se ela nao existir ainda
            a_pessoa = Pessoa(nome=nome_pessoa, tem_acesso=se_tem_acesso)
            db.session.add(a_pessoa)
            db.session.commit()
        else:
            # A pessoa eh desconhecida
            a_pessoa = db.session.execute(stmt).scalar_one()
        
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
        result = [{"id_evento": event.id_evento,"data": fix_time(event.data), "descricao": event.descricao, "pessoa_id": event.pessoa_id, "imagem_id": event.imagem_id, "nome": event.pessoa.nome, "tem_acesso": event.pessoa.tem_acesso, "photo_path": normalizar_path(event.imagem.photo_path)} for event in events]
        
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
        print("Usando o seguinte caminho {}".format(alvo))
        # Queremos rodar por todas tuplas de Imagem ate encontrar um correspondente
        as_imagens = Imagem.query.all()
        
        for imagem in as_imagens:
            if imagem.pessoa_id is not None:
                if reconhecimento(imagem.photo_path,alvo) == True:
                    print("Tentando reconhecer")
                    # Se isso aconteceu ele esta no banco de dados
                    #stmt = db.select(Pessoa).where(id == imagem.pessoa_id)
                    #resultado = db.session.execute(stmt).scalars()[0]
                    #resultado = db.one_or_404(Pessoa, imagem.pessoa_id)
                    teste = imagem.pessoa_id
                    #resultado = db.first_or_404(Pessoa, teste)
                    resultado = Pessoa.query.filter_by(id=teste).first_or_404()
                    print(f"Encontrado: {resultado.id}")
                    return resultado.id
        print("Nao foi possivel reconhecer retornando None")
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

def fix_time(data):
    # Convert the string to a datetime object
    datetime_object = data

    # Assume the original datetime is in UTC (adjust the timezone accordingly if it's different)
    utc_timezone = pytz.timezone('UTC')
    datetime_object_utc = utc_timezone.localize(datetime_object)

    # Convert to 'America/Sao_Paulo' timezone
    saopaulo_timezone = pytz.timezone('America/Sao_Paulo')
    datetime_object_saopaulo = datetime_object_utc.astimezone(saopaulo_timezone)

    print("A NOVA DATA EH = {}".format(datetime_object_saopaulo))
    return datetime_object_saopaulo.strftime('%d/%m/%Y às %H:%M:%S')
    