@echo off
REM Isso acima faz ele nao replicar os comandos na tela
echo "========[ TRABALHO DE PROCESSAMENTO E ANALISE DE IMAGENS ]========="
echo "Iniciando..."
echo "Grupo: Gabriel H.B., Arthur S., Igor C. e Maicon G."
echo "Se nao existir, altere os SET abaixo no .bat:"

REM Altere abaixo com o caminho absoluto do php.exe
set CAMINHO_PYTHON=pip

where /q python
IF %ERRORLEVEL% NEQ 0 (
	echo "Python nao foi encontrado, instale o Python PIP e altere o batch ou"
	echo "adicione o caminho ao PIP no PATH do sistema"
	pause
	exit /b 1
)ELSE (
	echo "Python detectado com sucesso"
)
where /q pip
IF %ERRORLEVEL% NEQ 0 (
	echo "Python nao foi encontrado, instale o Python PIP e altere o batch ou"
	echo "adicione o caminho ao PIP no PATH do sistema"
	pause
	exit /b 1
)ELSE (
	echo "Python detectado com sucesso"
)

echo "Vamos abrir o servidor pelo Flask"
cd ".\src"
REM flask run -h 192.168.0.35
echo "Comando: flask run -h 192.168.0.35"
REM cmd /k "flask run -h 192.168.0.35"
flask run -h 192.168.0.35
