# Change the default config with `make cnf="custom.env" build`
cnf ?= config.env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

.PHONY: help

help: ## Display help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[35m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

run: ## Run Python script
	python3 main.py

package: ## Create Package
	pip3 install -q -t . -r requirements.txt --upgrade
	zip -r -q $(LAMBDA_PACKAGE) *
	du -hs $(LAMBDA_PACKAGE)

lambda: ## Create Lambda
	aws lambda create-function --function-name $(LAMBDA_NAME) --zip-file fileb://$(LAMBDA_PACKAGE) --handler main.handler --runtime python3.7

invoke: ## Invoke Lambda
	aws lambda invoke --function-name $(LAMBDA_NAME) out --log-type Tail --payload '{ "code": "$(PRODUCT)", "source": "$(SOURCE)" }' --profile $(LAMBDA_PROFILE) | jq -r .LogResult | base64 -d