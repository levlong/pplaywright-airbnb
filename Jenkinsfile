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

    stage('Setup venv') {
      steps {
        sh '''
          if [ ! -d venv ]; then
            python3 -m venv venv
          fi
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Install Playwright') {
      steps {
        sh '''
          . venv/bin/activate
          playwright install chromium
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest -v
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'playwright-report/**', allowEmptyArchive: true
      junit 'test-results/*.xml'
    }
  }
}
