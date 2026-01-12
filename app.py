# Importa o Streamlit - framework para criar aplicações web interativas em Python
# Importa ChatGroq - classe que faz a conexão com a API da Groq para usar modelos de LLM
# Importa ChatPromptTemplate - classe para criar templates de prompts estruturados
# Importa StrOutputParser - parser que converte a resposta do modelo em string
# Importa load_dotenv - função que carrega variáveis de ambiente do arquivo .env
# Executa a função para carregar as variáveis do arquivo .env (como GROQ_API_KEY)
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

## === CONEXÃO COM A LLM === ##
id_model = "llama-3.3-70b-versatile" # Define o id da llm que será utilizada (Llama 3.3 70B Versatile) 
llm = ChatGroq(         # Cria a instância do ChatGroq com os parâmetros necessários
    model=id_model,     # Define o modelo a ser utilizado
    temperature=0.7,    # Controla temperatura/criatividade (0=conservador, 1=criativo)
    max_tokens=None,    # Número máximo de tokens na resposta (None=sem limite)
    timeout=None,       # Tempo máximo de espera (None=sem limite)
    max_retries=2,      # Número de tentativas em caso de erro
)

## === FUNÇÃO DE GERAÇÃO DE CONTEÚDO === ##
def llm_generate(llm, prompt):
  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
      ("human", "{prompt}"),
  ])

  chain = template | llm | StrOutputParser()
  # Cria uma cadeia (chain) que executa sequencialmente:
  # 1. template - formata o prompt
  # 2. llm - envia para o modelo e recebe resposta
  # 3. StrOutputParser - converte a resposta em string

  res = chain.invoke({"prompt": prompt})
  # Executa a cadeia passando o prompt como parâmetro
  return res
  # Retorna o texto gerado

## === INTERFACE COM STREAMLIT === ##
# Configuração das propriedades da página
st.set_page_config(page_title = "Gerador de conteúdo 🤖", page_icon="🤖")
st.title("Gerador de conteúdo")

# Campos do formulário
topic = st.text_input("Tema:", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")
platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])
#cta = st.checkbox("Incluir CTA")
cta = st.text_input("Chamada para Ação (CTA):", placeholder="Ex: Saiba mais, Inscreva-se, Compre agora...")
hashtags = st.checkbox("Retornar Hashtags")
keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")

## === PROCESSAMENTO E GERAÇÃO === ##
if st.button("Gerar conteúdo"):
  
  # Constrói o prompt final com todas as informações fornecidas pelo usuário
  prompt = f"""
  Escreva um texto com SEO otimizado sobre o tema '{topic}'.
  Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
  - Onde será publicado: {platform}.
  - Tom: {tone}.
  - Público-alvo: {audience}.
  - Comprimento: {length}.
  - {"Inclua ao final do texto esta cahamada para ação:" + cta if cta else "Não inclua chamada para ação"}
  - {"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."}
  {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""}
  """

# Bloco para capturar possíveis erros durante a geração
  try:
      res = llm_generate(llm, prompt)
      st.markdown(res)
  except Exception as e:
      st.error(f"Erro: {e}")