# Query Kong Metrics Using Service Account

## Overview

Using a service account generated within your namespace, you can send Prometheus queries to retrieve Kong metrics. Some examples will be provided, but any [PromQL (Prometheus Query Language)](https://prometheus.io/docs/prometheus/latest/querying/basics/) query can be sent.

## Prerequisites

- Namespace in the API Gateway
- Service Account associated with the namespace
  - Service Account should have at least `Namespace.View` permissions
- Ideally (but not necessary) an active service experiencing some traffic

## TL;DR

Generate an access token with your Service Account. Use the token to send PromQL queries with the following command. Note that queries should be URL encoded.

```sh
curl -v -H "Authorization: Bearer <access-token>" "https://gw-pql-api-gov-bc-ca.dev.api.gov.bc.ca/api/v1/<query>"
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
curl -v -H "Authorization: Bearer $TOK" "https://gw-pql-api-gov-bc-ca.dev.api.gov.bc.ca/api/v1/<query>"
```

## Example Queries

Reminder that if you wish to modify the PromQL queries, it should be URL encoded before sending the request.

Run the following before running the example queries below:

```sh
export PQ_URL=https://gw-pql-api-gov-bc-ca.dev.api.gov.bc.ca/api/v1
```

You can get a range of data between two points in time as well. This can be done by sending a request to: `/query_range?query=<query>&start=$START&end=$END&step=$STEP` instead of: `/query?query=<query>`. Below is some sample data if you wish to use `/query_range`.

```sh
export END=$(date +'%s') # End of time range. Example uses current UNIX time.
export START=$(($END - (60 * 60 * 5))) # Start of time range. Example subtracts 5h from END time.
export STEP=300 # Number of seconds the query steps before evaluating. Eg: evaluate at t0s, then t300s, then t600s, etc.
```

### Rate per Second per route/service by Status Code

**Raw PromQL Query:**

```
sum(rate(kong_http_status{service=~".*", route=~".*", instance=~".*"}[1m])) by (service,code)
```

**Example Command:**

```sh
export QUERY=sum%28rate%28kong_http_status%7Bservice%3D~%22.%2A%22%2C%20route%3D~%22.%2A%22%2C%20instance%3D~%22.%2A%22%7D%5B1m%5D%29%29%20by%20%28service%2Ccode%29

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"

# # Using /query_range
# curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
```

### Req/5m per route/service

**Raw PromQL Query:**

```
sum(increase(kong_http_status{service=~".*", route=~".*", instance=~".*"}[5m])) by (service,code) != 0
```

**Example Command:**

```sh
export QUERY=sum%28increase%28kong_http_status%7Bservice%3D~%22.%2A%22%2C%20route%3D~%22.%2A%22%2C%20instance%3D~%22.%2A%22%7D%5B5m%5D%29%29%20by%20%28service%2Ccode%29%20%21%3D%200

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"

# # Using /query_range
# curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
```

### Request time per Service

**Raw PromQL Query:**

```
histogram_quantile(0.95, sum(rate(kong_latency_bucket{type="request", service =~ ".*",route=~".*",instance=~".*"}[1m])) by (service,le))
```

**Example Command:**

```sh
export QUANTILE=0.95
export QUERY=histogram_quantile%28$QUANTILE%2C%20sum%28rate%28kong_latency_bucket%7Btype%3D%22request%22%2C%20service%20%3D~%20%22.%2A%22%2Croute%3D~%22.%2A%22%2Cinstance%3D~%22.%2A%22%7D%5B1m%5D%29%29%20by%20%28service%2Cle%29%29

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"

# # Using /query_range
# curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
```

### Request time per Route

**Raw PromQL Query:**

```
histogram_quantile(0.90, sum(rate(kong_latency_bucket{type="request", service =~ ".*",route=~".*",instance=~".*"}[1m])) by (route,le))
```

**Example Command:**

```sh
export QUANTILE=0.90
export QUERY=histogram_quantile%280$QUANTILE%2C%20sum%28rate%28kong_latency_bucket%7Btype%3D%22request%22%2C%20service%20%3D~%20%22.%2A%22%2Croute%3D~%22.%2A%22%2Cinstance%3D~%22.%2A%22%7D%5B1m%5D%29%29%20by%20%28route%2Cle%29%29

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"

# # Using /query_range
# curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
```

### Total Non-200 requests per second by route, code

**Raw PromQL Query:**

```
sum(rate(kong_http_status{instance=~".*",code!="200",code!="204",code!="201"}[5m])) by (route,code) != 0
```

**Example Command:**

```sh
export QUERY=sum%28rate%28kong_http_status%7Binstance%3D~%22.%2A%22%2Ccode%21%3D%22200%22%2Ccode%21%3D%22204%22%2Ccode%21%3D%22201%22%7D%5B5m%5D%29%29%20by%20%28route%2Ccode%29%20%21%3D%200

curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query?query=$QUERY"

# # Using /query_range
# curl -v -H "Authorization: Bearer $TOK" "$PQ_URL/query_range?query=$QUERY&start=$START&end=$END&step=$STEP"
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

Check out the [QUERYING PROMETHEUS](https://prometheus.io/docs/prometheus/latest/querying/basics/) documentation for the basics of forming PromQL queries.

I also felt [this video](https://youtu.be/hvACEDjHQZE) was useful for learning PromQL basics.

## Grafana and Additional Queries

We have a number of panels in our Grafana dashboards showcasing a number of queries. Here some examples of on our dashboard, along with the associated PromQL queries:

- Total Requests per second
  - sum(rate(kong_http_status{instance=~".*"}[1m]))
- Kong Proxy Latency per Service
  - histogram_quantile(0.90, sum(rate(kong_latency_bucket{type="kong", service =~ ".*",route=~".*",instance=~".*"}[1m])) by (service,le))
- Upstream Time per Service
  - histogram_quantile(0.90, sum(rate(kong_latency_bucket{type="upstream", service =~ ".*",route=~".*",instance=~".*"}[1m])) by (service,le))
- Total Requests (5m) by Consumer
  - sum(increase(konglog_service_consumer_counter{service=~".*",consumer!=""}[5m]])) by (consumer, service, status) != 0
- 400 and 500 Errors
  - sum(increase(konglog_service_agent_counter{status!='200',status!='201',status!='204',status!='206',status!='301',status!='302',status!='304',service!=''}[5m])) by (service, status) != 0
