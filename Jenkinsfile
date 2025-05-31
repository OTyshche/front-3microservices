pipeline {
    agent any
    
    environment {
        PYTHON_IMAGE = 'my-python:latest'
        GO_IMAGE = 'my-go:latest'
        JS_IMAGE = 'my-js:latest'
        FRONTEND_IMAGE = 'my-frontend:latest'
        GATEWAY_IMAGE = 'my-gateway:latest'
        DOCKER_CREDENTIALS_ID = 'boodiebo'
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
                    sh 'docker build -t $DOCKER_CREDENTIALS_ID/$GO_IMAGE .'
                }
                dir('backend/time_service') {
                    sh 'docker build -t $DOCKER_CREDENTIALS_ID/$JS_IMAGE .'
                }
                dir('backend/user_service') {
                    sh 'docker build -t $DOCKER_CREDENTIALS_ID/$PYTHON_IMAGE .'
                }
                dir('backend/gateway'){
                    sh 'docker build -t $DOCKER_CREDENTIALS_ID/$GATEWAY_IMAGE .'
                }
                dir('frontend') {
                    sh 'docker build -t $DOCKER_CREDENTIALS_ID/$FRONTEND_IMAGE .'
                }
            }
        }
        
        stage('Cleanup of old containers') {
            steps {
                sh 'docker rm -f front || true'
                sh 'docker rm -f go || true'
                sh 'docker rm -f js || true'
                sh 'docker rm -f python || true'
                sh 'docker rm -f gateway || true'
            }
        }
        
        stage('Run services') {
            steps {
                sh 'docker run -d --name front -p 80:80 $DOCKER_CREDENTIALS_ID/$FRONTEND_IMAGE'
                sh 'docker run -d --name go -p 8081:8081 $DOCKER_CREDENTIALS_ID/$GO_IMAGE'
                sh 'docker run -d --name js -p 3001:3001 $DOCKER_CREDENTIALS_ID/$JS_IMAGE'
                sh 'docker run -d --name python -p 5001:5001 $DOCKER_CREDENTIALS_ID/$PYTHON_IMAGE'
                sh 'docker run -d --name gateway -p 8082:8082 $DOCKER_CREDENTIALS_ID/$GATEWAY_IMAGE'
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

        stage('Cleanup') {
            steps {
                echo 'Tests were successful. Cleaning up containers...'
                sh 'docker rm -f front || true'
                sh 'docker rm -f go || true'
                sh 'docker rm -f js || true'
                sh 'docker rm -f python || true'
                sh 'docker rm -f gateway || true'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Pushing images to Docker Hub...'
                sh "docker push $DOCKER_CREDENTIALS_ID/$FRONTEND_IMAGE"
                sh "docker push $DOCKER_CREDENTIALS_ID/$GO_IMAGE"
                sh "docker push $DOCKER_CREDENTIALS_ID/$JS_IMAGE"
                sh "docker push $DOCKER_CREDENTIALS_ID/$PYTHON_IMAGE"
                sh "docker push $DOCKER_CREDENTIALS_ID/$GATEWAY_IMAGE"
                echo 'Images pushed successfully.'
            }
        }
        
        stage('Cleanup images') {
            steps {
                echo 'Cleaning up images...'
                sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$FRONTEND_IMAGE || true'
                sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$GO_IMAGE || true'
                sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$JS_IMAGE || true'
                sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$PYTHON_IMAGE || true'
                sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$GATEWAY_IMAGE || true'
            }
        }

        stage('Deploying kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                dir('frontend'){
                    h 'kubectl apply -f anifest.yaml'
                }
                dir('backend/random_service') {
                    sh 'kubectl apply -f manifest.yaml'
                }
                dir('backend/time_service') {
                    sh 'kubectl apply -f manifest.yaml'
                }
                dir('backend/user_service') {
                    sh 'kubectl apply -f manifest.yaml'
                }
                dir('backend/gateway') {
                    sh 'kubectl apply -f manifest.yaml'
                }
                echo 'Kubernetes deployment completed.'
            }
        }

    }
    
    post {
        success {
            echo 'All stages completed successfully.'
        }
        failure {
            echo 'Tests failed. Cleaning up containers...'
            sh 'docker rm -f front || true'
            sh 'docker rm -f go || true'
            sh 'docker rm -f js || true'
            sh 'docker rm -f python || true'
            sh 'docker rm -f gateway || true'
            sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$FRONTEND_IMAGE || true'
            sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$GO_IMAGE || true'
            sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$JS_IMAGE || true'
            sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$PYTHON_IMAGE || true'
            sh 'docker image rm -f $DOCKER_CREDENTIALS_ID/$GATEWAY_IMAGE || true'
            echo 'Containers and images cleaned up.'
        }
    }
} 