#type:ignore
from agents import Runner,set_tracing_disabled
import re # to chose keyword user query
import request
set_tracing_disabled(True)




def search_product(keyword:str)-> str:
    try:
        url = "https://hackathon-apis.vercel.app/api/products"
        response = request.get(url)
        response.raise_for_status()
        products = response.json()

        words = re.findall(r"b\w\b", keyword.lower())
        stopwords = {"the","with", "under", "above", "for", "of", "and", "or"}
        keywords = [w for w in words if w not in stopwords]

        filtered = []
        for p in products:
            





res = Runner.run_sync(
    starting_agent=agent,
    input="what is 2+2?"
)
print(res.final_output)