FROM node:18-alpine

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY . /app

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build"]
