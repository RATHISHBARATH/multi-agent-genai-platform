
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install --silent
COPY . .
ENV NODE_ENV=production
CMD ["npm","run","dev"]
