import psycopg2

# Database connection details
conn = psycopg2.connect("dbname=postgres user=alby. host=localhost")
cursor = conn.cursor()

# Path to your image
image_path = "/Users/alby./Desktop/galaxy.png"

# Open the image file in binary mode and read its contents
with open(image_path, "rb") as file:
    binary_data = file.read()

# Prepare other image information
image_name = "Sample Image"
image_type = "image/png"  # Set MIME type based on your image format
description = "A sample image stored as binary data"
size = len(binary_data)  # Size in bytes

# Insert the image data into PostgreSQL
cursor.execute("""
    INSERT INTO images(image_name, image_data)
    VALUES (%s, %s)
""", (image_name, binary_data))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Image data inserted successfully.")
