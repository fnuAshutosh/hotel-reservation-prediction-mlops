pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "traveler-ai-project"
        GCLOUD_PATH = "/var/jekins_home/google-cloud-sdk/bin"
    }
    stages {
        // Stage 1: Clone Repository
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins...........' 
                    checkout scmGit(
                        branches: [[name: 'main']], 
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/fnuAshutosh/hotel-reservation-prediction-mlops.git'
                        ]]
                    )
                }
            }
        }

        // Stage 2: Setup Environment
        stage('Setting up our virtual environment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and dependencies...' 
                    sh ''' 
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install -e .
                    '''
                }
            }
        }

        // Stage 3: Setup Environment
        stage('BUILDING AND PUSHING DOCKER IMAGE TO GCR') {
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'BUILDING AND PUSHING DOCKER IMAGE TO GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gor.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gor.io/${GCP_PROJECT}/ml-project:latest

                        '''
                    }
                }
            }
        }
    }
}