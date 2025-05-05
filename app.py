from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def get_cpu_launch_year(cpu_name: str) -> str:
    url_safe = cpu_name.lower().replace(" ", "+")
    url = f"https://www.techpowerup.com/cpu-specs/?q={url_safe}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Página não encontrada para {cpu_name}")

    soup = BeautifulSoup(response.text, 'html.parser')
    primeiro_item = soup.select_one(".items-mobile--item")
    
    if not primeiro_item:
        raise HTTPException(status_code=404, detail=f"Processador {cpu_name} não encontrado.")

    ano = primeiro_item.select(".item-properties-row")[-1].find_all("span")[-1].text.split()[-1]
    return ano

@app.get("/buscar")
async def buscar(cpu_name: str):
    try:
        year = get_cpu_launch_year(cpu_name)
        return {"cpu_name": cpu_name, "launch_year": year}
    except HTTPException as e:
        raise e
