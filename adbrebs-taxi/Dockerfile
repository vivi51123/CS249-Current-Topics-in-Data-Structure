
FROM nvcr.io/nvidia/tensorflow:17.12

RUN apt-get update && apt-get install --no-install-recommends -y \
        git \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install build-essential
#RUN pip install ***

WORKDIR /thunlp/OpenKE

CMD echo 'test before' >test.txt
CMD bash make.sh
CMD echo 'test operation' >test.txt
CMD THEANO_FLAGS=floatX=float32,device=cuda,optimizer=fast_run python example.py


