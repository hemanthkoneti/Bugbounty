# BugBounty

## Setup

### Make a virtual environment using conda

```
conda crate -m bugbounty flask
```

### Install dependencies

```
pip install -r requirements.txt
```

### Create migrations

```
flask db init
```

```
flask db migrate
```

```
flask db upgrade
```

### Run the application

```
python app.py
```
