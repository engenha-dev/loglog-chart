# Coordenograma Web

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
- `API do Google Sheets`
- `API do Google Drive`

## 🛠️ Para abrir e rodar o projeto

### Lembre-se de ter seu arquivo de credenciais do Google na raiz do projeto

```bash
python3 -m venv .venv #Windows: python -m venv .venv
```

```bash
source .venv/bin/activate #Windows: .venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```