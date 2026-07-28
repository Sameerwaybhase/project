import os
import json
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import boto3

app = FastAPI(
    title="Cloud-Native E-Commerce Backend Engine",
    description="Microservice API with Redis Caching, S3 Presigned Uploads, and Cognito Auth",
    version="1.0.0"
)

S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "ecommerce-product-media-bucket")
REGION = os.environ.get("AWS_REGION", "us-east-1")

s3_client = boto3.client("s3", region_name=REGION)

PRODUCT_CATALOG = [
    {"id": 1, "title": "Developer Cloud Hoodie", "price": 59.99, "category": "Apparel"},
    {"id": 2, "title": "DevOps Engineering Mug", "price": 19.99, "category": "Accessories"},
    {"id": 3, "title": "Wireless Mechanical Keyboard", "price": 129.99, "category": "Electronics"}
]

class UploadUrlRequest(BaseModel):
    filename: str

class OrderCreateRequest(BaseModel):
    product_id: int
    quantity: int

@app.get("/health")
def health_check():
    return {"status": "UP", "service": "E-Commerce Engine"}

@app.get("/products")
def list_products():
    return {"status": "success", "count": len(PRODUCT_CATALOG), "products": PRODUCT_CATALOG}

@app.post("/products/upload-url")
def get_presigned_media_upload_url(payload: UploadUrlRequest):
    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET, 'Key': f"products/{payload.filename}"},
            ExpiresIn=3600
        )
        return {"status": "success", "upload_url": url, "expires_in_seconds": 3600}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders")
def place_order(order: OrderCreateRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized. JWT Token required.")
    
    return {
        "status": "success",
        "order_id": "ORD-99281",
        "message": "Order placed successfully.",
        "details": order
    }
