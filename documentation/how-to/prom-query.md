---
title: "Query Kong Metrics"
---

## Overview

Using a service account generated within your namespace, you can send Prometheus queries to retrieve Kong metrics. Some examples will be provided, but any [PromQL (Prometheus Query Language)](https://prometheus.io/docs/prometheus/latest/querying/basics/) query can be sent.

## Prerequisites

- Namespace in the API Gateway
- Service Account associated with the namespace
  - Service Account should have at least `Namespace.View` permissions
- Ideally an active service experiencing some traffic

## TL;DR

Generate an access token with your Service Account. Use the token to send PromQL queries with the following command. Note that queries should be URL encoded.

```sh
curl -v -H "Authorization: Bearer <access-token>" "<prom-query-url>/api/v1/<query>"
```

## Detailed Instructions

### Getting an Access Token

Using your Service Account credentials, generate an access token:

```bash
export CID=my-client-id
export CSC=my-client-secret
export TOKEN_URL=my-token-url

curl $TOKEN_URL -X POST -H "Content-Type: application/x-www-form-urlencoded" \
-d client_id=$CID -d client_secret=$CSC \
-d grant_type=client_credentials -d scopes=openid
```

Copy and save the access token:

```bash
export TOK=my-copied-access-token
```

### Running Queries

Once you have an access token, you can run queries using:

```sh
curl -v -H "Authorization: Bearer $TOK" "<prom-query-url>/api/v1/<query>"
```

## Example Queries

Reminder that if you wish to modify the PromQL queries, it should be URL encoded before sending the request.

Run the following before running the example queries below:

```sh
export PQ_URL=https://gw-pql.api.gov.bc.ca/api/v1
# Can also query dev and test environments. Replace <env> with either dev or test:
# export PQ_URL=https://gw-pql-api-gov-bc-ca.<env>.api.gov.bc.ca/api/v1
```

### To execute queries

Run one of the `export QUERY=...` example blocks, then run one of the `Execute ...` blocks below to execute that query:

```sh
# Execute at current server timestamp:
curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"
```

```sh
# Execute at specific time, eg 5 days ago:
export FIVE_DAYS_AGO=$(($(date +'%s') - (60 * 60 * 24 * 5)))

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY&time=$FIVE_DAYS_AGO"
```

```sh
# Execute using /query_range:
export END=$(date +'%s') # End of time range. Example uses current UNIX time.
export START=$(($END - (60 * 60 * 5))) # Start of time range. Example subtracts 5h from END time.
export STEP=300 # Number of seconds the query steps before evaluating. Eg: evaluate at START + 0s, then START + 300s, etc.

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
```

### Rate per Second per route/service by Status Code

```sh
# Raw PromQL Query:
# sum(rate(kong_http_status{service=~".*", route=~".*"}[1m])) by (service,code)

export QUERY=sum%28rate%28kong_http_status%7Bservice%3D~%22.%2A%22%2C%20route%3D~%22.%2A%22%7D%5B1m%5D%29%29%20by%20%28service%2Ccode%29
```

### Req/5m per route/service

```sh
# Raw PromQL Query:
# sum(increase(kong_http_status{service=~".*", route=~".*"}[5m])) by (service,code) != 0

export QUERY=sum%28increase%28kong_http_status%7Bservice%3D~%22.%2A%22%2C%20route%3D~%22.%2A%22%7D%5B5m%5D%29%29%20by%20%28service%2Ccode%29%20%21%3D%200
```

### Request time per Service

**Raw PromQL Query:**

```sh
# Raw PromQL Query:
# histogram_quantile(0.95, sum(rate(kong_latency_bucket{type="request", service =~ ".*",route=~".*"}[1m])) by (service,le))

export QUANTILE=0.95
export QUERY=histogram_quantile%280.95%2C%20sum%28rate%28kong_latency_bucket%7Btype%3D%22request%22%2C%20service%20%3D~%20%22.%2A%22%2Croute%3D~%22.%2A%22%7D%5B1m%5D%29%29%20by%20%28service%2Cle%29%29
```

### Total Non-200 requests per second by route, code

```sh
# Raw PromQL Query:
# sum(rate(kong_http_status{code!="200",code!="204",code!="201"}[5m])) by (route,code) != 0

export QUERY=sum%28rate%28kong_http_status%7Bcode%21%3D%22200%22%2Ccode%21%3D%22204%22%2Ccode%21%3D%22201%22%7D%5B5m%5D%29%29%20by%20%28route%2Ccode%29%20%21%3D%200
```

## Help

### Prometheus HTTP API Documentation

View the [Prometheus HTTP API Documentation](https://prometheus.io/docs/prometheus/latest/querying/api/) for additional information on sending requests to the Prometheus API.

Some helpful takeaways:

- Send a GET request to the `/metadata` endpoint to list all available metrics.
  - You can limit the number of results using the `?limit=<number>` query string parameter
  - Use the `?metric=<string>` qsp to get information about a specific metric.
- Use `/labels` to get a list of available labels.
- Use `/label/<label_value>/values` to get possible values for a given `label_value`
- Use `/series` to get a list of time series that match a given label set. View Prometheus API docs for more info.

### PromQL

Check out the [Prometheus querying documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/) for the basics of forming PromQL queries.

[This video](https://youtu.be/hvACEDjHQZE) is also a good introduction.

## Grafana and Additional Queries

The panels in the [Grafana dashboards](/how-to/monitoring.md) available to
API Providers make use of PromQL data sources. Here a few of the metrics seen on
the dashboards, along with the PromQL queries:

- Total Requests per second
  
  ```linenums="0"
  sum(rate(kong_http_status[1m]))
  ```
  
- Kong Proxy Latency per Service

  ```linenums="0"
  histogram_quantile(0.90, sum(rate(kong_latency_bucket{type="kong", service =~ ".*",route=~".*",1m])) by (service,le))
  ```
  
- Upstream Time per Service

  ```linenums="0"
  histogram_quantile(0.90, sum(rate(kong_latency_bucket{type="upstream", service =~ ".*",route=~".*",}[1m])) by (service,le))`
  ```

- Total Requests (5m) by Consumer
  
  ```linenums="0"
  sum(
      increase(
          konglog_service_consumer_counter{
              service=~".*",
              consumer!=""
          }[5m]
      )
  ) by (consumer, service, status) != 0
  ```

- 400 and 500 Errors
  
  ```linenums="0"
  sum(
      increase(
          konglog_service_agent_counter{
              status!='200',
              status!='201',
              status!='204',
              status!='206',
              status!='301',
              status!='302',
              status!='304',
              service!=''
          }[5m]
      )
  ) by (service, status) != 0
  ```
