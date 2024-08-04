#!/bin/bash

<<blockComment 
- 
blockComment
echo -e "INFO(utl_dkr_preRun):\t Initializing ..."

strpth_pwd=$(pwd)
strpth_scriptLoc=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
strpth_scrHome="${strpth_scriptLoc}/../"
strpth_appHome="${strpth_scrHome}../"
strpth_scrModels="${strpth_scrHome}models/"

#echo "strpth_appHome = ${strpth_appHome}"

#--- for nginx;  external 7860;  internal 7860
service nginx start

#--- for fastapi;  external 49132;  internal 39132
echo "INFO:  starting fastapi ..."
uvicorn --app-dir=./fastapi_app entry_fastapi:app --reload --workers 1 --host 0.0.0.0 --port 39132 &          #--- specify a non-root app dir


#--- for streamlit;  external 49131;  internal 39131
echo "INFO:  starting streamlit ..."
streamlit run ./streamlit_app/entry_streamlit.py --server.port=39131 --server.maxUploadSize=2000            #--- & run in the background



<<blockErrorLog
blockErrorLog