# Use Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json only (package-lock.json is ignored)
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose port 5173 for Vite
EXPOSE 5173

# Start Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
