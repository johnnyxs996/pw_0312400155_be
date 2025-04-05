#!/bin/sh
set -ue

case "${1:-}" in
    -start)
        python -m app.main
        ;;

    -start-debug)
        python -m debugpy --listen 0.0.0.0:5678 -m app.main
        ;;
esac

exec "$@"
