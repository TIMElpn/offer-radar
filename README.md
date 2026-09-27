# 🎯 OfferRadar · 求职雷达

粘贴招聘 JD → AI 提取结构化岗位要求；再粘贴简历 → 输出匹配分 + 已满足/缺口清单。
一个为"AI 应用岗求职"而生的自研工具（顺便用它研究我自己要投的岗位）。

## 功能
| 版本 | 功能 | 接口 |
|---|---|---|
| V0 | JD 结构化解析（职位/职责/技能/学历/薪资/总评） | POST /analyze |
| V1 | 简历 × JD 匹配打分（0-100 + 绿卡已满足 + 红卡缺口） | POST /match |

## 架构与数据流
```
浏览器(原生HTML/JS, fetch+JSON.stringify)
  → FastAPI (Pydantic 校验请求, 422 挡在门外)
    → LLM (阿里云百炼 qwen)
      → 驯化三件套: response_format 锁JSON + Pydantic 验答卷 + 失败重试×3
        → JSON 原路返回 → 页面渲染
```

## 快速开始
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # 填入你的 API Key（推荐阿里云百炼）
uvicorn app:app --reload --port 8001              # 打开 http://127.0.0.1:8001
```

## 测试与评测（真实数据）
- **金标准集（3 份 AI 合成简历）**：满分候选人 95 / 半匹配 82 / 零匹配 5 —— 评分梯度判别力良好
- **对抗测试**：简历内埋四重提示注入（指令覆写 / 伪造JSON答案 / 情感胁迫 / 伪造总结），系统输出 5/100，攻击全部失效且未破坏输出格式
- **抽查纪律**：曾发现模型把示例简历的"计算机专业"安到别人头上——所有事实性输出必须抽查回原文

## 踩过的坑（都是真的）
- 401：系统残留旧 API Key 环境变量覆盖 .env → load_dotenv(override=True)
- 422：手贴 JSON 里的英文引号撞坏请求体 → 前端 JSON.stringify 根治
- JS 函数被贴进另一个函数肚子里 → onclick 全局找不到 → F12 Console 30 秒破案
- Field 用了没 import → uvicorn 崩了不弹窗 → 后端病看终端，前端病看 Console

## Roadmap
- [ ] V2 知识库问答（RAG：错题本/面试资料喂进去，回答带出处）
- [ ] V3 求职规划 Agent（Tool Calling + LangGraph）
- [ ] V4 工程化（日志/pytest/部署公网/可疑内容举报字段）
- [ ] V5 Multi-Agent 模拟面试间

> 作者背景：非科班本科生，全程手写+AI辅助，每个报错都追到根因。
