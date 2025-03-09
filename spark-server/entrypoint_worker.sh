#!/bin/bash
# spark/entrypoint.sh

# Start Spark Worker with resource limits
/spark/sbin/start-worker.sh spark://spark-server:7077 \
    --cores 8 \
    --memory 8G \
    --work-dir /spark/work-dir

# Keep container alive
tail -f /dev/null
