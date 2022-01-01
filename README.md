# Painel da Estação Meteorológica

Programa para administração da [Estação Meteorológica](https://estacao-ifrs.herokuapp.com/).
Oferece painel de amplo acesso aos dados climáticos e informações sobre os conteúdos ali postados.

### Para fazer uso do programa

É possível a sua utilização com o interpretador Python direto na máquina, [baixar os executáveis](https://github.com/luisdef/admin-estacao/releases), ou fazer a própria compilação do código na máquina.

É necessário estar dentro da pasta [`app`](https://github.com/luisdef/admin-estacao/tree/main/app) para realizar os comandos abaixo.
- Para rodar com o interpretador:
    ```bash
    python.exe run.py
    ```
    ou (para ambientes Linux):
    ```bash
    python3 run.py
    ```
- Para compilar o seu próprio executável (somente disponível para Windows, por enquanto):
    ```bash
    python.exe setup.py build
    ```
    Esse script irá compilar o código do programa e irá gerar um arquivo ZIP com o nome `Painel-Estação.zip`, o qual conterá os executáveis necessários para rodar o programa.

<ins>Observação:</ins> <span>Para rodar o programa e compilá-lo, é necessário o arquivo .env, que poderá ser acessado aqui: <a href="https://drive.google.com/drive/folders/19WiIqqZRgfHJs-nZdcB4cvmaPiXW7QUJ?usp=sharing">Google Drive</a>.</span>
