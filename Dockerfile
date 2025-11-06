FROM python:3.10-slim

# Create non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install lightweight deps first
COPY --chown=user:user requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# If heavy ML requirements exist, install CPU-only torch then the list
COPY --chown=user:user requirements-ml.txt ./requirements-ml.txt
RUN if [ -f "./requirements-ml.txt" ]; then \
      pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
      pip install --no-cache-dir -r requirements-ml.txt ; \
    fi

# Copy project files
COPY --chown=user:user . /app

# Expose HF Spaces required port
EXPOSE 7860

# Start FastAPI (must listen on 7860 for HF Spaces)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
