
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import io
from PIL import Image
from fastapi.responses import StreamingResponse

DATABASE_URL = "postgresql://alby.:@localhost/postgres"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Image model
class ImageModel(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(LargeBinary, nullable=False)  # Store as binary blob

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/image/{image_id}")
async def get_image(image_id: int):
    db = SessionLocal()
    image_record = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    db.close()

    if image_record is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Read image binary data and open with PIL
    image_data = io.BytesIO(image_record.image_data)
    image = Image.open(image_data)

    # Convert image to an in-memory file-like object to stream
    img_io = io.BytesIO()
    image.save(img_io, format=image.format)  # Use original format (e.g., JPEG, PNG)
    img_io.seek(0)

    # Return the image as a streaming response with appropriate MIME type
    return StreamingResponse(img_io, media_type=f"image/{image.format.lower()}")



