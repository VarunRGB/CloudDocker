pipeline {
    // Defines that the pipeline should run on any available agent (like your Jenkins server)
    // IMPORTANT: This agent must have Docker and Docker Compose installed.
    agent any 

    options {
        // Automatically abort builds that take longer than 15 minutes
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
                    echo "--- Building all services defined in docker-compose.yml ---"
                    // CHANGED: Using 'bat' for Windows execution
                    bat "docker-compose build" 
                    echo "All Docker images successfully built!"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo "Stopping and removing old containers..."
                    // CHANGED: Using 'bat' for Windows execution. Using 'cmd /c' to correctly handle the '|| true' on Windows.
                    bat 'cmd /c "docker-compose down || exit 0"' 
                    
                    echo "Starting new containers with the newly built images..."
                    // CHANGED: Using 'bat' for Windows execution
                    bat 'docker-compose up -d --force-recreate'
                    
                    echo "E-Commerce services deployed. Frontend is on host port 80."
                }
            }
        }

        stage('Verify Health Check') {
            steps {
                // Give the containers a few seconds to spin up
                bat 'timeout /t 5 /nobreak' // CHANGED: Windows equivalent of 'sleep 5'
                
                // 1. Verify the frontend is accessible on the host machine
                echo "Verifying Frontend accessibility at localhost:80"
                // WARNING: 'curl' might not exist on Windows. Using 'bat' and assuming curl is in your path, 
                // OR you can replace this with 'powershell "Invoke-WebRequest -Uri http://localhost:80 -UseBasicParsing | Select-Object -ExpandProperty Content"'
                // For simplicity, sticking with 'bat' and hoping 'curl' or an alias exists.
                bat "curl -s http://localhost:80 | findstr /c:\"Welcome to the Automated Shop!\""
                
                // 2. Verify the internal catalog service is running (must be done by executing a command inside a container)
                echo "Verifying Catalog (internal health check)"
                // CHANGED: Using 'bat' for Windows execution. Note the slightly different grep replacement (findstr).
                bat "docker exec ecom-catalog curl -s http://ecom-catalog:5001/status | findstr /c:\"UP\""
            }
        }
    }
    
    // Post-build actions for notification and cleanup
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
