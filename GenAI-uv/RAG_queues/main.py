import uvicorn
from .server import app  # import the FastAPI app from server.py

def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")

main()
# if __name__ == "__main__":
#     start_server()