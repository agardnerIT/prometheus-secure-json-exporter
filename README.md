# prometheus-secure-json-exporter
Sample files for exposing and scraping json_exporter securely with Prometheus.

This is the companion repo for this video:

TODO

## Step 1: Install Requirements & Start App

```
pip install -r requirements.txt
fastapi run main.py  --host localhost --port 8123
```

Access `http://127.0.0.1:8123` and login with:

* Username: `agardnerit`
* Password: `password123`

> Note! Details are hardcoded in `main.py` this is **terrible** security practice and this is ONLY a demo!
>
> DO NOT COPY & PASTE AND USE AS-IS IN ANYTHING IMPORTANT!

## Step 2: Start json_exporter

[Download and extract](https://github.com/prometheus-community/json_exporter/releases/latest) the json_exporter binary. Now run:

```
./json_exporter --config.file=json-exporter-config.yaml
```

## Step 3: Start Prometheus

Download and extract the prometheus binary. Run it:

```
./prometheus --config.file=prometheus-insecure.yml
```

This will work, you will see the target and metrics in Prometheus.

# The Problem

You're scraping an authenticated endpoint but the Prometheus endpoint is wide-open. Thus all that security protection is gone because anyone can see the Prometheus stats.

Let's fix that now.

## Step 3: Add basic auth to json_exporter endpoint

The json_exporter supports basic authentication too. First, decide on a username and password (this could be different from the API endpoint).

For this tutorial, the same values will be used:

* Username: `agardnerit`
* Password: `password123`

The json_exporter mirrors the functionality of the blackbox_exporter, which in turn uses `bcrypt` hashed passwords. So find a way on your OS to hash a password.

Following [the docs]([https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md](https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md#about-bcrypt), I can achieve this with:

```
htpasswd -nBC 10 "" | tr -d ':\n'
```

Take your encrypted value and place it in [json-exporter-web-config.yaml](json-exporter-web-config.yaml) with this syntax:

```
basic_auth_users:
  <USERNAME>: <BCRYPT_PASSWORD_VALUE_HERE>
```

Now start json-exporter with both the `--config.file` and `--web.config.file` parameters:

```
./json_exporter --config.file=json-exporter-config.yaml --web.config.file=json-exporter-web-config.yaml
```

Go to `http://localhost:7979/probe?target=http://localhost:8123` and you should now be prompted with a basic auth login box.

## Step 4: Enable Prometheus to authenticate

Up to this point, Prometheus is expecting to scrape open endpoints. We need to tell Prometheus what the username and password of the `/probe` endpoint is.

See [prometheus-secure.yaml](prometheus-secure.yaml). While you _could_ use the `password` field, I HIGHLY discourage it as it's just too easy for your password to end up in Git.

Rather, create ANOTHER file containing only the bcrypt hashed password and point to that file with the `password_file` field. This way, you can still commit the prometheus YAML to Git if you want and the hash is never publicly available.

Start Prometheus:

```
./prometheus --config.file=prometheus-secure.yml
```
