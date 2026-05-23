import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import os

# Supabase সেটআপ (এগুলো গিটহাব সিক্রেট থেকে আসবে)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def scrape_and_push():
    target_url = "https://www.startech.com.bd/laptop-notebook/laptop"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    items = soup.find_all('div', class_='p-item')

    for item in items:
        name = item.find('h4', class_='p-item-name').text.strip()
        price_text = item.find('div', class_='p-item-price').span.text.strip()
        price = int(price_text.replace('৳', '').replace(',', ''))
        image = item.find('div', class_='p-item-img').img['src']
        link = item.find('h4', class_='p-item-name').a['href']
        
        # ডাটাবেসে পাঠানোর জন্য ফরম্যাট
        product_data = {
            "name": name,
            "price": price,
            "image": image,
            "link": link + "?affiliate_id=YOUR_ID" # আপনার আইডি
        }

        # ডাটাবেসে ডাটা ইনসার্ট বা আপডেট (Upsert) করা
        # এটি নাম অনুযায়ী চেক করবে, যদি প্রোডাক্ট আগে থেকেই থাকে তবে শুধু দাম আপডেট করবে
        supabase.table("products").upsert(product_data, on_conflict="name").execute()

    print("Database Updated Successfully!")

if __name__ == "__main__":
    scrape_and_push()