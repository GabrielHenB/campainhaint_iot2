@echo off
REM Isso acima faz ele nao replicar os comandos na tela
echo "========[ TRABALHO DE PROCESSAMENTO E ANALISE DE IMAGENS ]========="
echo "Iniciando..."
echo "Grupo: Gabriel H.B., Arthur S., Igor C. e Maicon G."
echo "Se nao existir, altere os SET abaixo no .bat:"

REM Altere abaixo com o caminho absoluto do php.exe
set CAMINHO_PYTHON=node

where /q node
IF %ERRORLEVEL% NEQ 0 (
	echo "NodeJS nao foi encontrado, instale o NodeJS e altere o batch ou"
	echo "adicione o caminho ao node no PATH do sistema"
	pause
	exit /b 1
)ELSE (
	echo "NodeJS detectado com sucesso"
)
where /q npm
IF %ERRORLEVEL% NEQ 0 (
	echo "NPM nao foi encontrado, instale o NPM e altere o batch ou"
	echo "adicione o caminho ao NPM no PATH do sistema"
	pause
	exit /b 1
)ELSE (
	echo "NPM detectado com sucesso"
)

echo "Vamos abrir o app pelo Vite"
cd ".\web"
REM npm run dev
echo "Comando: npm run dev"
cmd /k "npm run dev"
