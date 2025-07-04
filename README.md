# Coordenograma Estudo MT

## 🔨 Funcionalidades do projeto
- Autenticar usuários
- Ler a Planilha Google do usuário logado
- Pegar os valores da aba Grafico e Curvas_fusíveis
- Plotar um gráfico de escala logarítmica (Coordenograma)
- Upar o gráfico em jpeg no Google Drive

## ✔️ Técnicas e tecnologias utilizadas
- `Python`
- `Matplotlib`
- `Streamlit`
- `Custom TKInter`
- `PyInstaller`
- `API do Google Sheets`
- `API do Google Drive`

## 🛠️ Para abrir e rodar o projeto

### Lembre-se de ter seu arquivo de credenciais do Google na raiz do projeto

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Rodar Web (Streamlit):
```bash
streamlit run app_web.py
```

Rodar Local (CTK):
```bash
python app_local.py
```

Gerar Executável:
```bash
pyinstaller --onefile --windowed --name "ECS Procord Beta" app_local.py
pyinstaller --onefile --name "ECS Procord Beta (terminal)" app_local.py
```

## 💼 Setup para clientes
1. Criar a pasta ECS Procord Beta na máquina do cliente
2. Criar arquivo urls.txt com os IDs do arquivo e pasta
3. Pegar o executável da pasta dist e colocar na raiz da pasta do cliente
4. Criar a pasta auth dentro da pasta do cliente
5. Configurar a API do Google
6. Baixar o arquivo das credenciais e renomear como client_secrets.json
7. Colocar o arquivo client_secrets.json na pasta auth
8. Dar 2 cliques no executável
9. Autorizar script com a conta google que criou as credenciais
