MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

# environment variables
.EXPORT_ALL_VARIABLES:
ifdef LINKML_ENVIRONMENT_FILENAME
include ${LINKML_ENVIRONMENT_FILENAME}
else
include config.public.mk
endif

RUN = uv run
SCHEMA_NAME = $(LINKML_SCHEMA_NAME)
SCHEMA_BASE_NAME = kbase_cdm
SCHEMA_ROOT = Entity
# from config.public.mk
# LINKML_SCHEMA_SOURCE_PATH=src/linkml/cdm_schema.yaml
LINKML_SCHEMA_FILE = $(LINKML_SCHEMA_SOURCE_PATH)
SRC_DIR = src
DEST_DIR = project
EXAMPLE_DIR = examples
# directory for documentation
DOC_DIR = docs
# jinja templates for generating docs
DOC_TEMPLATES_DIR = $(SRC_DIR)/docs/templates

# CDM schema directories
LINKML_DIR = $(SRC_DIR)/linkml
JSONSCHEMA_DIR = $(SRC_DIR)/jsonschema
PYTHON_DIR = $(SRC_DIR)/cdm_schema
# sample data
SAMPLE_DATA_DIR = sample_data

# unused
SHEET_MODULE = $(LINKML_SCHEMA_GOOGLE_SHEET_MODULE)
SHEET_ID = $(LINKML_SCHEMA_GOOGLE_SHEET_ID)
SHEET_TABS = $(LINKML_SCHEMA_GOOGLE_SHEET_TABS)
SHEET_MODULE_PATH = $(SRC_DIR)/sheets/$(SHEET_MODULE).yaml

# Use += to append variables from the variables file
CONFIG_YAML =
ifdef LINKML_GENERATORS_CONFIG_YAML
CONFIG_YAML += "--config-file"
CONFIG_YAML += ${LINKML_GENERATORS_CONFIG_YAML}
endif

GEN_DOC_ARGS =
ifdef LINKML_GENERATORS_DOC_ARGS
GEN_DOC_ARGS += ${LINKML_GENERATORS_DOC_ARGS}
endif

GEN_OWL_ARGS =
ifdef LINKML_GENERATORS_OWL_ARGS
GEN_OWL_ARGS += ${LINKML_GENERATORS_OWL_ARGS}
endif

GEN_JAVA_ARGS =
ifdef LINKML_GENERATORS_JAVA_ARGS
GEN_JAVA_ARGS += ${LINKML_GENERATORS_JAVA_ARGS}
endif

GEN_TS_ARGS =
ifdef LINKML_GENERATORS_TYPESCRIPT_ARGS
GEN_TS_ARGS += ${LINKML_GENERATORS_TYPESCRIPT_ARGS}
endif


.PHONY: all clean

# note: "help" MUST be the first target in the file,
# when the user types "make" they should get help info
help: status
	@echo ""
	@echo "make setup -- initial setup (run this first)"
	@echo "make site -- makes site locally"
	@echo "make install -- install dependencies"
	@echo "make test -- runs tests"
	@echo "make lint -- perform linting"
	@echo "make testdoc -- builds docs and runs local test server"
	@echo "make deploy -- deploys site"
	@echo "make update -- updates linkml version"
	@echo "make help -- show this help"
	@echo ""

status: check-config
	@echo "Project: $(SCHEMA_NAME)"
	@echo "Source: $(LINKML_SCHEMA_FILE)"

# generate products and add everything to github
setup: install gen-project gendoc # gen-examples

# install any dependencies required for building
install:
	uv sync
.PHONY: install


install-pygraphviz:
	uv add --config-settings="--globaal-option=build_ext" --config-settings="--global-option=-I$(brew --prefix graphviz)/include/"  --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/" pygraphviz --dev

update-packages: ## update packages in the uv lock file. Does not update pyproject.toml.
	uv sync -U

# EXPERIMENTAL
# create-data-harmonizer:
# 	npm init data-harmonizer $(LINKML_SCHEMA_FILE)

all: site
site: gen-project gendoc
%.yaml: gen-project
deploy: all mkd-gh-deploy

# compile-sheets:
# 	$(RUN) sheets2linkml --gsheet-id $(SHEET_ID) $(SHEET_TABS) > $(SHEET_MODULE_PATH).tmp && mv $(SHEET_MODULE_PATH).tmp $(SHEET_MODULE_PATH)

# In future this will be done by conversion
gen-examples:
	cp -r $(SAMPLE_DATA_DIR)/* $(EXAMPLE_DIR)

gen-project: $(PYTHON_DIR) ## generate all project files, save in $(DEST_DIR)
	$(RUN) gen-project ${CONFIG_YAML} -d $(DEST_DIR) $(LINKML_SCHEMA_FILE) && mv $(DEST_DIR)/*.py $(PYTHON_DIR)


# non-empty arg triggers owl (workaround https://github.com/linkml/linkml/issues/1453)
ifneq ($(strip ${GEN_OWL_ARGS}),)
	mkdir -p ${DEST_DIR}/owl || true
	$(RUN) gen-owl ${GEN_OWL_ARGS} $(LINKML_SCHEMA_FILE) >${DEST_DIR}/owl/${SCHEMA_NAME}.owl.ttl
endif
# non-empty arg triggers java
ifneq ($(strip ${GEN_JAVA_ARGS}),)
	$(RUN) gen-java ${GEN_JAVA_ARGS} --output-directory ${DEST_DIR}/java/ $(LINKML_SCHEMA_FILE)
endif
# non-empty arg triggers typescript
ifneq ($(strip ${GEN_TS_ARGS}),)
	mkdir -p ${DEST_DIR}/typescript || true
	$(RUN) gen-typescript ${GEN_TS_ARGS} $(LINKML_SCHEMA_FILE) >${DEST_DIR}/typescript/${SCHEMA_NAME}.ts
endif

test: test-schema test-python test-sample-data test-sample-data-jsonschema test-examples

test-schema: lint-validate lint
	$(RUN) gen-project ${CONFIG_YAML} -d /tmp $(LINKML_SCHEMA_FILE)

test-python:
	$(RUN) python -m pytest

lint:  ## lint the schema; warnings or errors result in a non-zero exit code
	$(RUN) linkml-lint $(LINKML_SCHEMA_FILE)

lint-validate:  ## validate the schema; warnings or errors result in a non-zero exit code
	$(RUN) linkml-lint --validate $(LINKML_SCHEMA_FILE)

lint-no-warn:  ## lint the schema; warnings do not result in a non-zero exit code
	$(RUN) linkml-lint --ignore-warnings $(LINKML_SCHEMA_FILE)

lint-validate-no-warn:  ## lint the schema; warnings do not result in a non-zero exit code
	$(RUN) linkml-lint --ignore-warnings --validate $(LINKML_SCHEMA_FILE)

test-sample-data:  ## validate sample data against LinkML schema
	$(RUN) linkml-validate -s $(LINKML_SCHEMA_FILE) sample_data/**/**/*.json

test-sample-data-jsonschema: ## validate sample data against JSONschema
	$(RUN) check-jsonschema --schemafile $(JSONSCHEMA_DIR)/$(SCHEMA_BASE_NAME).schema.json --verbose sample_data/**/**/*.json

check-config:
ifndef LINKML_SCHEMA_NAME
	$(error **Project not configured**:\n\n - See '.env.public'\n\n)
else
	$(info Ok)
endif

convert-examples-to-%:
	$(patsubst %, $(RUN) linkml-convert  % -s $(LINKML_SCHEMA_FILE) -C $(SCHEMA_ROOT), $(shell ${SHELL} find $(SAMPLE_DATA_DIR) -name "*.yaml"))

examples/%.yaml: $(SAMPLE_DATA_DIR)/%.yaml
	$(RUN) linkml-convert -s $(LINKML_SCHEMA_FILE) -C $(SCHEMA_ROOT) $< -o $@
examples/%.json: $(SAMPLE_DATA_DIR)/%.yaml
	$(RUN) linkml-convert -s $(LINKML_SCHEMA_FILE) -C $(SCHEMA_ROOT) $< -o $@
examples/%.ttl: $(SAMPLE_DATA_DIR)/%.yaml
	$(RUN) linkml-convert -P EXAMPLE=http://example.org/ -s $(LINKML_SCHEMA_FILE) -C $(SCHEMA_ROOT) $< -o $@

test-examples: examples/output

examples/output: src/$(SCHEMA_NAME)/schema/$(SCHEMA_NAME).yaml
	mkdir -p $@
	$(RUN) linkml-run-examples \
		--output-formats json \
		--output-formats yaml \
		--counter-example-input-directory $(SAMPLE_DATA_DIR)/invalid \
		--input-directory $(SAMPLE_DATA_DIR)/valid \
		--output-directory $@ \
		--schema $< > $@/README.md


serve: mkd-serve ## Test documentation locally

# Python directory
$(PYTHON_DIR):
	mkdir -p $@

# JSONschema dir
$(JSONSCHEMA_DIR):
	mkdir -p $@

# documentation dir
$(DOC_DIR):
	mkdir -p $@

gen-artefacts: $(PYTHON_DIR) $(JSONSCHEMA_DIR)  ## generate derived files: JSON Schema, Python, Pydantic, erdantic ERD.
	$(RUN) gen-json-schema $(LINKML_SCHEMA_SOURCE_PATH) > $(JSONSCHEMA_DIR)/$(SCHEMA_BASE_NAME).schema.json
	$(RUN) gen-python $(LINKML_SCHEMA_SOURCE_PATH) > $(PYTHON_DIR)/$(SCHEMA_BASE_NAME).py
	$(RUN) gen-pydantic $(LINKML_SCHEMA_SOURCE_PATH) > $(PYTHON_DIR)/$(SCHEMA_BASE_NAME)_pydantic.py
	$(RUN) ruff format $(PYTHON_DIR)
	PYTHONPATH=$(PYTHON_DIR) $(RUN) erdantic $(SCHEMA_BASE_NAME)_pydantic.$(SCHEMA_ROOT) -o $(SRC_DIR)/$(SCHEMA_BASE_NAME)-schema.png

gendoc: $(DOC_DIR)  ## generate Markdown documentation locally
	$(RUN) gen-doc ${GEN_DOC_ARGS} -d $(DOC_DIR) $(LINKML_SCHEMA_FILE)
	mkdir -p $(DOC_DIR)/js
	cp $(SRC_DIR)/docs/js/*.js $(DOC_DIR)/js/
	mkdir -p $(DOC_DIR)/pages
	cp $(SRC_DIR)/docs/pages/*.md $(DOC_DIR)/pages/
	mkdir -p $(DOC_DIR)/linkml
	cp $(LINKML_DIR)/*.yaml $(DOC_DIR)/linkml/

gendoc-gh: $(DOC_DIR) ## generate HTML documentation for deployment on GitHub Pages

	touch $(DOC_DIR)/.nojekyll
	make gendoc
	make mkd-gh-deploy

testdoc: gendoc serve

MKDOCS = $(RUN) mkdocs
mkd-%:
	$(MKDOCS) $*

clean:
	rm -rf $(DEST_DIR)
	rm -rf tmp
	rm -fr $(DOC_DIR)/*
	rm -fr $(PYTHON_DIR)/*

# include project.Makefile
