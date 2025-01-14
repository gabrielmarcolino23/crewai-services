from src.crews.copy_wpp_crew.crew import CopywhatsappCrew
from src.crews.copy_sms_crew.crew import CopySmsCrew
from src.crews.segment_builder_crew.crew import SegmentAiCrew
from src.inputs.campaing import CampaingInputs
from fastapi.encoders import jsonable_encoder
import asyncio
from datetime import datetime


class CampaingFlow:
    def __init__(self):
        self.copy_wpp_crew = CopywhatsappCrew()
        self.copy_sms_crew = CopySmsCrew()
        self.segment_builder_crew = SegmentAiCrew()

    async def execute_campaign(self, req: CampaingInputs):
        tipo_campanha = req.tipo_campanha
        inputs = req.inputs.model_dump()

        if tipo_campanha.lower() == "wpp":
            copy_job = self.copy_wpp_crew.crew().kickoff_async(inputs=inputs)
        elif tipo_campanha.lower() == "sms":
            copy_job = self.copy_sms_crew.crew().kickoff_async(inputs=inputs)
        else:
            raise ValueError("Tipo de campanha inválido. Escolha entre 'WhatsApp' ou 'SMS'.")

        publico_alvo = inputs["publico_alvo"]

        if isinstance(publico_alvo, str):
            publico_alvo = {"prompt": publico_alvo}

        segment_job = self.segment_builder_crew.crew().kickoff_async(inputs={"prompt": publico_alvo, "data_atual": datetime.now()})

        results = await asyncio.gather(copy_job, segment_job)
        
        copy_output = results[0]
        segment_output = results[1]

        copy_output = copy_output.raw
        segment_output = segment_output.raw

        return {
            "copy_output": copy_output,
            "segment_output": segment_output
        }
