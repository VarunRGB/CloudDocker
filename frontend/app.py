from flask import Flask
import requests

app = Flask(__name__)

# The internal hostname for the catalog service, as defined in docker-compose.yml
CATALOG_SERVICE_URL = 'http://ecom-catalog:5001/products'

def fetch_products():
    """Attempts to fetch product data from the catalog service."""
    try:
        # Use the internal Docker network name 'ecom-catalog'
        response = requests.get(CATALOG_SERVICE_URL, timeout=2)
        response.raise_for_status() # Raise exception for bad status codes
        return response.json()
    except Exception as e:
        print(f"Error connecting to Catalog Service: {e}")
        return [{"id": 0, "name": "Error Loading Products", "price": 0.00, "description": "Backend service unavailable."}]

@app.route('/')
def home():
    products = fetch_products()
    
    # Generate the HTML response (mediocre CSS included!)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevOps Demo Shop</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 900px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #4CAF50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .product-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }}
            .product-card {{ background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 6px; }}
            .product-card h2 {{ font-size: 1.2em; color: #2C3E50; margin-top: 0; }}
            .product-card p {{ font-size: 0.9em; color: #777; }}
            .price {{ font-size: 1.5em; color: #E74C3C; font-weight: bold; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Automated Shop!</h1>
            <p>Content served by the Frontend Microservice, data pulled from the Catalog Microservice.</p>
            <div class="product-grid">
    """
    
    for p in products:
        html_content += f"""
        <div class="product-card">
            <h2>{p['name']}</h2>
            <p>{p['description']}</p>
            <div class="price">${p['price']:.2f}</div>
        </div>
        """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # Runs on port 5000 internally
    app.run(host='0.0.0.0', port=5000)
