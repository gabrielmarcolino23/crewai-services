import sys
from copysms.crew import CopySmsCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'objetivo_copy': 'Divulgar a promoção de 50% de desconto em itens selecionados da coleção de verão.',
        'tom_de_voz': 'Cativante',
        'publico_alvo': 'Clientes que compraram na última estação e têm interesse em moda e tendências.'
    }
    CopySmsCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'objetivo_copy': 'Divulgar a promoção de 50% de desconto em itens selecionados da coleção de verão.',
        'tom_de_voz': 'Cativante',
        'publico_alvo': 'Clientes que compraram na última estação e têm interesse em moda e tendências.'
    }

    try:
        CopySmsCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CopySmsCrew().crew().replay(task_id=sys.argv[1])

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
        CopySmsCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
