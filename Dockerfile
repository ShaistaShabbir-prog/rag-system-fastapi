
# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory to the root of the project
WORKDIR /RAG_Shabbir

# Install dependencies first (for caching layers)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the whole project into the container's /RAG_Shabbir directory
COPY . /RAG_Shabbir

# Set the environment variable to ensure the app folder is on the module search path
ENV PYTHONPATH=/RAG_Shabbir/app

# Download and cache the Hugging Face model inside the container
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('google/flan-t5-small')"

# Expose FastAPI port
EXPOSE 8000

# Run the application with the correct import path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
