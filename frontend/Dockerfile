# Используем официальный Node.js образ
FROM node:19-alpine

# Устанавливаем рабочую директорию
WORKDIR ./app

# Копируем package.json и package-lock.json
COPY package*.json .
RUN npm install

# Копируем остальные файлы проекта
COPY . /app
CMD ["npm", "run", "dev", "--", "--host"]
## Устанавливаем Nginx
#FROM nginx:alpine
#
## Копируем сборку проекта в директорию Nginx
#COPY --from=0 /app/dist /usr/share/nginx/html
#
## Копируем конфигурационный файл Nginx
#COPY nginx.conf /etc/nginx/nginx.conf
#
## Открываем порт 80
#EXPOSE 80
#
## Запускаем Nginx
#CMD ["nginx", "-g", "daemon off;"]
