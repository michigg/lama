FROM node:latest as develop-stage
WORKDIR /app
COPY lama/package*.json ./
RUN npm install

FROM develop-stage as build-stage
COPY ./lama .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
