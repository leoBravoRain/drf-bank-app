# 1. Use Node image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY ./analytics-service/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project
COPY ./analytics-service/ .

# Build the NestJS project
RUN npm run build

# --- Production Image ---
FROM node:18-alpine AS production

WORKDIR /app

# Copy only the necessary files from builder
COPY ./analytics-service/package*.json ./

# Install only production dependencies
RUN npm install --only=production

# Copy compiled dist folder
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Run the app
CMD ["node", "dist/main.js"]
