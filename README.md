# 📊 RunSEO – Análise de SEO e ROI

**RunSEO** é uma aplicação web desenvolvida com Python e Flask que ajuda empresas e profissionais de marketing a analisarem o desempenho de estratégias de SEO e calcularem automaticamente o ROI (Retorno sobre o Investimento).

---

## 🚀 Funcionalidades

- ✅ Cadastro e login de usuários
- 📂 Upload de arquivos CSV com dados do Google Search Console e GA4
- 📊 Dashboard com métricas como cliques, impressões, CTR, posição média, sessõesconversões e receita
- 💰 Cálculo automático de ROI e ticket médio

---

## 🧩 Tecnologias Utilizadas

- Python 3.10+
- Flask
- SQLAlchemy
- Flask-Login
- Pandas
- Gunicorn (para deploy em produção)
- Railway (hospedagem)

---

## 🖥️ Pré-requisitos

Antes de rodar o projeto, verifique se você possui:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) (opcional, mas recomendado)

### 📦 Instalação do Python (Windows)

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe a versão recomendada (Python 3.10 ou superior)
3. Marque **"Add Python to PATH"** antes de clicar em *Install Now*

### 🛠 Verifique a instalação

```bash
python --version
pip --version
```

---

## ⚙️ Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/manroque/run-seo
cd run-seo
```

Ou baixe o código como ZIP e extraia os arquivos.

### 2. Crie um ambiente virtual (recomendado não obrigatório)

```bash
python -m venv venv
```

- No **Windows**:
    
    ```bash
    venv\Scripts\activate
    ```
    

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

O banco será criado automaticamente ao iniciar o app. Certifique-se de que a pasta `instance/` exista:

```bash
mkdir instance

```

Ou crie manualmente no mesmo nível de `app.py`.

---

## ▶️ Executando a aplicação

```bash
python app.py
```

Abra o navegador e acesse: [http://127.0.0.1:8080](http://127.0.0.1:8080/)

---

## 📄 Modelo de CSV

Você pode fazer o upload de arquivos CSV com colunas como:

- `Impressões`, `Cliques`, `CTR`, `Posição Média`
- `Novos Usuários`, `Sessões`, `Conversões`
- `Receita`, `Ticket Médio`, `Taxa de Conversão`
- `Dispositivo`, `URL`, `Palavras-chave`, `Origem/Mídia`

| Coluna | Tipo |
| --- | --- |
| data | `YYYY-MM-DD` |
| cliques | Inteiro |
| impressões | Inteiro |
| ctr | Percentual (float) |
| posicao_media | Float |
| dispositivo | desktop / mobile / tablet |
| url | String |
| keywords | String |
| novos_usuarios | Inteiro |
| sessoes | Inteiro |
| transacoes | Inteiro |
| receita | Float |
| taxa_conversao | Percentual (float) |
| ticket_medio | Float |
| origem_midia | String |

📥 [Baixe o modelo de CSV aqui](https://drive.google.com/file/d/1xK90cpN-1i6cNGqRl6BEuviOF3pdA4U2/view?usp=sharing)

---

## 💻 Requisitos do sistema

- Python 3.10+
- Pip 21+
- Navegador moderno (Chrome, Edge ou Firefox)

---

## 🛠 Problemas comuns

- ❌ *Erro ao subir o app?* Verifique se você ativou o ambiente virtual e instalou as dependências corretamente.
- ❌ *Template não encontrado?* Confirme se a pasta `templates/` está presente e contém os arquivos `.html`.
- ❌ **`ModuleNotFoundError`** ao rodar o app → verifique se o ambiente virtual está ativado
- ❌ **Erro 502 no Railway** → certifique-se de usar `gunicorn` e bind na porta `0.0.0.0:$PORT`
- 📂 **Banco de dados não criado** → execute `db.create_all()` no terminal Python

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

- Criar issues com sugestões ou bugs
- Fazer um fork e enviar pull requests

---

## 📜 Licença

Este projeto foi desenvolvido para fins educacionais no **Projeto Integrador da [UNIVESP](https://univesp.br/)**.

Você pode usar, modificar e redistribuir livremente com os devidos créditos.
