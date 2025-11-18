pipeline {
    agent any

    tools {
        python 'Python3'
    }

    environment {
        scannerHome = tool 'sonar-scanner'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'develop',
                    credentialsId: 'github-token',
                    url: 'https://github.com/Jhoan641/crud_usuarios.git'
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
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    . venv/bin/activate
                    ${scannerHome}/bin/sonar-scanner
                    '''
                }
            }
        }

        stage('Docker Build & Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build -t crud-usuarios:latest .

                echo "Loading image into Minikube..."
                minikube image load crud-usuarios:latest

                echo "Applying Kubernetes manifests..."
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/*.xml'
        }
    }
}

