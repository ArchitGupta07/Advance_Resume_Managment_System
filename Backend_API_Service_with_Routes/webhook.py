from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST","PUT"],
    allow_headers=["*"],
)

@app.webhooks.post("/webhook")
def fileUploaded(body):
    print(body)



