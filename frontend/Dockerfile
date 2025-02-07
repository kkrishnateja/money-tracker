# Use Node.js image based on Alpine
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy only package.json to generate a fresh lock file
COPY package.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the React app
RUN npm run build

# Expose port 5173 for Vite
EXPOSE 5173

# Start Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
