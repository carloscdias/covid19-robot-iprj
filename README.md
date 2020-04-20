# covid19-robot-iprj
covid19-robot-iprj

O objetivo deste projeto é buscar e organizar/agrupar informações sobre publicações contendo decisões/experiências/soluções ligadas à COVID-19.

## Execução

1. Instalação das dependências
    ```
    $ pip install -r requirements.txt
    ```
2. Criação do banco de dados. O comando analisa se foram feitas mudanças nos modelos e cria novas migrações
    ```
    $ make django-migrations
    ```
3. Aplicação das mudanças ao banco de dados
    ```
    $ make django-migrate
    ```
4. Scrapping
    ```
    $ make scrapy-run
    ```
5. Executar
    ```
    $ make django-run
    ```

O acesso é feito pelo localhost no browser.