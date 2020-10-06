FROM node:12-alpine AS ts-builder
WORKDIR /app
COPY package.json /app
RUN npm install
COPY . .
RUN npm run build

FROM node:12-alpine
WORKDIR /app
COPY --from=ts-builder ./app/dist /app/dist
COPY *.json /app/
RUN npm install --production
CMD npm start