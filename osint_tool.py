import http.server
import socketserver
import urllib.parse as urlparse
import json
import requests
from bs4 import BeautifulSoup

# Webhook URL for Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1229639510888026132/egi6pOOl3j2NboANv7F-nGd9nr-koNxWxXcF-r21LNRM1LjPj8MU6BHIqs8rywFqaeUY"

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path

        if path == '/search':
            query = urlparse.parse_qs(parsed_path.query).get('query', [''])[0]
            if query:
                google_results = google_search(query)
                bing_results = bing_search(query)
                wikipedia_results = wikipedia_search(query)
                duckduckgo_results = duckduckgo_search(query)
                yahoo_results = yahoo_search(query)
                yandex_results = yandex_search(query)
                ask_results = ask_search(query)
                
                all_results = {
                    'Google': google_results,
                    'Bing': bing_results,
                    'Wikipedia': wikipedia_results,
                    'DuckDuckGo': duckduckgo_results,
                    'Yahoo': yahoo_results,
                    'Yandex': yandex_results,
                    'Ask': ask_results
                }

                # Log results to Discord webhook
                log_to_webhook(all_results)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(all_results).encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("Bad request: Query parameter missing".encode())
        else:
            super().do_GET()

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a')
    return [result.get('href') for result in results]

def bing_search(query):
    url = f"https://www.bing.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'class': 'b_algo'})
    return [result.get('href') for result in results]

def wikipedia_search(query):
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    return [url]

def duckduckgo_search(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'class': 'result__url'})
    return [result.get('href') for result in results]

def yahoo_search(query):
    url = f"https://search.yahoo.com/search?p={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'class': 'ac-algo'})
    return [result.get('href') for result in results]

def yandex_search(query):
    url = f"https://yandex.com/search/?text={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'class': 'organic__url'})
    return [result.get('href') for result in results]

def ask_search(query):
    url = f"https://www.ask.com/web?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'class': 'PartialSearchResults-item-title-link result-link'})
    return [result.get('href') for result in results]

def log_to_webhook(results):
    # Post results to Discord webhook
    payload = {'content': json.dumps(results)}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print("Failed to log results to webhook")

def run(port=8000):
    with socketserver.TCPServer(("", port), RequestHandler) as httpd:
        print(f"Server started on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
