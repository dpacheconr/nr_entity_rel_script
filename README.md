
## Running docker

1. Ensure you've created the `env_file` (beware, it shouldn't have double quotes in it at all)
2. Build the image: `docker build -t nrgql .`
3. Run the image specifying the env_file: `docker run --env-file env_file nrgql` 

## Running local

1. Ensure you've created the required variables 
    > export NEWRELIC_ACCOUNT_ID=YOURACCOUNTID && export NEWRELIC_USER_KEY="YOURAPIKEY"
2. Run script
    > python3 app.py
