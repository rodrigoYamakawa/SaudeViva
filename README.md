# SaúdeViva - Prova de Conceito (PI - Segunda Etapa)

Esta é uma prova de conceito (PoC) do aplicativo SaúdeViva, desenvolvida como parte da segunda etapa do Projeto Integrador do curso de Tecnologia em Análise e Desenvolvimento de Sistemas / Sistemas para Internet.

## Justificativa da PoC

A jornada de João Carlos (45 anos, pré-diabético) foi escolhida para a Prova de Conceito (PoC) por focar em funcionalidades centrais e viáveis para demonstração: monitoramento de glicose e recomendações personalizadas (simuladas). Esta escolha permite ilustrar o valor do aplicativo "SaúdeViva" em ajudar usuários com condições específicas a gerenciar sua saúde proativamente, alinhando-se aos requisitos técnicos e de entrega da segunda etapa do Projeto Integrador.

## Integrante(s)

*   Rodrigo Yamakawa

## Tecnologias Utilizadas

*   **Frontend:** HTML, CSS (sem JavaScript adicional nesta PoC)
*   **Backend:** Flask (Python)
*   **Banco de Dados:** SQLite

## Funcionalidades Implementadas (PoC)

*   Registro de novos usuários.
*   Login de usuários existentes.
*   Dashboard para usuários logados.
*   Registro de níveis de glicose com data e hora.
*   Exibição do histórico de registros de glicose.
*   Exibição de dicas de saúde simuladas (aleatórias).
*   Logout.

**Observação:** A autenticação (verificação de senha) e o armazenamento de senhas são feitos em texto plano para simplificar a PoC. Em um ambiente de produção, é **essencial** usar hashing de senhas.

## Como Executar o Projeto

1.  **Pré-requisitos:**
    *   Python 3.11 ou superior instalado.
    *   Ambiente virtual (recomendado).

2.  **Instalação de Dependências:**
    *   Navegue até o diretório raiz do projeto (`/home/ubuntu/saudeviva_poc` neste ambiente, ou onde você descompactar o projeto).
    *   (Opcional, mas recomendado) Crie e ative um ambiente virtual:
        ```bash
        python3 -m venv venv
        source venv/bin/activate  # Linux/macOS
        # venv\Scripts\activate    # Windows
        ```
    *   Instale a única dependência externa (Flask já está pré-instalado no ambiente Manus):
        ```bash
        pip install Flask
        ```
        *(Se estiver fora do ambiente Manus, pode ser necessário instalar `sqlite3` separadamente, embora geralmente venha com Python)*

3.  **Execução:**
    *   Navegue até o diretório `src` dentro do projeto:
        ```bash
        cd src
        ```
    *   Execute o script principal do Flask:
        ```bash
        python main.py
        ```
    *   O aplicativo estará rodando em `http://127.0.0.1:5000` (ou `http://localhost:5000`). O banco de dados (`saudeviva.db`) e o arquivo de schema (`schema.sql`) serão criados automaticamente no primeiro acesso, se não existirem.

4.  **Acesso:**
    *   Abra seu navegador e acesse `http://127.0.0.1:5000`.
    *   Você será redirecionado para a página de login. Crie um novo usuário ou use um existente para acessar o dashboard.

