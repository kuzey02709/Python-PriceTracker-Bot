### EN
# Python Automated Price Tracker & ML Trend Analyzer

A modular Python automation tool that periodically scrapes data from target websites, stores the records in a local SQL Server database, and performs trend analysis using linear regression based on historical price movements.

## Technologies Used
- Python (requests, BeautifulSoup) - HTML parsing and data extraction from target pages
- SQL Server & pyodbc - Database connection and logging
- Scikit-Learn & NumPy - Basic machine learning model for analyzing price trends
- Schedule - Process automation and scheduler loop

## System Architecture and Flow
1. Data Collection: Current product information is fetched and cleaned via the specified URL.
2. Persistent Storage: Extracted data is saved to the PriceTrackerDb database along with a timestamp.
3. Trend Analysis: Past records in the database are read chronologically, and future price trends are calculated using the LinearRegression model.
4. Automation Loop: Operates in the background at specified time intervals to fully automate the process.

## Installation and Execution

Install the required libraries:
```bash```
```pip install requests beautifulsoup4 pyodbc scikit-learn numpy schedule```

### TR
# Python Otomatik Fiyat Takip ve ML Trend Analiz Aracı

Hedef web sitelerinden periyodik olarak veri çeken, bu verileri yerel SQL Server veritabanında saklayan ve geçmiş fiyat hareketlerini baz alarak doğrusal regresyon ile trend tahmini yapan modüler bir Python otomasyon aracı.

## Kullanılan Teknolojiler
- Python (requests, BeautifulSoup) - Hedef sayfadan HTML parsing ve veri ayıklama
- SQL Server & pyodbc - Veritabanı bağlantısı ve loglama
- Scikit-Learn & NumPy - Fiyat eğilimlerini analiz etmek için temel makine öğrenmesi modeli
- Schedule - Süreç otomasyonu ve zamanlayıcı döngüsü

## Sistem Mimarisi ve Akış
1. Veri Toplama: Belirtilen URL üzerinden güncel ürün bilgileri çekilir ve temizlenir.
2. Kalıcı Depolama: Elde edilen veriler zaman damgasıyla birlikte PriceTrackerDb veritabanına kaydedilir.
3. Trend Analizi: Veritabanındaki geçmiş kayıtlar kronolojik sırayla okunarak LinearRegression modeli üzerinden geleceğe yönelik fiyat eğilimi hesaplanır.
4. Otomasyon Döngüsü: Belirlenen zaman aralıklarında arka planda çalışarak süreci tamamen otomatik hale getirir.

## Kurulum ve Çalıştırma

Gerekli kütüphaneleri yükleyin:
```bash```
```pip install requests beautifulsoup4 pyodbc scikit-learn numpy schedule```
