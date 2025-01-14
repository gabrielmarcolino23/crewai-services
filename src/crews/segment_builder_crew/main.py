import sys
from segment_ai.crew import SegmentAiCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        "prompt": ""
    }
    SegmentAiCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "prompt": "Crie um segmento só de mulheres"
    }
    try:
        SegmentAiCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SegmentAiCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "prompt": "Crie um segmento só de mulheres"
    }
    try:
        SegmentAiCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
