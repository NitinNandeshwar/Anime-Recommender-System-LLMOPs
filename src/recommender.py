from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self,retriever,api_key:str,model_name:str):
        self.llm = ChatGroq(model=model_name, api_key=api_key,temperature=0)
        self.prompt= get_anime_prompt()
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def get_recommendations(self, query: str):
        try:
            # result = self.qa_chain({"query": query})
            result = self.qa_chain.invoke({"query": query})
            return result['result']
        except Exception as e:
            print("Error while getting recommendations", e)

