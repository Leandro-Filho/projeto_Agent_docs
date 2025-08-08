#importar a url que iremos pegar será fundamental para que o agente saiba o contexto de sua resposta 
import os

from dotenv import load_dotenv
load_dotenv()

from scrapper import get_all_text_from_url 
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent

def get_reponse_from_openai(message):

    llm = ChatOpenAI(model_name="gpt-3.5-tubro")

    response = llm.invoke(message)

    return response


#esse @tool vai fazer com que cada função que tiver @tool em cima, vira uma ferramenta para os agentes usarem
@tool 
#aqui fizemos uma função com um prompt responsável por colocar como parâmentro a url e a pergunta que o usuário irá fazer, além disso, o prompt avisa que irá receber uma documnetação de uma certa url e juntamnete uma pergunta sobre ela
def documentacion_tool(url: str, question: str) -> str:
    """This tool will receive as input a URL about a documentation and also a question about that documentation in which the user wants to be answered."""


    #como dito, dareemos um contexto para o HumanMessage. Fizemos a importação da função e colocamos a url da documentação como parâmetro.
    context = get_all_text_from_url(url)

    #será feito os prompts para: a resposta seja levada para algo mais técnica por falar que são documentações de programação, mesmo sendo o mais simples possivel. Além disso, um prompt feito para que seja lido e interpretado tanto a url quanto a pergunta feita, fazendo com que o agente interligue a pergunta com o conteúdo da url
    messages = [
        SystemMessage(content="You're a helpful programming assistant that must explain programming library documentation to users as simples as possible"),
        HumanMessage(content=f"Documentation: {context}\n\n {question}")
    ]

    #aqui será responsável por mostrar para o gpt-3.5-turbo que tem que responder de acordo com a mensagem acima
    response = get_reponse_from_openai(messages)

    return response
@tool
#Essa função irá formatar o arquivo em python. A importância desse aqui é formatar os caminhos e criar uma padronização para que rode em todos os sistemas operacionais, segurança e reuso do código
def black_formatter(path: str) -> str:
    """This tool receives as input a file of system path to a python script file and runs black formatter to format the file's python code"""

    try:
        os.system("poetry run black {path}")
        return "Feito!"
    except:
        return "Não foi feito!"

#simplesmente aqui será onde ficará as 'ferramentas' para o agente 
toolkit = [documentacion_tool, black_formatter]

#criamos mais uma llm e colocamos temperatuara igual 0 para que não haja criatividade por parte das respostas, respotas mais concretas
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

prompts = ChatPromptTemplate.from_messages(
    [
        ("system", """
            You are a programming assitant. Use your tools to answer questions.
            If you do not have a toll to answe the question, say to.
         
            Return only the answers.
         """),
         MessagesPlaceholder("chat_history", optional=True),
         ("human", "{input}"),
         MessagesPlaceholder("agent_scratchpad"),
    ]
)

#aqui, só passamos e criamos o agente com tudo que ela precisa para performar 
agent = create_openai_tools_agent(llm, toolkit, prompts)

agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)

result = agent_executor.invoke({"input": "Olá!"})

print(result["output"])