pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Verify') {
      steps {
        echo '✅ Repo cloned and Jenkinsfile found!'
      }
    }
  }
}
