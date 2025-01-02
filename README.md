# internet-shop

Web application of a shop with machine learning models, built with python, postgresql, redis, kafka.

## Configuration and requirements

You will need a `Docker Compose` and `Git LFS`.
With Git LFS do:

```bash
git lfs install
git lfs fetch --all
git lfs pull
```

## Build

### Backend

```bash
make # this will build and run a program
make down # this will close the application
```

### Frontend

With your virtual env activated, do:
```bash
streamlit run web/main.py
```