pipeline {
    agent any

    tools {
        python 'Python3'
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'github-token',
                    url: 'https://github.com/TU_USUARIO/crud_usuarios.git',
                    branch: 'develop'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test
                '''
            }
        }

        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'sonar-scanner'
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    . venv/bin/activate
                    ${scannerHome}/bin/sonar-scanner
                    '''
                }
            }
        }
    }

    post {
        always {
            junit 'reports/*.xml'
        }
    }
}

