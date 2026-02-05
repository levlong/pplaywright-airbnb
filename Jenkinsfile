pipeline {
  agent any

  options {
    timestamps()
  }

  triggers {
    cron('H 0 * * *')
  }

  parameters {
    booleanParam(name: 'ALLOW_RUN', defaultValue: false)
  }

  stages {
    stage('Gate Check') {
    when {
      expression { params.ALLOW_RUN }
    }

    steps {
        echo 'Backend build SUCCESS → Autotest allowed'
      }
    }

    stage('Checkout') {
      when {
        expression { params.ALLOW_RUN }
      }
      steps {
        checkout scm
      }
    }

    stage('Check python version') {
        when {
          expression { params.ALLOW_RUN }
        }
        steps {
            sh '''
            python3 --version
            '''
        }
    }

    stage('Setup venv') {
      when {
        expression { params.ALLOW_RUN }
      }
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
      when {
        expression { params.ALLOW_RUN }
      }
      steps {
        sh '''
          venv/bin/playwright install chromium
        '''
      }
    }

    stage('Run tests') {
      when {
        expression { params.ALLOW_RUN }
      }
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
