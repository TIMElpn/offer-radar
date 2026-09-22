import requests

# 三引号可以直接包裹多行文本，不需要管什么双引号转义
raw_jd = """岗位职责:参与AIAgent及Multi-Agent应用的设计、搭建、测试与优化;根据业务场景进行Prompt编写、调优及效果评估;参与Agent工作流、任务拆解、角色协作及工具调用设计;编写和维护AISkills及Agent Skills, 沉淀可复用的能力模块与最佳实践;参与知识库/RAG应用建设及检索效果优化;使用Python开发辅助工具, 完成API调用、数据处理及系统集成;协助排查Agent、Workflow、Prompt、RAG等环节的问题并持续优化;跟进Agent、Multi-Agent等AI应用技术, 完成相关技术调研和文档沉淀。学历要求: 本科及以上。"""

url = "http://127.0.0.1:8001/analyze"

# requests 库会自动帮你把 raw_jd 转成合法的 JSON
resp = requests.post(url, json={"jd_text": raw_jd})

print(f"状态码: {resp.status_code}")
print("解析结果：")
print(resp.json())