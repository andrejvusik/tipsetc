PROJECT_NAME := "TipsEtc..."

.DEFAULT: help

.PHONY: help
help:
	@echo "$(PROJECT_NAME)"
	@echo ""
	@echo "make help:"
	@echo "	- run this help."
	@echo ""
	@echo "make install:"
	@echo "	- install all requirements"
	@echo ""
	@echo "make update_requirements:"
	@echo "	- update requirements.txt with all packages installed in venv"
	@echo ""
	@echo "make update:"
	@echo "	- update all requirements"
	@echo ""
	@echo "make db_init:"
	@echo "	- init db migrations folder"
	@echo ""
	@echo "make db_migrate:"
	@echo "	- ccreate db migrations script"
	@echo ""
	@echo "make db_upgrade:"
	@echo "	- upgrade db"
	@echo ""
	@echo "make run:"
	@echo "	- run application"
	@echo ""
	@echo "make tests:"
	@echo "	- tests application"
	@echo ""
	@echo "make babel_extract"
	@echo " - extracting messages to translate"
	@echo ""
	@echo "make babel_update"
	@echo " - update messages to translate"
	@echo ""
	@echo "make babel_compile"
	@echo " - compile translations"
	@echo ""
	@echo "please make your choice..."

.PHONY: install
install:
	@echo "installing $(PROJECT_NAME)"
	@echo ""
	@( \
		python3 -m venv venv; \
		. venv/bin/activate; \
		pip install -r install/requirements.txt; \
		deactivate; \
	)
	@echo "install all requirements of $(PROJECT_NAME)"
	@echo ""

.PHONY: update_requirements
update_requirements:
	@echo "updating requirements.txt $(PROJECT_NAME)"
	@echo ""
	@( \
		python3 -m venv venv; \
		. venv/bin/activate; \
		pip freeze > install/requirements.txt; \
		deactivate; \
	)
	@echo "updated requirements.txt of $(PROJECT_NAME)"
	@echo ""
.PHONY: update
update:
		@echo "updating $(PROJECT_NAME)"
		@echo ""
		@( \
			python3 -m venv venv; \
			. venv/bin/activate; \
			pip install -r install/requirements.txt --upgrade; \
			deactivate; \
		)
		@echo "update all requirements of $(PROJECT_NAME)"
		@echo ""

.PHONY: db_init
db_init:
	@echo "initialization db migrations folder $(PROJECT_NAME)"
	@echo ""
	@( \
		. venv/bin/activate; \
		export FLASK_APP=main; \
		flask db init; \
	)
	@echo ""

.PHONY: db_migrate
db_migrate:
	@echo "creating db migrations script $(PROJECT_NAME)"
	@echo ""
	@( \
		. venv/bin/activate; \
		export FLASK_APP=main; \
		flask db migrate; \
	)
	@echo ""

.PHONY: db_upgrade
db_upgrade:
	@echo "upgrade db $(PROJECT_NAME)"
	@echo ""
	@( \
		. venv/bin/activate; \
		export FLASK_APP=main; \
		flask db upgrade; \
	)
	@echo ""

.PHONY: run
run:
	@echo "running $(PROJECT_NAME)"
	@echo ""
	@( \
		. venv/bin/activate; \
		export FLASK_APP=main; \
		export FLASK_ENV=development; \
		flask run; \
		export ELASTICSEARCH_URL=http://localhost:9200; \
	)
	@echo ""

.PHONY: tests
tests:
	@echo "testing $(PROJECT_NAME)"
	@echo ""
	@( \
		. venv/bin/activate; \
		python tests.py \
	)
	@echo ""

.PHONY: babel_extract
babel_extract:
	@echo "Extracting messages to translate"
	@echo ""
	@( \
		. venv/bin/activate; \
		pybabel extract -F blog/config/babel.cfg -k _l -o blog/translations/messages.pot .; \
		pybabel init -i blog/translations/messages.pot -d blog/translations -l ru \
		creating catalog blog/translations/ru/LC_MESSAGES/messages.po based on messages.pot \
	)

.PHONY: babel_update
babel_update:
	@echo "Update messages to translate"
	@echo ""
	@( \
		. venv/bin/activate; \
		pybabel extract -F blog/config/babel.cfg -k _l -o blog/translations/messages.pot .; \
		pybabel update -i blog/translations/messages.pot -d blog/translations \
	)

.PHONY: babel_compile
babel_compile:
	@echo "Compile translations"
	@echo ""
	@( \
		. venv/bin/activate; \
		pybabel compile -d blog/translations \
		compiling catalog blog/translations/ru/LC_MESSAGES/messages.po to blog/translations/ru/LC_MESSAGES/messages.mo \
		)
