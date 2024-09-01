from flask import Flask, json
import random
import uuid
from datetime import datetime


def random_domain():
    return f"{uuid.uuid4().hex[:8]}.example.com"


def random_path():
    return f"/v{random.randint(1, 3)}/locations/{uuid.uuid4().hex[:12]}"


def random_http_method():
    return random.choice(["GET", "POST", "PUT", "DELETE", "PATCH"])


def random_geo_location():
    locations = [
        {"city": "New York", "state_code": "US-NY", "state_name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"city": "Los Angeles", "state_code": "US-CA", "state_name": "California", "lat": 34.0522, "lon": -118.2437},
        {"city": "Chicago", "state_code": "US-IL", "state_name": "Illinois", "lat": 41.8781, "lon": -87.6298},
        {"city": "Houston", "state_code": "US-TX", "state_name": "Texas", "lat": 29.7604, "lon": -95.3698},
        {"city": "Phoenix", "state_code": "US-AZ", "state_name": "Arizona", "lat": 33.4484, "lon": -112.0740},
        {"city": "Miami", "state_code": "US-FL", "state_name": "Florida", "lat": 25.7617, "lon": -80.1918},
        {"city": "Denver", "state_code": "US-CO", "state_name": "Colorado", "lat": 39.7392, "lon": -104.9903},
        {"city": "Seattle", "state_code": "US-WA", "state_name": "Washington", "lat": 47.6062, "lon": -122.3321},
        {"city": "Atlanta", "state_code": "US-GA", "state_name": "Georgia", "lat": 33.7490, "lon": -84.3880},
        {"city": "Boston", "state_code": "US-MA", "state_name": "Massachusetts", "lat": 42.3601, "lon": -71.0589}
    ]
    return random.choice(locations)


def random_namespace():
    return f"namespace-{uuid.uuid4().hex[:8]}"


def mock_elb_log():
    domain = random_domain()
    path = random_path()
    original_url = f"https://{domain}:443{path}"
    http_method = random_http_method()
    geo_location = random_geo_location()
    namespace = random_namespace()

    log = {
        "_index": f".ds-logs-aws.elb_logs-{datetime.now().strftime('%Y.%m.%d')}-some_number",
        "_id": str(uuid.uuid4()),
        "_version": 1,
        "_score": 0,
        "_source": {
            "agent": {
                "name": "elastic-agent-relay-production",
                "id": str(uuid.uuid4()),
                "ephemeral_id": str(uuid.uuid4()),
                "type": "filebeat",
                "version": "8.0.1"
            },
            "tracing": {
                "trace": {
                    "id": str(uuid.uuid4())
                }
            },
            "log": {
                "file": {
                    "path": f"https://alb-elastic-agent-relay-us-east-1-production.s3.us-east-1.amazonaws.com/AWSLogs/somenumber/elasticloadbalancing/us-east-1/2024/08/29/{str(uuid.uuid4())}_elasticloadbalancing_us-east-1_app.some_number"
                },
                "offset": random.randint(1000000, 9999999)
            },
            "elastic_agent": {
                "id": str(uuid.uuid4()),
                "version": "8.0.1",
                "snapshot": False
            },
            "destination": {
                "domain": domain
            },
            "source": {
                "geo": {
                    "continent_name": "North America",
                    "region_iso_code": geo_location["state_code"],
                    "city_name": geo_location["city"],
                    "country_iso_code": "US",
                    "country_name": "United States",
                    "location": {
                        "lon": geo_location["lon"],
                        "lat": geo_location["lat"]
                    },
                    "region_name": geo_location["state_name"]
                },
                "as": {
                    "number": random.int(1000, 9999),
                    "organization": {
                        "name": "some_organization"
                    }
                },
                "port": random.randint(10000, 65535),
                "ip": "some_ip"
            },
            "url": {
                "path": path,
                "original": original_url,
                "scheme": "https",
                "port": 443,
                "domain": domain
            },
            "tags": [
                "forwarded",
                "aws-elb-logs"
            ],
            "cloud": {
                "provider": "aws",
                "region": "us-east-1"
            },
            "input": {
                "type": "aws-s3"
            },
            "@timestamp": datetime.utcnow().isoformat() + "Z",
            "ecs": {
                "version": "8.0.0"
            },
            "data_stream": {
                "namespace": namespace,
                "type": "logs",
                "dataset": "aws.elb_logs"
            },
            "http": {
                "request": {
                    "method": http_method,
                    "body": {
                        "bytes": random.randint(100, 500)
                    }
                },
                "response": {
                    "status_code": 200,
                    "body": {
                        "bytes": random.randint(1000, 2000)
                    }
                },
                "version": "1.1"
            },
            "tls": {
                "cipher": "ECDHE-RSA-AES128-GCM-SHA256",
                "version": "1.2",
                "version_protocol": "tls"
            },
            "aws": {
                "s3": {
                    "bucket": {
                        "name": "some_bucket",
                        "arn": f"arn:aws:s3:::some_bucket"
                    },
                    "object": {
                        "key": f"AWSLogs/somenumber/elasticloadbalancing/us-east-1/2024/08/29/{str(uuid.uuid4())}_elasticloadbalancing_us-east-1_app.some_api.0fe77309"
                    }
                },
                "elb": {
                    "trace_id": str(uuid.uuid4()),
                    "matched_rule_priority": "0",
                    "ssl_cipher": "ECDHE-RSA-AES128-GCM-SHA256",
                    "type": "https",
                    "request_processing_time": {
                        "sec": 0.001
                    },
                    "response_processing_time": {
                        "sec": 0
                    },
                    "target_port": [
                        "some_port"
                    ],
                    "protocol": "http",
                    "target_status_code": [
                        "200"
                    ],
                    "name": "app/ELB/some_number",
                    "backend": {
                        "port": "443",
                        "ip": "some_ip",
                        "http": {
                            "response": {
                                # randomly select a status code from a distribution
                                "status_code": random.choices([200, 301, 404, 500], weights=[0.9, 0.05, 0.025, 0.025])[0],
                            }
                        }
                    },
                    "target_group": {
                        "arn": f"arn:aws:elasticloadbalancing:us-east-1:somenumber:targetgroup/somenumber/{str(uuid.uuid4())}"
                    },
                    "backend_processing_time": {
                        "sec": 0.067
                    },
                    "ssl_protocol": "TLSv1.2",
                    "chosen_cert": {
                        "arn": "session-reused"
                    },
                    "action_executed": [
                        "waf",
                        "forward"
                    ]
                }
            },
            "event": {
                "agent_id_status": "verified",
                "ingested": datetime.utcnow().isoformat() + "Z",
                "kind": "event",
                "start": datetime.utcnow().isoformat() + "Z",
                "end": datetime.utcnow().isoformat() + "Z",
                "category": "web",
                "dataset": "aws.elb_logs",
                "outcome": "success"
            },
            "user_agent": {
                "original": "-",
                "name": "Other",
                "device": {
                    "name": "Other"
                }
            }
        },
        "fields": {
            "aws.elb.target_group.arn": [
                f"arn:aws:elasticloadbalancing:us-east-1:somenumber:targetgroup/some_api/{str(uuid.uuid4())}"
            ],
            "aws.elb.backend.ip": [
               "some_ip"
            ],
            "elastic_agent.version": [
                "8.0.1"
            ],
            "event.category": [
                "web"
            ],
            "tls.version_protocol": [
                "tls"
            ],
            "http.request.method": [
                http_method
            ],
            "source.geo.region_name": [
                geo_location["state_name"]
            ],
            "aws.elb.chosen_cert.arn": [
                "session-reused"
            ],
            "aws.elb.request_processing_time.sec": [
                0.001
            ],
            "aws.elb.name": [
                "app/some_api/some_id"
            ],
            "source.ip": [
               "some_ip"
            ],
            "agent.name": [
                "elastic-agent-relay-production"
            ],
            "event.agent_id_status": [
                "verified"
            ],
            "source.geo.region_iso_code": [
                geo_location["state_code"]
            ],
            "event.kind": [
                "event"
            ],
            "http.response.status_code": [
                200
            ],
            "http.version": [
                "1.1"
            ],
            "event.outcome": [
                "success"
            ],
            "source.geo.city_name": [
                geo_location["city"]
            ],
            "tls.version": [
                "1.2"
            ],
            "user_agent.original": [
                "-"
            ],
            "tracing.trace.id": [
                str(uuid.uuid4())
            ],
            "cloud.region": [
                "us-east-1"
            ],
            "aws.elb.type": [
                "https"
            ],
            "aws.elb.response_processing_time.sec": [
                0
            ],
            "aws.elb.protocol": [
                "http"
            ],
            "input.type": [
                "aws-s3"
            ],
            "log.offset": [
                random.randint(1000000, 9999999)
            ],
            "user_agent.name": [
                "Other"
            ],
            "aws.elb.backend.port": [
                "443"
            ],
            "destination.domain": [
                domain
            ],
            "data_stream.type": [
                "logs"
            ],
            "aws.elb.target_status_code": [
                "200"
            ],
            "tags": [
                "forwarded",
                "aws-elb-logs"
            ],
            "cloud.provider": [
                "aws"
            ],
            "url.path": [
                path
            ],
            "agent.id": [
                str(uuid.uuid4())
            ],
            "source.port": [
                random.randint(10000, 65535)
            ],
            "ecs.version": [
                "8.0.0"
            ],
            "aws.elb.ssl_protocol": [
                "TLSv1.2"
            ],
            "elastic_agent.snapshot": [
                False
            ]
        }
    }

    return log

app = Flask(__name__)

@app.route('/')
def home():
    return json.dumps({"message": "Mocking Things."}), 200, {'Content-Type': 'application/json'}



@app.route('/elb')
def mock_elb():
    return json.dumps(mock_elb_log()['_source'], indent=4), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(port=8080, debug=True)