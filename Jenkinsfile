pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        bat 'docker build -t cloud-docker-demo .'
      }
    }

    stage('Run Container') {
      steps {
        bat 'docker run --rm cloud-docker-demo'
      }
    }
  }

  post {
    success {
      echo '✅ Build and container run completed successfully!'
    }
    failure {
      echo '❌ Build failed. Check logs.'
    }
  }
}
