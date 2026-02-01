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
          set -e
          rm -rf venv
          python3 -m venv venv
          ls venv/bin
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
          venv/bin/pytest -v --html=reports/report.html --self-contained-html --css=assets/pytest_html.css
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
