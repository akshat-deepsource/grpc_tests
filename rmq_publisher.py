import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# make sure the queue exists

channel.queue_declare(queue="hello")

rmq_analyzer_task_message_json = """{
    "id": "task_12345",
    "task": "analyze_code_quality",
    "kwargs": {
      "run_id": "run_67890",
      "status": {
        "code": 200,
        "hmessage": "Analysis completed successfully",
        "err": ""
      },
      "check_seq": "seq_001",
      "report": {
        "issues": [
          {
            "issue_code": "W001",
            "issue_text": "Unused variable found",
            "location": {
              "path": "/src/main.py",
              "position": {
                "begin": {
                  "line": 15,
                  "column": 4
                },
                "end": {
                  "line": 15,
                  "column": 12
                }
              }
            },
            "processed_data": {
              "source_code": {
                "rendered": ["dmFyIHVudXNlZF92YXJpYWJsZSA9IDEwOw=="]
              }
            },
            "identifier": "unused_var_main_15"
          }
        ],
        "metrics": [
          {
            "metric_code": "M001",
            "namespace": [
              {
                "key": "complexity",
                "value": "low",
                "metadata": {
                  "score": 2.5
                }
              }
            ]
          }
        ],
        "is_passed": true,
        "errors": [],
        "file_meta": {
          "if_all": false,
          "deleted": [],
          "renamed": [],
          "modified": ["src/main.py"],
          "added": [],
          "diff_meta": {
            "src/main.py": {
              "additions": [[15, 18], [22, 24]],
              "deletions": [[10, 12]]
            }
          },
          "pr_diff_meta": null
        },
        "extra_data": {
          "analysis_duration": "2.5s",
          "tool_version": "1.0.0"
        }
      },
      "report_object": "54f0c1eb-dbca-4c69-bb55-410682e0acfa/1/20250910-105537-aef44b30"
    },
    "retries": 0
  }"""
# for i in range(10):
channel.basic_publish(
    exchange="", routing_key="hello", body=rmq_analyzer_task_message_json
)
print(f" [x] sent 'message'")

connection.close()
