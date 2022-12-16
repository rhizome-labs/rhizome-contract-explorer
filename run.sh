npx tailwindcss -i ./rhizome_contract_caller/app/css/main.css -o ./rhizome_contract_caller/app/static/style.css --minify --watch &
uvicorn rhizome_contract_caller.app.main:app --reload --port 8001