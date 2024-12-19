FROM node:20.10.0-alpine as base

WORKDIR /app

COPY package*.json ./
RUN npm install

FROM base as js-test

COPY . .

CMD ["npm", "run", "test:infrastructure"]
