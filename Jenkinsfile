// The existing Jenkinsfile content...
pipeline {
    agent any
    environment {
        // Define your Docker credentials if needed, or other env variables
        DOCKER_IMAGE_NAME = "ecom-app"
    }
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                // Ensure the current SCM is checked out at the beginning
                checkout scm
            }
        }
        stage('Checkout Code') {
            steps {
                script {
                    // Re-checkout to ensure the workspace is clean and ready
                    checkout scm
                    echo "Code checked out from SCM."
                }
            }
        }
        stage('Docker Compose Build') {
            steps {
                script {
                    echo "--- Running Docker Diagnostics ---"
                    // Check Docker installation status
                    bat "docker info"

                    echo "--- Building all services defined in docker-compose.yml ---"
                    // Build the services
                    bat "docker-compose -f docker-compose.yml build"
                    echo "All Docker images successfully built!"
                }
            }
        }
        stage('Deploy Application') {
            steps {
                script {
                    echo "Stopping and removing old containers..."
                    // Shut down old containers (|| exit 0 prevents failure if no containers exist)
                    bat 'cmd /c "docker-compose -f docker-compose.yml down || exit 0"' 
                    
                    echo "Starting new containers with the newly built images..."
                    // Start containers, forcing recreation
                    bat "docker-compose -f docker-compose.yml up -d --force-recreate"
                    echo "E-Commerce services deployed. Frontend is on host port 80."
                }
            }
        }
        stage('Verify Health Check') {
            steps {
                // Using the Jenkins built-in sleep function instead of 'timeout /t 5'
                // This provides a platform-independent, reliable pause.
                echo "Waiting 5 seconds for services to start up..."
                sleep 5 
                
                // TODO: Add a proper health check script here (e.g., curl or Invoke-WebRequest)
                echo "Health check placeholder executed successfully."
            }
        }
    }
    post {
        always {
            echo "CI/CD Pipeline finished."
        }
        failure {
            echo "Build or deployment failed! Check the console output for errors."
        }
        success {
            echo "Build and deployment successful!"
        }
    }
}
