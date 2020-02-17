import requests
from fastapi import BackgroundTasks, APIRouter

router = APIRouter()

def write_notification(email: str, message=""):
    url = "https://tiki.vn/combo-may-doc-sach-kindle-paperwhite-gen-10-8gb-mau-den-va-bao-da-well-begun-hang-nhap-khau-p11217956.html?src=search&2hi=0&keyword=kindle&_lc=Vk4wMzkwMjQwMDM%3D"
    r = requests.get(url = url)
    
    data = r.text
    with open("scrape.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        content += data
        email_file.write(content)

@router.post("/scrape")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email="check", message="some notification")
    return {"message": "Notification sent in the background"}
