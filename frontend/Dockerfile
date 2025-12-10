# Stage 1: Build
FROM node:20-slim AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN ls -R /app
RUN npm run build

# Stage 2: Runtime
FROM node:20-slim

WORKDIR /app

COPY --from=build /app/.output ./.output
# COPY --from=build /app/node_modules ./node_modules # .output usually contains necessary deps for standalone

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
