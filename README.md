<p align="center">Projeto IOT 2: Campainha Inteligente</p>

Alunos: Gabriel H, Arthur, Igor, Maicon.

## Como buildar (Flask)
1) Obter pacotes adicionais do pip
- pip install flask Flask-SQLAlchemy markupsafe flask-cors psycopg2-binary
- pip install dotenv
- pip install opencv-python numpy matplotlib
- pip install cmake dlib face-recoginition pytz

2) Renomear o .env.example para .env tendo as constantes para usar no codigo.

3) Rode o arquivo bash 'iniciar' ou execute o seguinte comando no terminal:
- cd src/app
- flask run


## Como buildar (Laravel)

1) Clonar o repositório local.
- Se usar XAMPP clone dentro da pasta web (ex: htdocs no XAMPP -> xampp/htdocs/).
- Clonar pra pasta "campainhaint" pra ter o mesmo nome do caminho usado.

2) Execute o XAMPP ou o mySQL.
- Se for pelo XAMPP é só abrir ele, se não for nenhum desses então vai ter que abrir manualmente o mySQL.
- O nome e senha usados pra acessar o mySQL devem ser os mesmos que estiverem no arquivo .env, a configuração padrão do XAMPP é root sem senha.

3) Edite o ".env.example" com o nome e senha do mySQL. Existem 3 campos que devem ser editados:
- DB_DATABASE é o nome do Esquema que terá que ser criado antes da migração.
- DB_USERNAME é o nome de usuário.
- DB_PASSWORD é a senha.
- Depois salve apenas como ".env".

4) Acesse "localhost/phpmyadmin" e entre com o nome de usuario que definiu (o padrao do XAMPP é root sem senha). Vá em importar na aba de cima e escolha o arquivo do dump do banco de dados. Desça a pagina e clique em importar.

5) Se não houver arquivo dump: No menu da esquerda crie um novo esquema com o nome do DB_DATABASE. Na pasta raiz clonada do repositório rode pelo terminal: "php artisan migrate --seed" com o mySQL aberto.

6) Se estiver usando XAMPP é possível já acessar o projeto pelo URL: "http://localhost/(nome_da_pasta_clonada)/public/" se não for
então é preciso executar "php artisan serve". Isso vai dar um link no terminal onde ficará hosteado localmente.

7) Para rodar o javascript e estilos abra outro terminal na raiz do projeto e rode "npm run dev". Depois disso estará tudo pronto.

## License

The Laravel framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
