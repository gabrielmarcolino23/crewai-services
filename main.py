from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import uuid4
from dotenv import load_dotenv
import time
import jwt
import os
import json
from src.inputs.copy_input import Inputs, ReviewInputs, linkedinInputs
from src.inputs.segment_input import InputSegment
from src.inputs.campaing import CampaingInputs
from datetime import datetime

app = FastAPI()

load_dotenv()

# Configuração JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_SECRET_KEY_ALGORITHM")

if SECRET_KEY is None or ALGORITHM is None:
    raise ValueError("Auth credentials not found")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        email = payload.get("email")

        if role is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Role ou email não encontrados no token",
            )
        return {"role": role, "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )


@app.post("/generate/copy/whatsapp")
async def generate_copy(req: Inputs, current_user: dict = Depends(get_current_user)):
    try:
        start_time = time.time()
        from src.crews.copy_wpp_crew.crew import CopywhatsappCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        resultado_final = (
            await CopywhatsappCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "objetivo_copy": req.objetivo_copy,
                    "tom_de_voz": req.tom_de_voz,
                    "publico_alvo": req.publico_alvo,
                    "segmento_loja": req.segmento_loja.strip() if req.segmento_loja else "varejo",
                }
            )
        )

        copy_text = resultado_final.raw.replace("[", "{{").replace("]", "}}")

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "copy": copy_text,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post("/generate/copy/email")
async def generate_copy(req: Inputs, current_user: dict = Depends(get_current_user)):
    try:
        start_time = time.time()
        from src.crews.copy_email_crew.crew import CopyEmailCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        resultado_final = (
            await CopyEmailCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "objetivo_copy": req.objetivo_copy,
                    "tom_de_voz": req.tom_de_voz,
                    "publico_alvo": req.publico_alvo,
                    "segmento_loja": req.segmento_loja.strip() if req.segmento_loja else "varejo",
                }
            )
        )

        copy_text = resultado_final.raw.replace("[", "{{").replace("]", "}}")

        assunto = (
            json.loads(resultado_final.pydantic.model_dump_json())
            .get("assunto")
            .replace("[", "{{")
            .replace("]", "}}")
        )
        corpo_email = (
            json.loads(resultado_final.pydantic.model_dump_json())
            .get("corpo")
            .replace("[", "{{")
            .replace("]", "}}")
        )

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "assunto": assunto,
            "corpo_email": corpo_email,
            "copy": copy_text,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post("/generate/copy/email/test")
async def generate_copy(req: Inputs, current_user: dict = Depends(get_current_user)):
    try:
        start_time = time.time()
        from src.crews.copy_email_crew.crew import CopyEmailCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        (
            CopyEmailCrew()
            .crew()
            .test(
                n_iterations=3,
                inputs={
                    "objetivo_copy": req.objetivo_copy,
                    "tom_de_voz": req.tom_de_voz,
                    "publico_alvo": req.publico_alvo,
                },
                openai_model_name="gpt-4o-mini",
            )
        )

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}


@app.post("/generate/copy/sms")
async def generate_copy(req: Inputs, current_user: dict = Depends(get_current_user)):
    try:
        start_time = time.time()
        from src.crews.copy_sms_crew.crew import CopySmsCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        resultado_final = (
            await CopySmsCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "objetivo_copy": req.objetivo_copy,
                    "tom_de_voz": req.tom_de_voz,
                    "publico_alvo": req.publico_alvo,
                    "segmento_loja": req.segmento_loja.strip() if req.segmento_loja else "varejo",
                }
            )
        )

        copy_text = resultado_final.raw.replace("[", "{{").replace("]", "}}")

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "copy": copy_text,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/review/copy/whatsapp")
async def review_copy(
    req: ReviewInputs, current_user: dict = Depends(get_current_user)
):
    try:
        start_time = time.time()
        from src.crews.copy_wpp_reviewer_crew.crew import ReviewerwppCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        resultado_final = (
            await ReviewerwppCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "mensagem": req.mensagem,
                    "feedback": req.feedback,
                }
            )
        )

        copy_text = resultado_final.raw.replace("[", "{{").replace("]", "}}")

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "copy": copy_text,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/review/copy/sms")
async def review_copy(
    req: ReviewInputs, current_user: dict = Depends(get_current_user)
):
    try:
        start_time = time.time()
        from src.crews.copy_sms_reviewer_crew.crew import ReviewersmsCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        resultado_final = (
            await ReviewersmsCrew()
            .crew()
            .kickoff_async(
                inputs={
                    "mensagem": req.mensagem,
                    "feedback": req.feedback,
                }
            )
        )

        copy_text = resultado_final.raw.replace("[", "{{").replace("]", "}}")

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "copy": copy_text,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/generate/segment")
async def generate_segment(
    req: InputSegment, current_user: dict = Depends(get_current_user)
):
    try:
        start_time = time.time()
        from src.crews.segment_builder_crew.crew import SegmentAiCrew

        print(f"Usuário autenticado: {current_user.get('email')}")

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        crew_instance = SegmentAiCrew().crew()
        data_atual = datetime.now()

        result = await crew_instance.kickoff_async(inputs={"prompt": req.prompt, "data_atual": datetime.now()})

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "segment": result.raw,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate/campaign")
async def generate_campaign(
    req: CampaingInputs
):
    try:
        start_time = time.time()
        from src.flows.campaing_flow.main import CampaingFlow

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        service = CampaingFlow()

        result = await service.execute_campaign(req=req)

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "copy_output": result["copy_output"],
            "segment_output": result["segment_output"],
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/linkedin")
async def generate_linkedin(
    req: linkedinInputs
):
    try:
        start_time = time.time()
        from src.crews.linkedin_ale_crew.crew import LinkedinPostAle

        run_id = uuid4()
        print(f"Run ID: {run_id}")

        result = await LinkedinPostAle().crew().kickoff_async(inputs={
            "topic": req.topic,
        })

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "run_id": str(run_id),
            "linkedin_output": result.raw,
            "tempo_execucao": f"{execution_time}s",
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    print(">>>>>>>>>>>> version V0.0.1")
    uvicorn.run(app, host="0.0.0.0", port=8000)
