import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# make sure the queue exists
channel.queue_declare(queue='hello')

json_msg = """{
    "run_id": "analysis_run_67890",
    "status": {
      "code": 0,
      "hmessage": "Analysis completed successfully",
      "err": ""
    },
    "check_seq": "check_sequence_001",
    "report": {
      "issues": [
        {
          "issue_code": "SEC001",
          "issue_text": "Hardcoded credentials detected in configuration file",
          "location": {
            "path": "src/config/database.py",
            "position": {
              "begin": {
                "line": 15,
                "column": 1
              },
              "end": {
                "line": 15,
                "column": 45
              }
            }
          },
          "processed_data": {
            "source_code": {
              "rendered": ["DATABASE_PASSWORD = \\"admin123\\""]
            }
          },
          "identifier": "hardcoded_creds_001"
        },
        {
          "issue_code": "PERF002",
          "issue_text": "Inefficient database query in loop",
          "location": {
            "path": "src/services/user_service.py",
            "position": {
              "begin": {
                "line": 42,
                "column": 8
              },
              "end": {
                "line": 44,
                "column": 35
              }
            }
          },
          "processed_data": null,
          "identifier": "n_plus_one_query_001"
        }
      ],
      "metrics": [
        {
          "metric_code": "COMPLEXITY",
          "namespace": [
            {
              "key": "cyclomatic_complexity",
              "value": "12",
              "metadata": {
                "threshold": "10",
                "function_name": "process_user_data"
              }
            }
          ]
        },
        {
          "metric_code": "COVERAGE",
          "namespace": [
            {
              "key": "line_coverage",
              "value": "85.7",
              "metadata": {
                "total_lines": 350,
                "covered_lines": 300
              }
            }
          ]
        }
      ],
      "is_passed": false,
      "errors": [
        {
          "hmessage": "Could not parse syntax in legacy_module.py",
          "level": 2
        }
      ],
      "file_meta": {
        "if_all": false,
        "deleted": ["deprecated/old_auth.py"],
        "renamed": ["utils.py -> shared_utils.py"],
        "modified": [
          "src/config/database.py",
          "src/services/user_service.py",
          "tests/test_auth.py"
        ],
        "added": [
          "src/middleware/rate_limiter.py",
          "docs/api_changes.md"
        ],
        "diff_meta": {
          "src/config/database.py": {
            "additions": [[15, 17], [23, 25]],
            "deletions": [[14, 14], [22, 22]]
          },
          "src/services/user_service.py": {
            "additions": [[42, 44], [67, 70]],
            "deletions": []
          }
        },
        "pr_diff_meta": {
          "feature/security-fixes": {
            "src/config/database.py": {
              "additions": [[15, 17]],
              "deletions": [[14, 14]]
            }
          }
        }
      },
      "extra_data": {
        "analysis_duration_seconds": 45.2,
        "analyzer_version": "3.1.4",
        "rules_version": "2023.12.01",
        "total_files_analyzed": 127,
        "skipped_files": ["node_modules/", "*.min.js"]
      }
    },
    "report_object": "eyJhbmFseXNpcyI6ICJiYXNlNjQgZW5jb2RlZCByZXBvcnQgZGF0YSJ9"
  }"""
# for i in range(10):
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json_msg)
print(f" [x] sent 'message'")

connection.close()
