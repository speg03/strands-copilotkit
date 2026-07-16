FROM python:3.13-slim

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY src ./src
RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
