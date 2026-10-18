import re
import requests
import urllib.parse
import idna

def analyze_url(url: str):
    print(f"\n?? Analyzing URL: {url}")
    print("-" * 50)
    
    # 1. Check for IDN Homograph Attack (Lookalike characters)
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    
    try:
        punycode_domain = idna.encode(domain).decode('ascii')
        if "xn--" in punycode_domain:
            print("?? WARNING: Homograph Attack Detected!")
            print(f"   Original domain uses lookalike characters.")
            print(f"   Punycode representation: {punycode_domain}")
        else:
            print("? Domain formatting appears legitimate (No homographs).")
    except Exception as e:
        print(f"?? Error checking domain characters: {e}")

    # 2. Safely follow redirects without executing harmful browser code
    print("\n?? Testing URL Redirection and End-Destination...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5, stream=True)
        
        if len(response.history) > 0:
            print(f"?? URL Redirected {len(response.history)} time(s).")
            for resp in response.history:
                print(f"   -> Passed through: {resp.url} ({resp.status_code})")
            print(f"?? Final Destination: {response.url}")
        else:
            print("? Direct Link. No redirects found.")
            
    except requests.exceptions.RequestException as e:
        print(f"? Failed to reach URL safely: {e}")

if __name__ == "__main__":
    # Test case: A standard short link that redirects
    test_url = "https://bit.ly" 
    analyze_url(test_url)
