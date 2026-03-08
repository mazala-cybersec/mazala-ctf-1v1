FROM node:20-slim
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY app.js .
ENV FLAG="mazala{jwt_4lg_n0n3}"
ENV PORT=5000
EXPOSE 5000
RUN addgroup --system ctf && adduser --system --ingroup ctf ctf
USER ctf
CMD ["node", "app.js"]
