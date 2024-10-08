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
```

## 💼 Setup para clientes
1. Criar a pasta ECS Procord Beta na máquina do cliente
2. Pegar o executável da pasta dist e colocar na raiz da pasta do cliente
3. Criar a pasta auth dentro da pasta do cliente
4. Configurar a API do Google
5. Baixar o arquivo das credenciais e renomear como client_secrets.json
6. Colocar o arquivo client_secrets.json na pasta auth
7. Dar 2 cliques no executável
8. Autorizar script com a conta google que criou as credenciais