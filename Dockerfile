FROM python:3-slim-bookworm 

WORKDIR /main

COPY . .

RUN pip install --no-cache-dir --upgrade --root-user-action ignore pip && pip install --no-cache-dir --root-user-action ignore "fastapi[standard]" gunicorn sqlmodel psycopg2-binary faker semver pydantic_extra_types pydantic_settings && python3 generate_todos.py && rm todos.json

CMD ["fastapi", "run", "src/main.py", "--workers", "17"]

