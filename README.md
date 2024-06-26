<h1 align="center">
  <a
    target="_blank"
    href="https://github.com/ivpinheiro/google-analytics-middleware"
  >
    <img
      align="center"
      alt="Google Analytics - Middleware"
      src="https://github.com/ivpinheiro/google-analytics-middleware/blob/main/frontend/src/assets/img/google-analytics.jpg"
    />
  </a>
</h1>

# Google Analytics - Middleware

O propósito deste repositório é simplificar o uso da API do Google Analytics. Com esse intuito, desenvolvemos um middleware que processa as requisições e retorna em um formato conveniente para Analistas de Dados.

## Pré-requisitos

Antes de compilar o projeto, é necessário criar um arquivo .env na raiz do mesmo. Este arquivo deve conter as chaves de uma conta de serviço do GCP que tenha os serviços do Google Analytics ativados. A variável de ambiente que deve receber a chave de acesso é a que segue abaixo:

  ```
  SERVICE_ACCOUNT_FILE
  ```

## Build do projeto

O projeto está contêinerizado e o processo de compilação da aplicação é simples. Para executar o projeto localmente, basta seguir os seguintes comandos:

  ```
  docker-compose up --build
  ```

## Documentação da API

A rota '[api/docs/](http://localhost/api/docs/)' disponibiliza o Swagger com exemplos de como utilizar o projeto.
