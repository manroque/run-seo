# RunSEO – Análise de SEO e ROI
RunSEO é uma aplicação web desenvolvida com Python e Flask para ajudar empresas a analisarem os resultados das estratégias de SEO (Search Engine Optimization) e calcular o ROI (Retorno sobre o Investimento).

# Funcionalidades
Cadastro e login de usuários
Upload de arquivos CSV com dados de SEO e desempenho
Dashboard com gráficos interativos (cliques, impressões, CTR, receita, etc.)
Cálculo automático de ROI

# Pré-requisitos
Antes de começar, você precisa ter instalado no seu computador:
Python 3.10 ou superior
Git (opcional, mas recomendado)

# Verificar se o Git está instalado:
    - Digite `git --version` no terminal (PowerShell ou Prompt de Comando).
    - Se der o mesmo erro, **você realmente não tem o Git instalado**.

# Instalar o Git:
- Acesse https://git-scm.com/downloads.
- Baixe e instale a versão para seu sistema operacional.
- **Importante:** Durante a instalação, aceite a opção de "Adicionar Git ao PATH" (é uma telinha com várias opções avançadas — escolha a padrão ou a recomendada).
- **Após a instalação:**
    - Feche o terminal/PowerShell.
    - Abra novamente.
    - Teste com: `git --version`.
    - Agora deve aparecer algo como `git version 2.43.0.windows.1` (ou similar).

# Instalar python 
Download pelo navegador
Se você quiser baixar e instalar via browser:

- Acesse https://www.python.org/downloads/.
- Clique no botão **Download Python 3.x.x**.
- Execute o instalador baixado.

Atenção visionária
SEMPRE marque a caixinha** "**Add Python 3.x to PATH**" antes de clicar em **Install Now**.
Se esquecer disso, a vida vai ficar um pouco mais difícil depois.

Forma "oficial" e segura: usando o **winget**

O `winget` é o **Gerenciador de Pacotes** oficial do Windows, tipo um "apt-get" para Windows.
Digite:

- Se pedir confirmação, digite `Y` e pressione `Enter`.
- Se o `winget` não funcionar, veja a dica bônus no final.

# Passo a passo para rodar o projeto na sua máquina local
1. Clone o repositório
Se você tem Git instalado, abra o terminal e digite:

git clone https://github.com/manroque/run-seo
cd runseo
Ou baixe o código como ZIP e extraia os arquivos.

2. Instale o Python (caso ainda não tenha)
Acesse: https://www.python.org/downloads/
Baixe a versão Python 3.10 ou superior
Durante a instalação, marque a opção "Add Python to PATH"
Para verificar se está tudo certo, digite no terminal:

python --version

3. Crie e ative um ambiente virtual (opcional, mas recomendado), digite no terminal
    
python -m venv venv

# Ativar no Windows: 
venv\Scripts\activate
# Ativar no Mac/Linux:
source venv/bin/activate

4. Instale as bibliotecas necessárias
Certifique-se de estar na pasta do projeto e digite:

pip install -r requirements.txt

6. Crie o banco de dados (apenas na primeira vez)
Abra o terminal Python:

python

Dentro do terminal interativo, digite:

from app import db
db.create_all()
exit()

⚠️ Se a pasta instance/ não existir, crie uma manualmente no mesmo nível de app.py.

6. Rode o sistema localmente
Com tudo pronto, execute:

python app.py

Você verá algo como:
 * Running on http://127.0.0.1:5000/
   
Abra o navegador e acesse:
http://127.0.0.1:5000/

Requisitos do sistema
Certifique-se de que seu sistema possui:
Python	3.10
Pip	21.0
Navegador	Chrome / Edge / Firefox (moderno)
Problemas comuns e como resolver

Sinta-se à vontade para enviar melhorias, abrir issues ou sugerir novas funcionalidades!


Licença
Este projeto foi desenvolvido para fins educacionais no Projeto Integrador da UNIVESP.
Você pode usar, modificar e adaptar livremente com créditos ao autor.



