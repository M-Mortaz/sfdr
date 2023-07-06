if [[ "$ENTRYPOINT" = "celery_worker" ]]
then
  echo Starting celery workers
  celery -A champertor worker -l INFO --pool eventlet --concurrency "${CELERY_CONCURRENCY:-10}"  \
    --max-tasks-per-child "${CELERY_MAX_TASKS_PER_CHILD:-100}" --prefetch-multiplier "${CELERY_PREFETCH_MULTIPLIER:-1}"
elif [[ "$ENTRYPOINT" = "celery_beat" ]]
then
  echo Starting beat schedulers
  celery -A champertor beat -l INFO
elif [[ -z "$ENTRYPOINT" ]] || [[ "$ENTRYPOINT" = "web" ]]
then
   echo "Starting web" && gunicorn --config gunicorn_config.py  champertor.wsgi:application
else
  echo Error, cannot find entrypoint $ENTRYPOINT to start
fi
