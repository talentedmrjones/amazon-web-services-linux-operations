FROM node:6.11.0-alpine

# Install app dependencies
COPY package.json /src/package.json
RUN cd /src; npm install

# Bundle app source
COPY . /src

EXPOSE 3000
CMD ["node", "/src/server.js"]
