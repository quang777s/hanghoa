import aiohttp
import asyncio
from fastapi import BackgroundTasks, APIRouter
from bs4 import BeautifulSoup

router = APIRouter()

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def soup_a_page(url: str):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return BeautifulSoup(html, 'html.parser')

async def scrape_detail_page(url: str):
    soup = await soup_a_page(url)
    title = soup.h1.getText().strip()
    price = soup.select('#span-price')[0].getText().strip()
    
    with open("scrape_detail_page-page.txt", mode="w") as email_file:
        content = title + '\n'
        content += price
        email_file.write(content)

async def scrape_search_page(urls: list):
    content = ""
    for url in urls:
        soup = await soup_a_page(url)
        titles = soup.select('a.search-a-product-item')
        prices = soup.select('span.final-price')
        for i in range(len(titles)):
            content += titles[i].get('title') + " " + prices[i].findAll(text=True, recursive=False)[0].strip() + '\n'
    
    with open("scrape_search_page.txt", mode="w") as text_file:
        text_file.write(content)

@router.post("/scrape")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_detail_page, url="https://tiki.vn/combo-may-doc-sach-kindle-paperwhite-gen-10-8gb-mau-den-va-bao-da-well-begun-hang-nhap-khau-p11217956.html?src=search&2hi=0&keyword=kindle&_lc=Vk4wMzkwMjQwMDM%3D")
    return {"message": "Notification sent in the background"}

@router.post("/scrape-search-page")
async def route_scrape_search_page(background_tasks: BackgroundTasks):
    urls = [
        "https://tiki.vn/search?q=iphone&_lc=Vk4wMzkwMjQwMDM%3D",
        "https://tiki.vn/search?q=kindle&_lc=Vk4wMzkwMjQwMDM%3D",
        "https://tiki.vn/search?q=macbook&_lc=Vk4wMzkwMjQwMDM%3D"
    ]
    background_tasks.add_task(
        scrape_search_page,
        urls=urls
        )
    return {"message": "search"}
