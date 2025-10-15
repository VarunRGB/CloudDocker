pipeline {
    // IMPORTANT: Docker Desktop must be running on the Jenkins host machine
    agent any 

    environment {
        // FIX: Using the Windows Named Pipe to reliably connect the Jenkins agent 
        // to the Docker daemon on the Windows machine.
        DOCKER_HOST = 'npipe:////./pipe/docker_engine'
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Retrieves all files from your GitHub repository
                checkout scm
                echo "Code checked out from SCM."
            }
        }

        stage('Docker Compose Build') {
            steps {
                script {
                    echo "--- Running Docker Diagnostics ---"
                    // This should now successfully show the Docker info
                    bat "docker info" 
                    
                    echo "--- Building all services defined in docker-compose.yml ---"
                    // Building the images using the named pipe connection
                    bat "docker-compose -f docker-compose.yml build" 
                    echo "All Docker images successfully built!"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo "Stopping and removing old containers..."
                    // Use 'exit 0' on failure to prevent pipeline breakage if containers aren't running
                    bat 'cmd /c "docker-compose -f docker-compose.yml down || exit 0"' 
                    
                    echo "Starting new containers with the newly built images..."
                    bat 'docker-compose -f docker-compose.yml up -d --force-recreate'
                    
                    echo "E-Commerce services deployed. Frontend is on host port 80."
                }
            }
        }

        stage('Verify Health Check') {
            steps {
                // Give containers time to initialize
                bat 'timeout /t 5 /nobreak'
                
                // 1. Verify the frontend is accessible (Note: Requires 'curl' or a similar tool in your Windows path)
                echo "Verifying Frontend accessibility at localhost:80"
                // If 'curl' fails, you may need to use 'powershell "Invoke-WebRequest -Uri http://localhost:80 -UseBasicParsing"'
                bat "curl -s http://localhost:80 | findstr /c:\"Welcome to the Automated Shop!\""
                
                // 2. Verify the internal catalog service
                echo "Verifying Catalog (internal health check)"
                bat "docker exec ecom-catalog curl -s http://ecom-catalog:5001/status | findstr /c:\"UP\""
            }
        }
    }
    
    post {
        always {
            echo "CI/CD Pipeline finished."
        }
        success {
            echo 'Deployment successful! Your e-commerce demo is live on host port 80.'
        }
        failure {
            echo 'Build or deployment failed! Check the console output for errors.'
        }
    }
}
