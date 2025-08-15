from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY,MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger=get_logger(__name__)

class AnimeRecommenderPipeline:
    def __init__(self,persist_dir= "chroma_db"):

        try:
            logger.info("Initializing Anime Recommender Pipeline")

            vector_builder = VectorStoreBuilder(csv_path='',perist_dir=persist_dir)
            retriever = vector_builder.load_vector_store().as_retriever()

            self.recommender= AnimeRecommender(retriever,GROQ_API_KEY,MODEL_NAME)

            logger.info("Anime Recommender Pipeline initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to intialize pipeline {str(e)}")
            raise CustomException("Error during pipeline intialization" , e)

    def recommend(self, query: str) -> str:
        try:
            logger.info(f"Received a query: {query}")
            recommendations = self.recommender.get_recommendations(query)
            logger.info("Recommendations generated successfully")
            return recommendations
        except Exception as e:
            logger.error(f"Failed to get recommendations: {str(e)}")
            raise CustomException("Error while getting recommendations", e)
        

def main():
    try:
        pipeline = AnimeRecommenderPipeline()
        query = "What are some good anime recommendations?"
        recommendations = pipeline.recommend(query)
        print(recommendations)
        logger.info("Recommendations printed successfully")
    except CustomException as ce:
        logger.error(f"Custom Exception: {ce}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")  

if __name__ == "__main__":
    main()