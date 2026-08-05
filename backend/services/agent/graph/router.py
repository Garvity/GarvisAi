from config.llm_models import get_model


async def router(state):
    file = state.get("file")
    if file and file.get("mimetype") == "application/pdf":
        return {**state, "agent": "pdfRag"}
    if file and file.get("mimetype", "").startswith("image/"):
        return {**state, "agent": "imageAnalyzer"}
    if state.get("agent") and state.get("agent") != "auto":
        return {**state, "agent": state["agent"]}

    llm = await get_model("router")
    prompt = f"""You are an agent router.

Available agents:
- chat
- search
- coding
- pdf
- ppt
- image

Rules:
chat:
General conversation,
explanations,
Learning,
questions.

search:
Current events,
latest information,
news,
recent developments,
internet lookup.

coding:
Generate code,
debug code,
build projects,
architecture,
API design.

pdf:
Questions about generate PDFs or document context.

ppt:
Questions about generate ppts or ppt context.

image:
Use whenever the user wants an image to be created or modified.
image Tasks include:
Generate images
Illustrations
Logos
Posters
Diagrams
Icons
Infographics
Image editing
Image enhancement
Style transfer
Character design
Concept art

Return ONLY one word:
chat
search
coding
pdf
ppt
image

User Query: {state.get("prompt")}
    """

    response = await llm.ainvoke(prompt)
    print("router agent response", response.content.strip().lower())
    return {**state, "agent": response.content.strip().lower()}
