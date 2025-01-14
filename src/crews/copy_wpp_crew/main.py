#!/usr/bin/env python
import sys
from copywhatsapp.crew import CopywhatsappCrew

from langtrace_python_sdk import langtrace

langtrace.init(api_key = 'bda7ffc02e8d1ed29c7c712892a6fdfa864bc520db6c1e70bec27329258ae921')

def run():
    """
    Run the crew.
    """
    inputs = {
        'objetivo_copy': 'Enviar um cupom de giftback para clientes.',
        'tom_de_voz': 'Cativante',
        'publico_alvo': 'consumidores preocupados com sustentabilidade e qualidade.'
    }
    
    result = CopywhatsappCrew().crew().kickoff(inputs=inputs)
    print(result)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'objetivo_copy': 'Enviar um cupom de giftback para clientes.',
        'tom_de_voz': 'Formal',
        'publico_alvo': 'Consumidores preocupados com sustentabilidade e qualidade.'
    }

    try:
        CopywhatsappCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CopywhatsappCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'objetivo_copy': 'Criar um copy para venda de curso de direito',
        'tom_de_voz': 'formal',
        'publico_alvo': 'estudantes de direito'
    }
    try:
        CopywhatsappCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
