# Build stage
FROM golang:1.18 AS build
WORKDIR /go/src

# Copy go.mod and go.sum files to use them for downloading dependencies
COPY go.mod go.sum ./

# Download dependencies to the module cache
RUN go mod download

# Copy the rest of the application
COPY . .

# Ensure the /tmp directory has the correct permissions
RUN chmod 1777 /tmp

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o openapi .

# Runtime stage
FROM alpine:3.14

# Install ffmpeg
RUN apk add --no-cache ffmpeg

# Copy the built binary from the build stage
COPY --from=build /go/src/openapi /openapi

# Expose the port that the application listens on
EXPOSE 4000

# Set the entrypoint to run the application
ENTRYPOINT ["./openapi"]