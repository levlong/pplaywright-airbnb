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
            py -m venv venv
          fi
          . venv/bin/activate
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

    stage('Generate report') {
      steps {
        sh '''
          . venv/bin/activate
          pytest --html=reports/report.html --self-contained-html
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
