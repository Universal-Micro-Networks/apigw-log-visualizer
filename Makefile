START_DATE ?= 2024-01-01
# for Mac
END_DATE ?= $(shell date -v-1d +%Y-%m-%d)

# for Linux
#END_DATE ?= $(shell date -d '1 days ago' '+%Y-%m-%d')
MARKER ?= ""

docker-up:
	docker-compose up
docker-reset:
	docker-compose down --volumes
fetch-log-%:
	python packages/log_collection/presentation/apigw_log.py -t "fetch_log" -e ${@:fetch-log-%=%} -S $(START_DATE) -E $(END_DATE) -m $(MARKER)
load-log:
	python packages/log_collection/presentation/apigw_log.py -t "load_log"
