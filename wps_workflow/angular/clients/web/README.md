# WPSflow Web Client

1. Install Angular CLI **npm install @angular/cli**

## Developement
1. Start WPSServer **python3 manage.py runserver** inside server folder
2. Run **ng serve** inside client folder

## Build
1. Modify IP in client/web/src/environments/environments.prod.ts
2. Run **ng build --prod --output-hashing none**
3. Copy all files from client/web/dist into server/static
