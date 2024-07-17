
## Installation

There are two options of installing the project. It can either be run locally or in a container.

No matter which option you choose, ensure to create a `config.json` file based on the provided template.

### Local

To run the project locally it is recommended to create a virtual Python environment with the following command executed in the project's root directory:

```bash
    python -m venv venv
```

The next step is to activate the environment and install the necessary packages:

```bash
    venv\Scripts\activate.bat
    pip install -r requirements.txt
```

To ensure that the imports are resolved correctly please ensure to install the the application package locally in an editable mode. This can be achieved by running the following command in a directory where the `setup.py` file is placed:

```bash
    pip install -e .
```

When running the project locally ensure that you have the database engine running.

The necessary information for connecting to the DB must be supplied via environment variables. Please create a `.env` file based on the provided `.env.template` and fill with the information about your DB instance.

Then, to run the app, use the following command:

```bash
    fastapi dev src\main.py
```


### Docker
> There is a `docker compose` file included in the repository that allows you to run the app using a `mysql` database. To run the application, ensure that you have docker installed and that the docker daemon is running. Once that's done, you can run the app by executing the following commands in the project's root directory:

```bash
    docker compose build
```

This will create the image for the backend.

```bash
    docker compose up -d 
```

This will create both the backend and DB continers as well as the necessary volumes.

> The app is using the `root` MySQL user that is created by default as well as the defautl `mysql` database. This is fine for running the project locally but should be changed in case of running the project in a production environment - there shoudl be a dedicated DB user with less priveleges.