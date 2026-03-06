import urllib.request
import urllib.error

def test_endpoints():
    base_url = "http://127.0.0.1:5000"
    endpoints = [
        "/",
        "/login",
    ]
    
    print("Testing Endpoints:")
    for ep in endpoints:
        try:
            response = urllib.request.urlopen(base_url + ep)
            print(f"Endpoint {ep}: Status {response.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"Endpoint {ep}: Status {e.code}")
        except Exception as e:
            print(f"Endpoint {ep}: Failed - {e}")

if __name__ == "__main__":
    test_endpoints()
