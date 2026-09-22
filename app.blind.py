#blind
import os
import json
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pydantic import BaseModel,ValidationError

load_dotenv(override=True)
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))
MODEL=os.getenv("MODEL_NAME")

#p2----
SYSTEM = (
    "你是 JD 解析器。从用户发来的职位描述原文中提取信息，只输出一个 JSON 对象。"
    "原文没有的信息填 null，列表没有内容填 []，禁止编造。"
)
SCHEMA = ('输出格式: {"position": "职位名称", "responsibilities": ["职责1","职责2"], '
          '"skills": ["技能1","技能2"], "education": "学历要求或null", '
          '"experience": "经验要求或null", "salary":"薪资条件或null",'
          '"summary": "一句话概括这个岗位要什么样的人"}')

class AnalyzeRequest(BaseModel):
    jd_text:str

class JdRequirements(BaseModel):        
    position: str | None                
    responsibilities: list[str]
    skills: list[str]
    education: str | None
    experience: str | None
    summary: str
    salary:str| None = None

app = FastAPI(title="OfferRadar V0")

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if len(req.jd_text.strip()) < 10:   # 最便宜的防御：太短的输入根本不配花钱
        return {"error": "JD 太短，至少给 10 个字"}

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"{req.jd_text}\n\n{SCHEMA}"},
    ]
    for attempt in range(1, 4):         # 重考最多 3 次
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,                              # 提取任务：要死板的准
            response_format={"type": "json_object"},    # 锁 JSON
        )
        try:
            data = json.loads(resp.choices[0].message.content)
            result = JdRequirements.model_validate(data)   
        except (json.JSONDecodeError, ValidationError):
            continue
        return result.model_dump()      # Pydantic 对象 → 字典 → FastAPI 变 JSON
    return {"error": "模型三次都没按格式来，稍后再试"}
