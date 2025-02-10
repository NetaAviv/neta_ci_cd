#this jenkinsfile looks at the github repo every 5 minutes and if any changes where made it builds the image based on the dockerfile tests it and add it to dockerhub (without using the ansible we wrote) 
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-app'
        CONTAINER_NAME = 'my-app-container'
        DOCKER_REPO = 'netaaviv/jenkins_exe_2:latest'
    }

    triggers {
        pollSCM('H/5 * * * *') 
    }

    stages {
        stage('Build') {
            steps {
                script {
                    sh '''
                        docker build -t $IMAGE_NAME .
                        docker rmi $(docker images -f "dangling=true" -q) || true
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh '''
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                        docker run --name $CONTAINER_NAME -d $IMAGE_NAME
                        sleep 10
                        if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)" != "true" ]; then
                            echo "Container failed to start"
                            docker logs $CONTAINER_NAME
                            exit 1
                        fi
                    '''
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'DOCKER_PASSWORD', variable: 'DOCKER_PASS')]) {
                    script {
                        sh 'echo "$DOCKER_PASS" | docker login -u "netaaviv" --password-stdin'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        docker tag $IMAGE_NAME $DOCKER_REPO
                        docker push $DOCKER_REPO
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                sh 'docker logout'
            }
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
        success {
            echo 'Deployment successful!'
        }
    }
