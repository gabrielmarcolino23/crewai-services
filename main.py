import os
from agents.copywriter_giftback import copywriter_giftback
from agents.copywriter_data_comemorativa import copywriter_data_comemorativa

# from utils.helper_functions import process_and_format_result
from dotenv import load_dotenv

load_dotenv()

from crewai import Crew, Process


os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Inputs do usuário ou de algum fluxo de dados
dados_cliente = {
    "nome_loja": "Vorr",
    "segmento": "moda feminina",
    "publico_alvo": "jovens adultas",
    "tom_voz": "amigável e próxima",
    "objetivo_campanha": "Envio de giftback com código e data de expiração resultante de uma compra",
    "tipo_campanha": "giftback",
    "data_comemorativa": "Dia das Mães",
}

# copywriter_agent, copywriter_task = copywriter_data_comemorativa()
copywriter_agent, copywriter_task = copywriter_giftback()
#   = copywriter_data_comemorativa()

crew = Crew(
    agents=[copywriter_agent],
    tasks=[copywriter_task],
    process=Process.sequential,
    verbose=True,
)

resultado_final = crew.kickoff(inputs=dados_cliente)

print(resultado_final)

"""
formatted_result = process_and_format_result(resultado_final, dados_cliente)
print(formatted_result)
"""
