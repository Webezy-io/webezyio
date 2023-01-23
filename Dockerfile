FROM python:3.9 
# Or any preferred Python version.
COPY ./dist/webezyio-0.1.8.tar.gz /webezyio/webezyio-0.1.8.tar.gz
RUN pip install ./webezyio/webezyio-0.1.8.tar.gz
CMD ["wz"]
# Or enter the name of your unique directory and parameter set.