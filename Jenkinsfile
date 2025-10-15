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
                    // This command reads the 'build' context in your docker-compose.yml
                    // and builds the ecom-frontend:latest and ecom-catalog:latest images.
                    sh "docker-compose build" 
                    echo "All Docker images successfully built!"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    echo "Stopping and removing old containers..."
                    // Shut down and remove any existing services from the previous deployment (|| true prevents job failure if nothing is running)
                    sh 'docker-compose down || true' 
                    
                    echo "Starting new containers with the newly built images..."
                    // Start the containers in detached mode (-d) and force them to use the fresh images (--force-recreate)
                    sh 'docker-compose up -d --force-recreate'
                    
                    echo "E-Commerce services deployed. Frontend is on host port 80."
                }
            }
        }

        stage('Verify Health Check') {
            steps {
                // Give the containers a few seconds to spin up
                sh 'sleep 5'
                
                // 1. Verify the frontend is accessible on the host machine
                echo "Verifying Frontend accessibility at localhost:80"
                sh "curl -s http://localhost:80 | grep 'Welcome to the Automated Shop!'"
                
                // 2. Verify the internal catalog service is running (must be done by executing a command inside a container)
                echo "Verifying Catalog (internal health check)"
                // We use 'docker exec' to run curl inside the 'ecom-catalog' container to hit its own health endpoint
                sh "docker exec ecom-catalog curl -s http://ecom-catalog:5001/status | grep 'UP'"
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