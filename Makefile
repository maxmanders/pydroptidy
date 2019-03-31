PROJECT_NAME := pydroptidy

SRC_PATH := $(CURDIR)/src
BUILD_PATH := $(CURDIR)/_build
COVERAGE_PATH := $(BUILD_PATH)/coverage
LINT_RESULT := $(BUILD_PATH)/lint.txt
REQUIREMENTS_RESULT := $(BUILD_PATH)/requirements.txt
LAMBDA_BUILD_PATH := $(BUILD_PATH)/lambda
LAMBDA_PACKAGE_PATH := $(LAMBDA_BUILD_PATH)/artifact
LAMBDA_ARTIFACT_ZIP := $(LAMBDA_BUILD_PATH)/$(PROJECT_NAME).zip


.PHONY: clean
clean:
	rm -rf $(BUILD_PATH)
	rm -rf node_modules/
	find $(SRC_PATH) -name "*.pyc" -delete
	find $(SRC_PATH) -type d -name __pycache__ -delete


.PHONY: build_dirs
build_dirs: $(BUILD_PATH)


$(BUILD_PATH):
	mkdir -p $(BUILD_PATH)
	mkdir -p $(COVERAGE_PATH)


.PHONY: get-serverless
get-serverless:
	npm install


.PHONY: requirements
requirements: $(REQUIREMENTS_RESULT)


$(REQUIREMENTS_RESULT): $(BUILD_PATH) $(SRC_PATH)/requirements.txt
	pip install -q --upgrade pip setuptools wheel
	pip install -q --upgrade --requirement $(SRC_PATH)/requirements.txt
	pip freeze > $@


.PHONY: setup
setup: clean requirements


.PHONY: format
format: requirements
	isort -rc $(SRC_PATH)
	black $(SRC_PATH)


.PHONY: lint
lint: requirements
	flake8 $(SRC_PATH) | tee $(LINT_RESULT)
	@# If the lint output is non-zero-length then there's lint issues so fail the build
	@test ! -s $(LINT_RESULT) || exit 1


.PHONY: unittest
unittest: requirements
	pytest $(SRC_PATH) --cov
	coverage html


.PHONY: test
test: unittest lint


.PHONY: build
build:
	rm -rf $(LAMBDA_PACKAGE_PATH) $(LAMBDA_ARTIFACT_ZIP)
	mkdir -p $(LAMBDA_PACKAGE_PATH)
	pip install -t $(LAMBDA_PACKAGE_PATH) --src $(LAMBDA_PACKAGE_PATH) --force-reinstall .
	find $(LAMBDA_PACKAGE_PATH) -name "*.pyc" -delete
	find $(LAMBDA_PACKAGE_PATH) -type d -name __pycache__ -delete
	find $(LAMBDA_PACKAGE_PATH)/$(PROJECT_NAME)/ -type d -name tests | xargs rm -rf
	rm -f $(LAMBDA_PACKAGE_PATH)/$(PROJECT_NAME)/settings/local.py
	cd $(LAMBDA_PACKAGE_PATH) && zip -q -r $(LAMBDA_ARTIFACT_ZIP) .
