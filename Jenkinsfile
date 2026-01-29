pipeline {
   agent { 
        dockerContainer {
        image 'mcr.microsoft.com/playwright/python:v1.57.0-noble'
        args '-u root'
        } 
    }

    triggers {
        githubPush()
    }

   stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('e2e-tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
      }
   }
}