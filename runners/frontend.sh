#!/bin/bash

echo "Starting frontend..."
streamlit run src/app.py --server.port ${FRONTEND_PORT} --server.address ${FRONTEND_HOST}