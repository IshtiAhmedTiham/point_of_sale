# POINT OF SALE

## Installation

```bash
# Install Fastapi
pip install "fastapi[standard]"

# Install SQLAlchemy
pip install sqlalchemy

# Install Postgresql
pip install psycopg2-binary

# Install Hash Password
pip install 'pwdlib[argon2]'

# Install jwt
pip install python-jose[cryptography]
```

## Usage

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "This is home page"
```

## Git Clone

git@github.com:IshtiAhmedTiham/point_of_sale.git