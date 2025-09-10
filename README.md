# enki-grpc-client-test

 - Use `cli.py` to connect to gRPC client
 - Use `rmq_publisher` to publish object meta to a queue


### Envs required
 - CLIENT_RECONNECTION_TIMEOUT=<value in seconds \>
 - RMQ_HOST=<rabbit mq host \>
 - SESSION_ID=<queue name to which consumer connects \>
 - GCS_BUCKET_NAME=<bucket name on gcs \>

### Tests with grpcurl

Start enki as `python src/enki_v2/main.py grpc_server`. By default starts at port 50051, to change port change env variable GRPC_SERVER_PORT.

 - Health Check
```bash
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check

# Output
{
  "status": "SERVING"
}
```

 - Reflection(list available services)
```bash
grpcurl -plaintext localhost:50051 list

# Output
events.EventService
events.TelemetryService
grpc.health.v1.Health
grpc.reflection.v1alpha.ServerReflection
```

 - Event Service
    - StreamRequest
    ```bash
    grpcurl -plaintext localhost:50051 events.EventService/StreamEvents

    # In parallel publish a message using python rmq_publisher.py
    {
      "type": "logstream",
      "logstream": {
        "guid": "8da2fc0e-c6e2-44ac-8409-b4b99cb1328e",
        "message": "Analysis result processed successfully: run_67890",
        "timestamp": "1757520203"
      },
      "timestamp": "2025-09-10T16:03:23.631189Z"
    }
    # Keeps waiting after this..
    ```

 - FixRequest
     ```bash
     grpcurl -plaintext -d '{
        "issue": {
          "short_explanation": "SQL injection vulnerability",
          "long_explanation": "The code uses string concatenation to build SQL queries",
          "fix_steps": "Use parameterized queries instead",
          "file_locations": [
            {
              "file": "src/database.py",
              "start_line": 42,
              "end_line": 42
            }
          ],
          "type": "SECURITY"
        },
        "user_comment": "Please provide a secure fix for this SQL injection"
      }' localhost:50051 events.EventService.RequestFix

     # Output Generated in two places
     # For FixRequest:
        {
          "short_explanation": "Generic fix applied",
          "long_explanation": "Applied standard fix for this type of issue",
          "patch": "# Fix applied based on issue type"
        }

     # In StreamEvents
        {
          "type": "logstream",
          "logstream": {
            "guid": "system",
            "message": "Fix generated for: SQL injection vulnerability",
            "timestamp": "1757520491"
          },
          "timestamp": "2025-09-10T16:08:11.463933Z"
        }
     ```



