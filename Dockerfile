FROM python:2.7-jessie

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 5000

RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates 
ADD app/ /app
RUN pip install -r /app/requirements.txt && pip install j2cli 

WORKDIR /app

ENV 	UPLOAD_DIR=/UPLOAD/ \
	BUNDLES_UPLOAD_DIR=/UPLOAD/BUNDLES/ \
	RAWPLANS_UPLOAD_DIR=/UPLOAD/RAWPLANS/ \
	MEASURES_UPLOAD_DIR=/UPLOAD/MEASURES/ \
	PLANS_UPLOAD_DIR=/UPLOAD/PLANS
RUN 	mkdir -p $BUNDLES_UPLOAD_DIR && \
	mkdir -p $RAWPLANS_UPLOAD_DIR && \
	mkdir -p $MEASURES_UPLOAD_DIR && \
	mkdir -p $PLANS_UPLOAD_DIR

VOLUME /UPLOAD
RUN 	env && j2 /app/properties.j2 > /app/properties.py && \
	cat /app/properties.py
CMD python /app/main.py
