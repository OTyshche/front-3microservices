pipeline {
    agent any
    
    environment {
        PYTHON_IMAGE = 'my-python:latest'
        GO_IMAGE = 'my-go:latest'
        JS_IMAGE = 'my-js:latest'
        FRONTEND_IMAGE = 'my-frontend:latest'
    }
    
    stages {
        stage('Github clone') {
            steps {
                echo "Starting clonning the project"
                git branch: 'main', url: 'https://github.com/OTyshche/front-3microservices'
            }
        }
        
        stage('Images build') {
            steps {
                dir('backend/random_service') {
                    sh 'docker build -t $GO_IMAGE .'
                }
                dir('backend/time_service') {
                    sh 'docker build -t $JS_IMAGE .'
                }
                dir('backend/user_service') {
                    sh 'docker build -t $PYTHON_IMAGE .'
                }
                dir('frontend') {
                    sh 'docker build -t $FRONTEND_IMAGE .'
                }
            }
        }
        
        stage('Cleanup of old containers') {
            steps {
                sh 'docker stop front || true'
                sh 'docker stop go || true'
                sh 'docker stop js || true'
                sh 'docker stop python || true'
                sh 'docker container prune -f || true'
            }
        }
        
        stage('Run services') {
            steps {
                sh 'docker run -d --name front -p 80:80 $FRONTEND_IMAGE'
                sh 'docker run -d --name go -p 8081:8081 $GO_IMAGE'
                sh 'docker run -d --name js -p 3001:3001 $JS_IMAGE'
                sh 'docker run -d --name python -p 5001:5001 $PYTHON_IMAGE'
            }
        }
        
        stage('Wait for Service') {
            steps {
                echo 'Waiting 60 seconds for service to start...'
                sleep time: 60, unit: 'SECONDS'
            }
        }
        
        stage('Run tests') {
            steps {
                dir('tests') {
                    sh 'python3 test_microservices.py'
                }
            }
        }
    }
    
    post {
        success {
            echo 'System successfuly deployed'
        }
        failure {
            echo 'Tests failed. Cleaning up containers...'
            sh 'docker stop front || true'
            sh 'docker stop go || true'
            sh 'docker stop js || true'
            sh 'docker stop python || true'
            sh 'docker image rm -f $FRONTEND_IMAGE || true'
            sh 'docker image rm -f $GO_IMAGE || true'
            sh 'docker image rm -f $JS_IMAGE || true'
            sh 'docker image rm -f $PYTHON_IMAGE || true'
            sh 'docker container prune -f || true'
        }
    }
}
