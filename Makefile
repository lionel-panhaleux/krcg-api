.PHONY: serve

serve:
	source .env && uwsgi --socket 127.0.0.1:8000 --protocol=http  --module krcg_api.wsgi:application
