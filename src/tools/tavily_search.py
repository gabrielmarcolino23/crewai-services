from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.tools.tavily_search import TavilySearchResults

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search"
    description: str = (
        "Uma ferramenta para buscar resultados no Tavily. Útil para obter informações atualizadas "
        "sobre tecnologia, mercado e tendências."
    )
    tool: TavilySearchResults = Field(default_factory=lambda: TavilySearchResults(k=3))

    def _run(self, query: str) -> str:
        try:
            return self.tool.run(query)  
        except Exception as e:
            return f"Erro ao executar a busca: {str(e)}"
        
