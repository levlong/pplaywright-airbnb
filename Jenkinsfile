pipeline {
  agent any

  options {
    timestamps()
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Check python version') {
        steps {
            sh '''
            python3 --version
            '''
        }
    }

    stage('Setup venv') {
      steps {
        sh '''
          if [ ! -d venv ]; then
            python3 -m venv venv
          fi
          venv/bin/pip install --upgrade pip
          venv/bin/pip install -r requirements.txt
        '''
      }
    }

    stage('Install Playwright') {
      steps {
        sh '''
          venv/bin/playwright install chromium
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          venv/bin/pytest -v --html=reports/report.html --self-contained-html
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
  }
}
