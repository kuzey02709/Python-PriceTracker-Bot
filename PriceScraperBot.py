import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pyodbc
import numpy as np
from sklearn.linear_model import LinearRegression
import schedule

URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

SERVER = '(localdb)\\MSSQLLocalDB'
DATABASE = 'PriceTrackerDb'
CONNECTION_STRING = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'


def get_product_data():
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('h1').get_text(strip=True)
            price_raw = soup.find('p', class_='price_color').get_text(strip=True)
            
            price = float(price_raw.replace('£', '').strip())
            check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {'title': title, 'price': price, 'time': check_time}
        else:
            print(f"Sayfaya ulaşılamadı. Durum Kodu: {response.status_code}")
            return None
    except Exception as e:
        print(f"Scraping Hatası: {e}")
        return None


def save_to_sql(title, price, check_time):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ProductPriceLogs' and xtype='U')
            CREATE TABLE ProductPriceLogs (
                Id INT IDENTITY(1,1) PRIMARY KEY,
                ProductTitle NVARCHAR(255),
                Price DECIMAL(18,2),
                CheckTime DATETIME
            )
        """)
        conn.commit()
        
        query = "INSERT INTO ProductPriceLogs (ProductTitle, Price, CheckTime) VALUES (?, ?, ?)"
        cursor.execute(query, (title, price, check_time))
        conn.commit()
        
        cursor.close()
        conn.close()
        print("-> Veri başarıyla SQL Server veritabanına kaydedildi.")
    except Exception as e:
        print(f"SQL Kayıt Hatası: {e}")


def analyze_price_trend():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        cursor.execute("SELECT Price FROM ProductPriceLogs ORDER BY CheckTime ASC")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if len(rows) < 2:
            print("\n[Bilgi] Henüz yeterli veri birikmedi (En az 2 kayıt gerekiyor).")
            return

        prices = [row[0] for row in rows]
        
        X = np.array(range(len(prices))).reshape(-1, 1)
        y = np.array(prices)
        
        model = LinearRegression()
        model.fit(X, y)
        
        next_x = np.array([[len(prices)]])
        predicted_price = model.predict(next_x)[0]
        
        print("\n--- Makine Öğrenmesi Fiyat Trend Analizi ---")
        print(f"Toplam Ölçüm Sayısı : {len(prices)}")
        print(f"Son Kaydedilen Fiyat: £{prices[-1]}")
        print(f"Gelecek Tahmini Fiyat: £{predicted_price:.2f}")
        
        if predicted_price > prices[-1]:
            print("Trend Durumu: Fiyatlar artış eğiliminde.")
        else:
            print("Trend Durumu: Fiyatlar düşüş veya yatay seyir eğiliminde.")
        print("-" * 40)

    except Exception as e:
        print(f"Analiz Hatası: {e}")


def job():
    print(f"\n[OTOMATİK GÖREV BAŞLATILDI] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data = get_product_data()
    if data:
        print(f"Ürün: {data['title']} | Fiyat: £{data['price']}")
        save_to_sql(data['title'], data['price'], data['time'])
        analyze_price_trend()


if __name__ == "__main__":
    print("--- Fiyat Takip Otomasyon Sistemi Devreye Alındı ---")
    print("Bot arka planda çalışıyor. Durdurmak için CTRL+C tuşlarına basabilirsin.\n")
    
    job()
    
    schedule.every(1).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)